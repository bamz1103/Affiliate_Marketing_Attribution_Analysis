# Attribution Model Recommendation
**Affiliate Marketing Analytics | June 2026**
**Prepared by: Bamidele Oluwatobi**

---

## Executive Summary
Analysis of 10,000 customer journeys across five affiliate channels reveals that 
attribution model choice significantly impacts how marketing credit is distributed. 
Last-click attribution overrewards Google and Direct while systematically 
undervaluing Facebook and Affiliate1. Based on this analysis, the **Time-Decay 
model** is recommended as the most balanced and business-appropriate attribution 
approach for this channel mix.

---

## What We Analysed
- 10,000 simulated customer journeys across 5 channels: Google, Facebook, 
  Email, Direct, and Affiliate1
- Date range: January 2024 to June 2026
- 2,455 converting users generating a total attributed revenue pool
- Three attribution models compared: Last-Click, Linear, and Time-Decay (7-day half-life)

---

## Key Findings

| Channel    | Last-Click | Linear | Time-Decay |
|------------|------------|--------|------------|
| Google     | 36.16%     | 30.19% | 32.15%     |
| Facebook   | 13.04%     | 25.57% | 21.28%     |
| Email      | 19.62%     | 18.34% | 18.87%     |
| Direct     | 24.14%     | 13.80% | 17.59%     |
| Affiliate1 | 7.04%      | 12.10% | 10.11%     |

**Three findings stand out:**

1. **Last-click dramatically undervalues Facebook and Affiliate1.** Facebook's 
   credit nearly doubles from 13% to 26% under the Linear model, revealing it 
   plays a significant role in introducing customers to the brand at the top of 
   the funnel — work that last-click ignores entirely.

2. **Direct traffic is overrewarded under last-click.** Customers who already 
   know the brand often type the URL directly as their final step before 
   purchasing. Last-click attributes 24% of revenue to Direct — but Direct is 
   rarely the channel that created that awareness in the first place.

3. **Time-Decay produces the most intuitive middle ground.** It acknowledges 
   that the final touch before conversion matters most, while still giving 
   meaningful credit to earlier touchpoints that built awareness and intent.

---

## Recommendation
**Adopt the Time-Decay attribution model as the primary reporting standard.**

Time-Decay is recommended over Last-Click because it avoids punishing upper-funnel 
channels like Facebook and Affiliate1 that generate awareness but rarely close the 
sale. It is recommended over Linear because it still reflects the commercial reality 
that touchpoints closer to conversion carry more persuasive weight.

A 7-day half-life is appropriate for this channel mix given that the average 
customer journey spans 1-14 days. This can be adjusted as more data is collected.

**Budget implication:** Under Time-Decay, Facebook and Affiliate1 collectively 
receive 31% of attributed revenue versus just 20% under Last-Click. A marketing 
team relying on Last-Click would systematically underfund these channels, 
potentially weakening the top of the funnel over time and reducing the volume 
of customers entering the journey entirely.

---

## Limitations
- This analysis is based on simulated data. Real-world journeys may show 
  different channel interaction patterns.
- Time-Decay assumes recency equals intent — this may not always be true. 
  A customer who saw a Facebook ad 30 days ago and thought about it for a 
  month before buying is undervalued by this model.
- None of these models account for view-through attribution (seeing an ad 
  without clicking it), which is particularly relevant for Facebook and 
  display channels.
- The 7-day half-life is an assumption. A/B testing different half-life 
  values against actual revenue outcomes would strengthen this recommendation.

---