 # Affiliate Marketing Attribution Analysis

A end-to-end data analytics project comparing three attribution models across 
10,000 simulated customer journeys spanning 5 affiliate marketing channels.

🔗 **[Live App](https://affiliatemarketingattributionanalysis-mlbgvxaxcatrwcizsswaah.streamlit.app/)**

---

## Project Overview

In affiliate marketing, multiple channels touch a customer before they convert. 
The attribution problem asks: which channel deserves credit for the sale?

This project simulates 10,000 customer journeys across 5 channels — Google, 
Facebook, Email, Direct, and Affiliate1 — and compares how three attribution 
models distribute revenue credit differently across those channels.

---

## Attribution Models Compared

| Model | Logic |
|---|---|
| Last-Click | 100% credit to the final touchpoint before conversion |
| Linear | Credit split equally across all touchpoints in the journey |
| Time-Decay | More recent touchpoints receive exponentially more credit (7-day half-life) |

---

## Key Finding

Last-Click attributed **36% of revenue to Google** and only **13% to Facebook**.  
Under Linear attribution, Facebook's share nearly **doubled to 26%**.  
This shows how attribution model choice directly impacts media spend decisions — 
the same data tells a completely different story depending on the model used.

---

## What's Inside

| File | Description |
|---|---|
| `attribution.py` | Last-Click, Linear, and Time-Decay model implementations |
| `charts.py` | Matplotlib bar charts comparing all 3 models |
| `app.py` | Streamlit web app with interactive journey simulator |
| `recommendation.md` | 1-page business recommendation on model selection |
| `data/` | 10,000 simulated customer journeys (Jan 2024 - Jun 2026) |
| `charts/` | Exported PNG comparison charts |

---

## Tech Stack

- Python (Pandas, NumPy, Matplotlib, SciPy)
- Streamlit
- GitHub + Streamlit Cloud

---

## App Features

- **Model Comparison Charts** — visualise how revenue credit shifts across all 3 models
- **Journey Simulator** — build a custom customer journey and see credit allocation in real time
- **Raw Data Explorer** — filter and download the underlying 10,000 journey dataset

---

## Business Recommendation

Based on the analysis, **Time-Decay attribution** is recommended as the most 
balanced model for this channel mix. It acknowledges that final touchpoints 
carry more persuasive weight while still giving meaningful credit to upper-funnel 
channels like Facebook and Affiliate1 that drive awareness but rarely close the sale.

Full recommendation with limitations and next steps in `recommendation.md`.

---

## Author

**Bamidele Oluwatobi** — Data Analyst  
[LinkedIn](https://www.linkedin.com/in/your-linkedin-here) | 
[GitHub](https://github.com/bamz1103)
