import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

CSV_PATH = Path("bench/results.csv")
PLOTS_DIR = Path("bench/plots")

COLOR = {"grpc": "#1f77b4", "rest": "#d62728"}


def load(csv_path):
    rows = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "protocol": row["protocol"],
                    "latency_ms": int(row["latency_ms"]),
                    "run": int(row["run"]),
                    "total_requests": int(row["total_requests"]),
                    "total_time": float(row["total_time"]),
                    "requests_per_sec": float(row["requests_per_sec"]),
                }
            )
    return rows


def aggregate(rows, group_key, metric="requests_per_sec"):
    """Agrupa por chave única, retorna lista [(key, mean, stdev, n), ...] ordenada."""
    buckets = defaultdict(list)
    for r in rows:
        buckets[r[group_key]].append(r[metric])
    out = []
    for key, vals in sorted(buckets.items()):
        mean = statistics.mean(vals)
        stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
        out.append((key, mean, stdev, len(vals)))
    return out


def plot_throughput_vs_volume(rows, out_path):
    lh = [r for r in rows if r["latency_ms"] == 0]
    if not lh:
        print("sem dados em latency_ms=0; pulando throughput_vs_volume")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    for protocol in ["grpc", "rest"]:
        proto_rows = [r for r in lh if r["protocol"] == protocol]
        if not proto_rows:
            continue
        agg = aggregate(proto_rows, "total_requests")
        xs = [k for k, *_ in agg]
        ys = [m for _, m, *_ in agg]
        errs = [s for _, _, s, _ in agg]
        ax.errorbar(
            xs, ys, yerr=errs,
            marker="o", capsize=4, linewidth=1.5,
            label=protocol.upper(), color=COLOR.get(protocol),
        )

    ax.set_xlabel("Total de requests")
    ax.set_ylabel("Requests/sec")
    ax.set_title("Throughput vs volume de requests (localhost)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"saved {out_path}")
    plt.close(fig)


def plot_throughput_vs_latency(rows, out_path):
    latencies = sorted({r["latency_ms"] for r in rows})
    if len(latencies) < 2:
        print(
            f"só tem dados em latency_ms={latencies}; "
            "pulando throughput_vs_latency (precisa >=2 latências)"
        )
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    for protocol in ["grpc", "rest"]:
        proto_rows = [r for r in rows if r["protocol"] == protocol]
        if not proto_rows:
            continue
        agg = aggregate(proto_rows, "latency_ms")
        xs = [k for k, *_ in agg]
        ys = [m for _, m, *_ in agg]
        errs = [s for _, _, s, _ in agg]
        ax.errorbar(
            xs, ys, yerr=errs,
            marker="o", capsize=4, linewidth=1.5,
            label=protocol.upper(), color=COLOR.get(protocol),
        )

    ax.set_xlabel("Latência simulada (ms)")
    ax.set_ylabel("Requests/sec")
    ax.set_title("Throughput vs latência de rede")
    ax.legend()
    ax.grid(True, alpha=0.3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"saved {out_path}")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=CSV_PATH)
    parser.add_argument("--out-dir", type=Path, default=PLOTS_DIR)
    args = parser.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"CSV não encontrado: {args.csv}")

    rows = load(args.csv)
    if not rows:
        raise SystemExit("CSV vazio.")

    print(f"carregado {len(rows)} linhas de {args.csv}")
    plot_throughput_vs_volume(rows, args.out_dir / "throughput_vs_volume.png")
    plot_throughput_vs_latency(rows, args.out_dir / "throughput_vs_latency.png")


if __name__ == "__main__":
    main()
