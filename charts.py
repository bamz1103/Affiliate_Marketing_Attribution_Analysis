import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from attribution import run_all_models

results, df, converters = run_all_models()

# ── Visual style ──────────────────────────────────────
CHANNEL_COLORS = {
    "Google":     "#4285F4",
    "Facebook":   "#1877F2",
    "Email":      "#34A853",
    "Direct":     "#FBBC05",
    "Affiliate1": "#EA4335"
}

MODELS = ["Last-Click", "Linear", "Time-Decay"]
CHANNELS = ["Google", "Facebook", "Email", "Direct", "Affiliate1"]


def chart_revenue_comparison():
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.suptitle("Attributed Revenue by Channel Across 3 Models",
                 fontsize=16, fontweight="bold", y=1.02)

    for ax, model in zip(axes, MODELS):
        data = results[results["model"] == model].sort_values(
            "attributed_revenue", ascending=False
        )
        colors = [CHANNEL_COLORS[ch] for ch in data["channel"]]
        bars = ax.bar(data["channel"], data["attributed_revenue"],
                      color=colors, edgecolor="white", linewidth=0.8)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 500,
                f"£{height:,.0f}",
                ha="center", va="bottom", fontsize=9, fontweight="bold"
            )

        ax.set_title(model, fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("Channel", fontsize=10)
        ax.set_ylabel("Attributed Revenue (£)", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
        ax.tick_params(axis="x", rotation=15)
        ax.set_ylim(0, results["attributed_revenue"].max() * 1.15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("charts/chart1_revenue_comparison.png", dpi=150, bbox_inches="tight")
    print("Saved: charts/chart1_revenue_comparison.png")


def chart_pct_share_grouped():
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(CHANNELS))
    width = 0.25
    offsets = [-width, 0, width]
    model_colors = ["#4A90D9", "#E8724A", "#5CB85C"]

    for i, (model, color) in enumerate(zip(MODELS, model_colors)):
        data = results[results["model"] == model].set_index("channel")
        values = [data.loc[ch, "pct_share"] for ch in CHANNELS]
        bars = ax.bar(x + offsets[i], values, width=width,
                      label=model, color=color, edgecolor="white", linewidth=0.8)

        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{val}%",
                ha="center", va="bottom", fontsize=8, fontweight="bold"
            )

    ax.set_title("Channel Credit Share by Attribution Model",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Channel", fontsize=11)
    ax.set_ylabel("% of Total Attributed Revenue", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(CHANNELS, fontsize=11)
    ax.set_ylim(0, 45)
    ax.legend(title="Model", fontsize=10, title_fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

    plt.tight_layout()
    plt.savefig("charts/chart2_pct_share_grouped.png", dpi=150, bbox_inches="tight")
    print("Saved: charts/chart2_pct_share_grouped.png")


def chart_credit_shift():
    fig, ax = plt.subplots(figsize=(12, 6))

    for channel in CHANNELS:
        values = []
        for model in MODELS:
            val = results[
                (results["model"] == model) &
                (results["channel"] == channel)
            ]["pct_share"].values[0]
            values.append(val)

        ax.plot(MODELS, values, marker="o", linewidth=2.5,
                markersize=8, label=channel,
                color=CHANNEL_COLORS[channel])

        ax.text(
            MODELS[-1], values[-1] + 0.3,
            f"{channel} ({values[-1]}%)",
            fontsize=9, color=CHANNEL_COLORS[channel],
            fontweight="bold"
        )

    ax.set_title("Credit Shift Across Attribution Models by Channel",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Attribution Model", fontsize=11)
    ax.set_ylabel("% Credit Share", fontsize=11)
    ax.set_ylim(0, 45)
    ax.legend(title="Channel", fontsize=9, title_fontsize=10, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

    plt.tight_layout()
    plt.savefig("charts/chart3_credit_shift.png", dpi=150, bbox_inches="tight")
    print("Saved: charts/chart3_credit_shift.png")


if __name__ == "__main__":
    print("Generating charts...")
    chart_revenue_comparison()
    chart_pct_share_grouped()
    chart_credit_shift()
    print("\nAll charts saved to charts/ folder.")