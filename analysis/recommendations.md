# Analytical Recommendations

## What Stands Out

- Driver-side supply gaps distort acquisition ROI when rider campaigns are judged without market capacity context.
- Drip campaigns improve retention most when triggered by first-ride completion rather than account creation.
- Vehicle-exterior advertising works best in dense markets, but only after excluding markets with low repeat usage.

## Recommended Operating Moves

- Score every campaign by incremental rides per available driver hour, not only acquisition cost.
- Move inactive riders into behavior-triggered drip sequences after first ride, cancellation, or referral events.
- Shift paid media away from markets where supply saturation blocks conversion into completed rides.

## How I Would Use The Data

1. Start with `daily_metrics.csv` to identify entities with worsening priority scores.
2. Join `source_events.csv` to separate true business movement from freshness or definition issues.
3. Use `stakeholder_requirements.csv` to confirm whether the dashboard is answering a decision, not just visualizing a number.
4. Use `data_quality_checks.csv` to block recommendations where the source is unreliable.
5. Push the final action queue from `recommended_actions.csv` into roadmap or operating review follow-up.
