# Return & Refund Analysis – Findings (Template)

> Replace placeholders with your results after running `python src/analysis.py`.

## Executive Summary
- Overall return rate: <X>%
- Highest-risk categories: <list>
- Highest-risk regions: <list>
- Key drivers: lower seller rating, lower price, category mix

## Key Insights
1. **Category Risk:** Fashion/Footwear exhibit higher return rates due to sizing and expectation mismatch.
2. **Seller Rating:** Every -1 drop in rating increases return odds significantly (see logit coefficients).
3. **Region Logistics:** Regions with weaker last-mile performance show elevated returns.

## Actions
- Enforce minimum seller rating thresholds and training for high-return sellers.
- Standardize size charts & improve PDP content.
- Strengthen packaging and delivery SLAs for top-risk regions.

## Next Steps
- A/B test revised PDP templates.
- Pilot stricter onboarding for new sellers in risky categories.
- Add automated alerts in the dashboard when rates exceed thresholds.