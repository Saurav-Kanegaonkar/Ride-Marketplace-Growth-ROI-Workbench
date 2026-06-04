# Data Profile

The source tables are synthetic, role-realistic operating data for a ride marketplace growth team.

| Table | Grain | What it supports |
|---|---|---|
| `markets.csv` | Market snapshot | Supply coverage, repeat usage, demand, and growth-stage segmentation |
| `campaign_performance.csv` | Date x market x channel | Paid, organic, referral, field, and lifecycle ROI analysis |
| `drip_experiments.csv` | Market x trigger | Open rate, click rate, holdout conversion, lift, and incremental rides |
| `field_marketing_tests.csv` | Market x placement | Vehicle exterior, in-vehicle, airport, and QR placement ROI |
| `data_quality_checks.csv` | Table x check | Freshness, grain, definition drift, null, duplicate, and outlier review |

The generated data intentionally includes supply-constrained launch markets, mature core markets, high-intent lifecycle cohorts, and source-tagged field placements so the workbench can support operating recommendations.
