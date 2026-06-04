import csv
from collections import defaultdict


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


campaign_rows = read_csv("data/campaign_performance.csv")
drip_rows = read_csv("data/drip_experiments.csv")
field_rows = read_csv("data/field_marketing_tests.csv")
quality_rows = read_csv("data/data_quality_checks.csv")

campaigns = defaultdict(lambda: {"spend": 0.0, "incremental_rides": 0, "driver_efficiency": []})
for row in campaign_rows:
    key = (row["market"], row["channel"])
    campaigns[key]["spend"] += float(row["spend"])
    campaigns[key]["incremental_rides"] += int(row["incremental_rides"])
    campaigns[key]["driver_efficiency"].append(float(row["incremental_rides_per_100_driver_hours"]))

print("Top campaign ROI opportunities")
ranked_campaigns = []
for (market, channel), values in campaigns.items():
    value = values["incremental_rides"] * 18.5
    roi = (value - values["spend"]) / values["spend"] if values["spend"] else 0
    efficiency = sum(values["driver_efficiency"]) / len(values["driver_efficiency"])
    ranked_campaigns.append((roi, efficiency, market, channel, values))

for rank, (roi, efficiency, market, channel, values) in enumerate(sorted(ranked_campaigns, reverse=True)[:10], start=1):
    print(
        f"{rank}. {market} | {channel}: roi={roi:.2f}x, "
        f"incremental_rides={values['incremental_rides']:,}, "
        f"rides_per_100_driver_hours={efficiency:.2f}"
    )

print("\nTop drip triggers")
for rank, row in enumerate(sorted(drip_rows, key=lambda item: float(item["lift_pct"]), reverse=True)[:8], start=1):
    print(
        f"{rank}. {row['market']} | {row['trigger']}: "
        f"lift={float(row['lift_pct']):.1f}%, incremental_rides={int(row['incremental_rides']):,}"
    )

print("\nField marketing scale candidates")
for rank, row in enumerate(sorted(field_rows, key=lambda item: float(item["roi"]), reverse=True)[:8], start=1):
    print(
        f"{rank}. {row['market']} | {row['placement']}: "
        f"roi={float(row['roi']):.2f}x, scans={int(row['qr_scans']):,}, "
        f"completed_rides={int(row['completed_rides']):,}, note={row['operator_note']}"
    )

print("\nData quality gates")
for row in sorted(quality_rows, key=lambda item: (item["status"] != "Fail", -int(item["failed_records"])))[:8]:
    print(
        f"{row['table_name']} | {row['check_type']}: "
        f"status={row['status']}, failed_records={int(row['failed_records']):,}, fix={row['fix']}"
    )
