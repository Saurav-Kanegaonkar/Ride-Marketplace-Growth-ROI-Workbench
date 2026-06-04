# Data Dictionary

| Dataset | Grain | Key fields |
|---|---|---|
| `data/markets.csv` | Market snapshot | `market`, `stage`, `modeled_weekly_requests`, `available_driver_hours`, `supply_coverage_pct`, `rider_repeat_rate_pct` |
| `data/campaign_performance.csv` | Date x market x channel | `spend`, `incremental_rides`, `incremental_rides_per_100_driver_hours`, `roi`, `channel_group` |
| `data/drip_experiments.csv` | Market x trigger | `open_rate_pct`, `click_rate_pct`, `conversion_rate_pct`, `holdout_conversion_rate_pct`, `lift_pct` |
| `data/field_marketing_tests.csv` | Market x placement | `units`, `qr_scans`, `completed_rides`, `program_cost`, `estimated_value`, `roi` |
| `data/data_quality_checks.csv` | Table x check | `check_type`, `status`, `failed_records`, `business_risk`, `fix` |
| `analysis/outputs/app_payload.json` | UI payload | Pre-aggregated metrics consumed by the static app |
