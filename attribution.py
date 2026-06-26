import pandas as pd
import numpy as np

def load_data(path="data/affiliate_journeys_raw.csv"):
    df = pd.read_csv(path)
    converters = df[df["converted"] == 1].copy()
    return df, converters

def last_click(converters):
    last_touch = (
        converters
        .sort_values(["user_id", "touchpoint_order"])
        .groupby("user_id")
        .last()
        .reset_index()
    )
    
    result = (
        last_touch.groupby("channel")["order_value"]
        .sum()
        .reset_index()
        .rename(columns={"order_value": "attributed_revenue"})
    )
    result["model"] = "Last-Click"
    return result

def linear(converters):
    df = converters.copy()
    df["attributed_revenue"] = df["order_value"] / df["total_touchpoints"]
    
    result = (
        df.groupby("channel")["attributed_revenue"]
        .sum()
        .reset_index()
    )
    result["model"] = "Linear"
    return result

def time_decay(converters, half_life_days=7):
    df = converters.copy()
    df["touchpoint_date"] = pd.to_datetime(df["touchpoint_date"])
    df["conversion_date"] = pd.to_datetime(df["conversion_date"])
    
    df["days_before_conv"] = (
        df["conversion_date"] - df["touchpoint_date"]
    ).dt.days
    
    df["weight"] = np.exp(-np.log(2) / half_life_days * df["days_before_conv"])
    
    user_weight_totals = df.groupby("user_id")["weight"].transform("sum")
    df["norm_weight"] = df["weight"] / user_weight_totals
    
    df["attributed_revenue"] = df["norm_weight"] * df["order_value"]
    
    result = (
        df.groupby("channel")["attributed_revenue"]
        .sum()
        .reset_index()
    )
    result["model"] = "Time-Decay"
    return result

def run_all_models(path="data/affiliate_journeys_raw.csv"):
    df, converters = load_data(path)
    
    lc = last_click(converters)
    li = linear(converters)
    td = time_decay(converters)
    
    combined = pd.concat([lc, li, td], ignore_index=True)
    
    combined["pct_share"] = (
        combined.groupby("model")["attributed_revenue"]
        .transform(lambda x: x / x.sum() * 100)
        .round(2)
    )
    
    combined["attributed_revenue"] = combined["attributed_revenue"].round(2)
    return combined, df, converters


if __name__ == "__main__":
    results, df, converters = run_all_models()
    print(results.sort_values(["model", "pct_share"], ascending=[True, False]).to_string(index=False))