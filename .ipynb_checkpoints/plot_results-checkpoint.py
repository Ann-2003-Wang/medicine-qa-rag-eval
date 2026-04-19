import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_accuracy_by_strategy(df: pd.DataFrame, save_dir="outputs/figures"):
    os.makedirs(save_dir, exist_ok=True)

    pivot_df = df.pivot(index="strategy", columns="model", values="accuracy")
    ax = pivot_df.plot(kind="bar", figsize=(10, 6))

    plt.title("Accuracy by Strategy and Model")
    plt.xlabel("Strategy")
    plt.ylabel("Accuracy")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "accuracy_by_strategy.png"), dpi=200)
    plt.show()


def plot_latency_by_strategy(df: pd.DataFrame, save_dir="outputs/figures"):
    os.makedirs(save_dir, exist_ok=True)

    pivot_df = df.pivot(index="strategy", columns="model", values="avg_latency")
    ax = pivot_df.plot(kind="bar", figsize=(10, 6))

    plt.title("Average Latency by Strategy and Model")
    plt.xlabel("Strategy")
    plt.ylabel("Average Latency (s)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "latency_by_strategy.png"), dpi=200)
    plt.show()


def plot_parse_success(df: pd.DataFrame, save_dir="outputs/figures"):
    os.makedirs(save_dir, exist_ok=True)

    pivot_df = df.pivot(index="strategy", columns="model", values="parse_success_rate")
    ax = pivot_df.plot(kind="bar", figsize=(10, 6))

    plt.title("Parse Success Rate by Strategy and Model")
    plt.xlabel("Strategy")
    plt.ylabel("Parse Success Rate")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "parse_success_rate.png"), dpi=200)
    plt.show()


def main():
    df = pd.read_csv("outputs/all_metrics.csv")

    print(df)

    plot_accuracy_by_strategy(df)
    plot_latency_by_strategy(df)
    plot_parse_success(df)


if __name__ == "__main__":
    main()