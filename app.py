import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from attribution import run_all_models

# ── Page config ──────────────────────────────────────
st.set_page_config(
    page_title="Affiliate Attribution Analysis",
    page_icon="📊",
    layout="wide"
)

# ── Load data ──────────────────────────────────────
@st.cache_data
def load_results():
    results, df, converters = run_all_models()
    return results, df, converters

results, df, converters = load_results()

CHANNEL_COLORS = {
    "Google":     "#4285F4",
    "Facebook":   "#1877F2",
    "Email":      "#34A853",
    "Direct":     "#FBBC05",
    "Affiliate1": "#EA4335"
}

MODELS = ["Last-Click", "Linear", "Time-Decay"]
CHANNELS = ["Google", "Facebook", "Email", "Direct", "Affiliate1"]

# ── Header ──────────────────────────────────────
st.title("📊 Affiliate Marketing Attribution Analysis")
st.markdown("Compare how **Last-Click**, **Linear**, and **Time-Decay** models distribute credit across 5 marketing channels.")

st.divider()

# ── Top metrics ──────────────────────────────────────
total_users = df["user_id"].nunique()
total_converters = converters["user_id"].nunique()
conversion_rate = total_converters / total_users * 100
total_revenue = converters.drop_duplicates("user_id")["order_value"].sum()
avg_order_value = converters.drop_duplicates("user_id")["order_value"].mean()
avg_touchpoints = df[df["converted"] == 1].groupby("user_id")["touchpoint_order"].max().mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Conversions", f"{total_converters:,}")
col3.metric("Conversion Rate", f"{conversion_rate:.1f}%")
col4.metric("Total Revenue", f"£{total_revenue:,.0f}")
col5.metric("Avg Order Value", f"£{avg_order_value:,.2f}")

st.divider()

# ── Section 1: Model Comparison Charts ──────────────────────────────────────
st.subheader("📈 Attribution Model Comparison")

tab1, tab2, tab3 = st.tabs(["Revenue by Channel", "% Credit Share", "Credit Shift"])

with tab1:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    fig.suptitle("Attributed Revenue by Channel Across 3 Models",
                 fontsize=16, fontweight="bold", y=1.02)

    for ax, model in zip(axes, MODELS):
        data = results[results["model"] == model].sort_values(
            "attributed_revenue", ascending=False)
        colors = [CHANNEL_COLORS[ch] for ch in data["channel"]]
        bars = ax.bar(data["channel"], data["attributed_revenue"],
                      color=colors, edgecolor="white", linewidth=0.8)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 500,
                    f"£{height:,.0f}", ha="center", va="bottom",
                    fontsize=9, fontweight="bold")

        ax.set_title(model, fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("Channel", fontsize=10)
        ax.set_ylabel("Attributed Revenue (£)", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
        ax.tick_params(axis="x", rotation=15)
        ax.set_ylim(0, results["attributed_revenue"].max() * 1.15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab2:
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
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{val}%", ha="center", va="bottom",
                    fontsize=8, fontweight="bold")

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
    st.pyplot(fig)
    plt.close()

with tab3:
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

        ax.text(MODELS[-1], values[-1] + 0.3,
                f"{channel} ({values[-1]}%)",
                fontsize=9, color=CHANNEL_COLORS[channel],
                fontweight="bold")

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
    st.pyplot(fig)
    plt.close()

st.divider()

# ── Section 2: Interactive Journey Simulator ──────────────────────────────────────
st.subheader("🧪 Journey Simulator")
st.markdown("Build a custom customer journey and see how each attribution model assigns credit.")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("**Build your journey**")
    
    order_value = st.number_input("Order Value (£)", min_value=5.0, 
                                   max_value=5000.0, value=100.0, step=5.0)
    
    num_touchpoints = st.slider("Number of Touchpoints", 
                                 min_value=1, max_value=8, value=3)
    
    journey = []
    for i in range(num_touchpoints):
        col_ch, col_days = st.columns(2)
        with col_ch:
            ch = st.selectbox(f"Touch {i+1} Channel", CHANNELS, key=f"ch_{i}")
        with col_days:
            days = st.number_input(f"Days before conversion", 
                                    min_value=0, max_value=90, 
                                    value=max(0, (num_touchpoints - i - 1) * 7),
                                    key=f"days_{i}")
        journey.append({"channel": ch, "days_before_conv": days})

with col_right:
    st.markdown("**Credit allocation by model**")

    # ── Last-Click ──
    lc_credits = {ch: 0.0 for ch in CHANNELS}
    lc_credits[journey[-1]["channel"]] = order_value

    # ── Linear ──
    li_credits = {ch: 0.0 for ch in CHANNELS}
    for touch in journey:
        li_credits[touch["channel"]] += order_value / len(journey)

    # ── Time-Decay ──
    half_life = 7
    weights = [np.exp(-np.log(2) / half_life * t["days_before_conv"]) for t in journey]
    total_weight = sum(weights)
    td_credits = {ch: 0.0 for ch in CHANNELS}
    for touch, w in zip(journey, weights):
        td_credits[touch["channel"]] += (w / total_weight) * order_value

    # ── Display results ──
    model_credits = {
        "Last-Click": lc_credits,
        "Linear": li_credits,
        "Time-Decay": td_credits
    }

    for model, credits in model_credits.items():
        st.markdown(f"**{model}**")
        active = {ch: v for ch, v in credits.items() if v > 0}
        
        fig, ax = plt.subplots(figsize=(8, 1.5))
        bars = ax.barh(list(active.keys()), list(active.values()),
                       color=[CHANNEL_COLORS[ch] for ch in active.keys()],
                       edgecolor="white")
        
        for bar, val in zip(bars, active.values()):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                    f"£{val:.2f}", va="center", fontsize=9, fontweight="bold")
        
        ax.set_xlim(0, order_value * 1.2)
        ax.set_xlabel("£ Credit", fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

st.divider()

# ── Section 3: Raw Data Explorer ──────────────────────────────────────
st.subheader("🔍 Raw Data Explorer")
st.markdown("Explore the underlying dataset of 10,000 customer journeys.")

col1, col2, col3 = st.columns(3)

with col1:
    selected_channel = st.multiselect(
        "Filter by Channel",
        options=CHANNELS,
        default=CHANNELS
    )

with col2:
    selected_converted = st.selectbox(
        "Filter by Conversion",
        options=["All", "Converted", "Not Converted"]
    )

with col3:
    selected_device = st.multiselect(
        "Filter by Device",
        options=["Mobile", "Desktop", "Tablet"],
        default=["Mobile", "Desktop", "Tablet"]
    )

# Apply filters
filtered_df = df[
    (df["channel"].isin(selected_channel)) &
    (df["device"].isin(selected_device))
]

if selected_converted == "Converted":
    filtered_df = filtered_df[filtered_df["converted"] == 1]
elif selected_converted == "Not Converted":
    filtered_df = filtered_df[filtered_df["converted"] == 0]

st.markdown(f"Showing **{len(filtered_df):,}** rows")
st.dataframe(filtered_df, use_container_width=True, height=400)

# ── Download button ──────────────────────────────────────
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_journeys.csv",
    mime="text/csv"
)