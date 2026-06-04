# Data Sources

The project uses synthetic but role-realistic operating data for a ride marketplace growth team. The data is not company performance data.

## Generation Method

The generation script uses a fixed random seed and market-level assumptions modeled on public ride marketplace patterns: multi-market expansion, driver supply constraints, rider affordability positioning, favorite or trusted-driver behavior, subscription-style driver economics, and growth programs that combine paid media, lifecycle messaging, referrals, vehicle-exterior advertising, in-vehicle placements, and organic social.

Launch markets are assigned lower supply coverage and higher growth indices. Core markets are assigned larger rider request volume and stronger repeat usage. Campaign ROI is penalized when supply coverage is too low to convert ride requests into completed rides. Drip campaigns include holdout conversion so lift can be discussed honestly. Field marketing includes QR scans, source-tagged ride requests, program costs, and completed rides.

| File | Grain | Rows |
|---|---:|---:|
| `markets.csv` | Market snapshot | 8 |
| `campaign_performance.csv` | Date x market x channel | 8,640 |
| `drip_experiments.csv` | Market x trigger | 40 |
| `field_marketing_tests.csv` | Market x placement | 40 |
| `daily_metrics.csv` | Date x market x campaign metric | 8,640 |
| `data_quality_checks.csv` | Source table x quality check | 20 |

The source tables are shaped so they can be loaded into SQL, a notebook, or a BI layer and defended in an interview.
