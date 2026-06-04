import csv
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
DOC_IMAGES = ROOT / "docs" / "images"

random.seed(42)

MARKETS = [
    ("MKT-DC", "Capital Core", "Core", 1.22, 0.91, 1.12, 0.78, 0.74),
    ("MKT-BAL", "Harbor Commuter", "Core", 1.06, 0.86, 1.04, 0.82, 0.68),
    ("MKT-NYC", "Metro Outer Boroughs", "Scale", 1.18, 0.73, 1.18, 0.69, 0.71),
    ("MKT-MIA", "South Florida Launch", "Launch", 0.92, 0.62, 1.36, 0.73, 0.65),
    ("MKT-HOU", "Gulf Launch", "Launch", 0.84, 0.55, 1.42, 0.61, 0.58),
    ("MKT-DFW", "North Texas Launch", "Launch", 0.81, 0.52, 1.38, 0.64, 0.57),
    ("MKT-ATL", "Southeast Launch", "Launch", 0.78, 0.49, 1.45, 0.58, 0.54),
    ("MKT-GSO", "Triad Local", "Emerging", 0.64, 0.66, 1.02, 0.77, 0.62),
]

CHANNELS = [
    ("paid_search", "Paid search", "Paid media", 1.08, 0.36),
    ("paid_social", "Paid social", "Paid media", 1.18, 0.42),
    ("organic_social", "Organic social", "Organic", 0.46, 0.31),
    ("driver_referral", "Driver referral", "Referral", 0.58, 0.52),
    ("rider_referral", "Rider referral", "Referral", 0.62, 0.47),
    ("vehicle_exterior", "Vehicle exterior ads", "Field marketing", 0.74, 0.39),
    ("in_vehicle", "In-vehicle cards", "Field marketing", 0.42, 0.44),
    ("welcome_drip", "Welcome drip", "Lifecycle", 0.18, 0.55),
    ("winback_drip", "Winback drip", "Lifecycle", 0.16, 0.51),
]

DRIP_PROGRAMS = [
    ("DRIP-FIRST", "First ride completion", "New rider", 0.43, 0.18, 0.30),
    ("DRIP-CANCEL", "Canceled request recovery", "At risk", 0.36, 0.14, 0.26),
    ("DRIP-FAVORITE", "Favorite driver prompt", "Activated", 0.39, 0.16, 0.28),
    ("DRIP-QUIET", "Dormant rider winback", "Dormant", 0.28, 0.09, 0.20),
    ("DRIP-REFERRAL", "Referral nudge", "Advocate", 0.33, 0.12, 0.22),
]

PLACEMENTS = [
    ("FIELD-WRAP", "Vehicle exterior wrap", 1700, 0.012, 0.19),
    ("FIELD-DOOR", "Door decal", 860, 0.009, 0.15),
    ("FIELD-SEAT", "Back-seat card", 420, 0.018, 0.22),
    ("FIELD-QR", "QR receipt card", 300, 0.021, 0.24),
    ("FIELD-AIRPORT", "Airport staging flyer", 1200, 0.011, 0.17),
]

START = date(2026, 2, 1)
DAYS = 120


def ensure_dirs():
    for path in (DATA, OUTPUTS, DOC_IMAGES):
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def money(value):
    return f"${value:,.0f}"


def pct(value):
    return f"{value:.1f}%"


def build_market_rows():
    rows = []
    for market_id, market, stage, demand, supply, growth, retention, trust in MARKETS:
        base_requests = int(1300 * demand * (1.2 if stage == "Core" else 0.78 if stage == "Launch" else 0.48))
        active_drivers = int(280 * supply * (1.15 if stage == "Core" else 0.62 if stage == "Launch" else 0.42))
        completed = int(base_requests * min(0.88, 0.55 + supply * 0.23))
        cancellation_rate = max(6.0, 22.0 - supply * 13 + random.uniform(-1.8, 2.2))
        rider_savings = 15 + trust * 8 + random.uniform(-1.2, 1.5)
        rows.append(
            {
                "market_id": market_id,
                "market": market,
                "stage": stage,
                "modeled_weekly_requests": base_requests,
                "modeled_weekly_completed_rides": completed,
                "available_driver_hours": round(active_drivers * 23.5, 1),
                "active_drivers": active_drivers,
                "rider_repeat_rate_pct": round(100 * retention, 1),
                "supply_coverage_pct": round(100 * min(0.95, supply), 1),
                "cancellation_rate_pct": round(cancellation_rate, 1),
                "avg_rider_savings_pct": round(rider_savings, 1),
                "market_growth_index": round(100 * growth, 1),
                "trust_request_share_pct": round(100 * trust, 1),
            }
        )
    return rows


def build_campaign_rows(market_rows):
    rows = []
    daily_rows = []
    market_lookup = {row["market_id"]: row for row in market_rows}
    for offset in range(DAYS):
        day = START + timedelta(days=offset)
        season = 1 + 0.09 * math.sin(offset / 12)
        for market_id, market, stage, demand, supply, growth, retention, trust in MARKETS:
            market_base = market_lookup[market_id]
            for channel_id, channel, channel_group, spend_factor, intent in CHANNELS:
                if channel_group == "Lifecycle":
                    spend = random.randint(120, 420)
                elif channel_group == "Organic":
                    spend = random.randint(80, 260)
                elif channel_group == "Referral":
                    spend = random.randint(180, 720)
                else:
                    spend = random.randint(650, 2400)
                spend = int(spend * spend_factor * (1.1 if stage == "Launch" else 0.86 if stage == "Core" else 0.64))
                impressions = int(spend * random.uniform(38, 92) * (1.2 if channel_group == "Field marketing" else 1))
                signups = int(impressions * random.uniform(0.006, 0.028) * intent * growth)
                requests = int(signups * random.uniform(0.31, 0.58) * demand)
                supply_penalty = min(1, float(market_base["supply_coverage_pct"]) / 78)
                completed = int(requests * random.uniform(0.62, 0.86) * supply_penalty)
                incremental = max(0, int(completed * random.uniform(0.42, 0.74) * season))
                driver_hours = float(market_base["available_driver_hours"])
                value = incremental * random.uniform(15.5, 22.0)
                roi = (value - spend) / spend if spend else 0
                rows.append(
                    {
                        "date": day.isoformat(),
                        "market_id": market_id,
                        "market": market,
                        "stage": stage,
                        "channel_id": channel_id,
                        "channel": channel,
                        "channel_group": channel_group,
                        "spend": spend,
                        "impressions": impressions,
                        "new_rider_signups": signups,
                        "ride_requests": requests,
                        "completed_rides": completed,
                        "incremental_rides": incremental,
                        "incremental_rides_per_100_driver_hours": round(100 * incremental / driver_hours, 2),
                        "roi": round(roi, 3),
                        "supply_coverage_pct": market_base["supply_coverage_pct"],
                        "rider_repeat_rate_pct": market_base["rider_repeat_rate_pct"],
                    }
                )
                daily_rows.append(
                    {
                        "date": day.isoformat(),
                        "market_id": market_id,
                        "metric_name": f"{channel_id}_roi",
                        "primary_value": round(roi, 3),
                        "comparison_value": round(roi - random.uniform(-0.2, 0.28), 3),
                        "volume": completed,
                        "defect_rate_pct": round(max(0.2, 8 - market_base["supply_coverage_pct"] / 12 + random.random()), 2),
                        "automation_minutes_saved": random.randint(8, 80),
                        "quality_score": random.randint(82, 98),
                        "priority_score": random.randint(35, 95),
                    }
                )
    return rows, daily_rows


def build_drip_rows():
    rows = []
    for market_id, market, stage, demand, supply, growth, retention, trust in MARKETS:
        for program_id, trigger, cohort, open_base, click_base, conv_base in DRIP_PROGRAMS:
            sent = int(random.randint(1800, 9200) * (1.25 if stage == "Core" else 0.72 if stage == "Launch" else 0.45))
            open_rate = min(0.72, open_base + retention * 0.08 + random.uniform(-0.04, 0.05))
            click_rate = min(0.34, click_base + trust * 0.04 + random.uniform(-0.025, 0.025))
            conversion = min(0.46, conv_base + supply * 0.09 + random.uniform(-0.035, 0.035))
            holdout_conversion = max(0.05, conversion - random.uniform(0.035, 0.11))
            lift = (conversion - holdout_conversion) / holdout_conversion
            incremental_rides = int(sent * click_rate * (conversion - holdout_conversion))
            rows.append(
                {
                    "market_id": market_id,
                    "market": market,
                    "program_id": program_id,
                    "trigger": trigger,
                    "cohort": cohort,
                    "messages_sent": sent,
                    "open_rate_pct": round(open_rate * 100, 1),
                    "click_rate_pct": round(click_rate * 100, 1),
                    "conversion_rate_pct": round(conversion * 100, 1),
                    "holdout_conversion_rate_pct": round(holdout_conversion * 100, 1),
                    "lift_pct": round(lift * 100, 1),
                    "incremental_rides": incremental_rides,
                    "estimated_value": int(incremental_rides * random.uniform(9, 15)),
                    "deployment_status": random.choice(["Scale", "Tune copy", "Needs QA", "Pilot"]),
                }
            )
    return rows


def build_field_rows():
    rows = []
    for market_id, market, stage, demand, supply, growth, retention, trust in MARKETS:
        for placement_id, placement, install_cost, scan_rate, request_rate in PLACEMENTS:
            units = random.randint(12, 88) if stage == "Core" else random.randint(5, 44)
            impressions = int(units * random.randint(320, 920) * demand)
            qr_scans = int(impressions * scan_rate * random.uniform(0.7, 1.35))
            requests = int(qr_scans * request_rate * growth)
            completed = int(requests * min(0.86, 0.5 + supply * 0.31))
            cost = int(units * install_cost * random.uniform(0.82, 1.15))
            value = int(completed * random.uniform(95, 170))
            rows.append(
                {
                    "market_id": market_id,
                    "market": market,
                    "placement_id": placement_id,
                    "placement": placement,
                    "units": units,
                    "impressions": impressions,
                    "qr_scans": qr_scans,
                    "ride_requests": requests,
                    "completed_rides": completed,
                    "program_cost": cost,
                    "estimated_value": value,
                    "roi": round((value - cost) / cost, 3),
                    "supply_coverage_pct": round(100 * min(0.95, supply), 1),
                    "operator_note": "Scale" if value > cost and supply > 0.62 else "Hold for driver supply" if supply <= 0.62 else "Refresh creative",
                }
            )
    return rows


def build_quality_rows():
    checks = []
    tables = [
        ("campaign_performance.csv", "daily channel grain", "attribution window"),
        ("drip_experiments.csv", "market x trigger", "holdout assignment"),
        ("field_marketing_tests.csv", "market x placement", "QR source match"),
        ("markets.csv", "market snapshot", "driver hour coverage"),
    ]
    for table, grain, risk in tables:
        for check in ["freshness", "nulls", "duplicate keys", "definition drift", "outlier review"]:
            severity = random.choice(["Low", "Medium", "Medium", "High"])
            failed = random.randint(0, 42) if severity != "High" else random.randint(18, 90)
            checks.append(
                {
                    "check_id": f"CHK-{len(checks) + 1:03d}",
                    "table_name": table,
                    "expected_grain": grain,
                    "check_type": check,
                    "status": "Fail" if failed > 40 else "Warn" if failed > 12 else "Pass",
                    "failed_records": failed,
                    "business_risk": risk,
                    "owner": random.choice(["Analytics", "Growth", "Operations", "Lifecycle"]),
                    "fix": random.choice(
                        [
                            "Reconcile source export",
                            "Add owner attestation",
                            "Backfill missing campaign tag",
                            "Lock metric definition",
                            "Review outlier before publishing",
                        ]
                    ),
                }
            )
    return checks


def rollup_campaigns(rows):
    grouped = {}
    for row in rows:
        key = (row["market"], row["stage"], row["channel"], row["channel_group"])
        bucket = grouped.setdefault(
            key,
            {
                "market": row["market"],
                "stage": row["stage"],
                "channel": row["channel"],
                "channel_group": row["channel_group"],
                "spend": 0,
                "incremental_rides": 0,
                "completed_rides": 0,
                "driver_efficiency_values": [],
                "supply_coverage_pct": row["supply_coverage_pct"],
                "rider_repeat_rate_pct": row["rider_repeat_rate_pct"],
            },
        )
        bucket["spend"] += int(row["spend"])
        bucket["incremental_rides"] += int(row["incremental_rides"])
        bucket["completed_rides"] += int(row["completed_rides"])
        bucket["driver_efficiency_values"].append(float(row["incremental_rides_per_100_driver_hours"]))
    rollup = []
    for bucket in grouped.values():
        value = bucket["incremental_rides"] * 18.5
        bucket["roi"] = round((value - bucket["spend"]) / bucket["spend"], 2)
        bucket["incremental_rides_per_100_driver_hours"] = round(
            sum(bucket["driver_efficiency_values"]) / len(bucket["driver_efficiency_values"]), 2
        )
        bucket.pop("driver_efficiency_values")
        rollup.append(bucket)
    return sorted(
        rollup,
        key=lambda row: (row["roi"], row["incremental_rides_per_100_driver_hours"]),
        reverse=True,
    )


def build_recommendations(campaign_rollup, drip_rows, field_rows):
    top_campaign = next(row for row in campaign_rollup if row["roi"] > 0 and row["supply_coverage_pct"] >= 65)
    constrained = sorted(
        [row for row in campaign_rollup if row["supply_coverage_pct"] < 62 and row["spend"] > 30000],
        key=lambda row: row["spend"],
        reverse=True,
    )[0]
    top_drip = sorted(drip_rows, key=lambda row: (row["lift_pct"], row["incremental_rides"]), reverse=True)[0]
    top_field = sorted(field_rows, key=lambda row: row["roi"], reverse=True)[0]
    return [
        {
            "priority": "P0",
            "theme": "Shift budget to supply-cleared acquisition",
            "evidence": f"{top_campaign['channel']} in {top_campaign['market']} is modeled at {top_campaign['roi']}x ROI with {top_campaign['incremental_rides_per_100_driver_hours']} incremental rides per 100 driver hours.",
            "next_step": "Move one week of low-efficiency paid spend into this market and review completed rides per available driver hour.",
            "owner": "Growth analytics",
        },
        {
            "priority": "P0",
            "theme": "Do not scale paid media where supply blocks conversion",
            "evidence": f"{constrained['market']} has {constrained['supply_coverage_pct']}% supply coverage while {constrained['channel']} still consumed {money(constrained['spend'])}.",
            "next_step": "Hold acquisition spend until driver activation, ride acceptance, and wait-time guardrails clear.",
            "owner": "Marketplace operations",
        },
        {
            "priority": "P1",
            "theme": "Scale the highest-lift drip trigger",
            "evidence": f"{top_drip['trigger']} produced {pct(top_drip['lift_pct'])} lift and {top_drip['incremental_rides']} incremental rides in the modeled holdout design.",
            "next_step": "Ship the copy variant with market-specific wait-time language and keep the holdout cell active.",
            "owner": "Lifecycle marketing",
        },
        {
            "priority": "P1",
            "theme": "Use field marketing where conversion is visible",
            "evidence": f"{top_field['placement']} in {top_field['market']} has {top_field['qr_scans']:,} modeled scans and {top_field['roi']}x ROI.",
            "next_step": "Refresh QR source tags weekly and pair each placement with a driver referral code.",
            "owner": "Field operations",
        },
    ]


def build_payload(market_rows, campaign_rollup, drip_rows, field_rows, quality_rows, recommendations):
    total_spend = sum(row["spend"] for row in campaign_rollup)
    incremental_rides = sum(row["incremental_rides"] for row in campaign_rollup)
    modeled_value = incremental_rides * 18.5
    blended_roi = (modeled_value - total_spend) / total_spend
    supply_clear = [row for row in market_rows if row["supply_coverage_pct"] >= 65]
    best_drip = sorted(drip_rows, key=lambda row: (row["lift_pct"], row["incremental_rides"]), reverse=True)[0]
    field_scale = [row for row in field_rows if row["operator_note"] == "Scale"]
    quality_fails = sum(1 for row in quality_rows if row["status"] == "Fail")
    return {
        "summary": {
            "blended_roi": round(blended_roi, 2),
            "incremental_rides": incremental_rides,
            "supply_clear_markets": len(supply_clear),
            "best_drip_trigger": best_drip["trigger"],
            "best_drip_lift_pct": best_drip["lift_pct"],
            "field_scale_count": len(field_scale),
            "quality_fails": quality_fails,
        },
        "cards": [
            ["Blended growth ROI", f"{round(blended_roi, 2)}x", f"{incremental_rides:,} incremental rides"],
            ["Supply-cleared markets", str(len(supply_clear)), "safe to scale acquisition"],
            ["Top drip lift", pct(best_drip["lift_pct"]), best_drip["trigger"]],
            ["Field placements ready", str(len(field_scale)), "programs above hurdle"],
        ],
        "marketRows": sorted(market_rows, key=lambda row: row["market_growth_index"], reverse=True),
        "campaignRows": campaign_rollup[:24],
        "dripRows": sorted(drip_rows, key=lambda row: row["lift_pct"], reverse=True)[:18],
        "fieldRows": sorted(field_rows, key=lambda row: row["roi"], reverse=True)[:18],
        "qualityRows": sorted(quality_rows, key=lambda row: (row["status"] != "Fail", -row["failed_records"]))[:10],
        "recommendations": recommendations,
    }


def write_data_js(payload):
    path = ROOT / "src" / "data.js"
    path.write_text("window.workbenchData = " + json.dumps(payload, indent=2) + ";\n")


def write_analysis_docs(payload, recommendations):
    (ROOT / "analysis" / "analysis_plan.md").write_text(
        """# Analysis Plan

1. Segment markets by supply coverage, rider demand, repeat usage, and growth stage.
2. Score acquisition and lifecycle campaigns by incremental rides, ROI, and incremental rides per available driver hour.
3. Separate paid media decisions from driver-side marketplace constraints so spend is not scaled where supply cannot convert requests into completed rides.
4. Evaluate drip campaigns with holdout conversion, lift, and triggered cohort behavior.
5. Prioritize vehicle-exterior and in-vehicle programs only where source-tagged scans and completed rides exceed the operating hurdle.
"""
    )
    finding_lines = [
        "# Executive Findings",
        "",
        f"- Blended modeled growth ROI is {payload['summary']['blended_roi']}x across {payload['summary']['incremental_rides']:,} incremental rides.",
        f"- {payload['summary']['supply_clear_markets']} markets clear the supply hurdle for acquisition scaling.",
        f"- The strongest lifecycle trigger is {payload['summary']['best_drip_trigger']} at {pct(payload['summary']['best_drip_lift_pct'])} modeled lift.",
        f"- {payload['summary']['field_scale_count']} field placements clear the scale hurdle after matching QR source tags to completed rides.",
        "",
        "## Recommendations",
        "",
    ]
    finding_lines.extend([f"- {rec['theme']}: {rec['next_step']}" for rec in recommendations])
    (ROOT / "analysis" / "executive_findings.md").write_text("\n".join(finding_lines) + "\n")
    (ROOT / "analysis" / "recommendations.md").write_text(
        "# Recommendation Memo\n\n"
        + "\n".join(
            [
                f"## {rec['priority']} {rec['theme']}\n\nEvidence: {rec['evidence']}\n\nNext step: {rec['next_step']}\n\nOwner: {rec['owner']}\n"
                for rec in recommendations
            ]
        )
    )
    (ROOT / "analysis" / "data_profile.md").write_text(
        """# Data Profile

The source tables are synthetic, role-realistic operating data for a ride marketplace growth team.

| Table | Grain | What it supports |
|---|---|---|
| `markets.csv` | Market snapshot | Supply coverage, repeat usage, demand, and growth-stage segmentation |
| `campaign_performance.csv` | Date x market x channel | Paid, organic, referral, field, and lifecycle ROI analysis |
| `drip_experiments.csv` | Market x trigger | Open rate, click rate, holdout conversion, lift, and incremental rides |
| `field_marketing_tests.csv` | Market x placement | Vehicle exterior, in-vehicle, airport, and QR placement ROI |
| `data_quality_checks.csv` | Table x check | Freshness, grain, definition drift, null, duplicate, and outlier review |

The generated data intentionally includes supply-constrained launch markets, mature core markets, high-intent lifecycle cohorts, and source-tagged field placements so the workbench can support operating recommendations.
"""
    )


def write_sql_checks():
    (ROOT / "analysis" / "sql_checks.sql").write_text(
        """-- Portfolio SQL checks for a ride marketplace growth ROI operating workbench.

-- 1. Campaign ROI by market and channel.
SELECT
  market,
  channel,
  SUM(spend) AS spend,
  SUM(incremental_rides) AS incremental_rides,
  ROUND((SUM(incremental_rides) * 11.5 - SUM(spend)) / NULLIF(SUM(spend), 0), 2) AS roi
FROM campaign_performance
GROUP BY market, channel
ORDER BY roi DESC;

-- 2. Supply guardrail before paid media scale.
SELECT
  c.market,
  c.channel,
  SUM(c.spend) AS spend,
  AVG(c.supply_coverage_pct) AS avg_supply_coverage_pct,
  SUM(c.incremental_rides) AS incremental_rides
FROM campaign_performance c
GROUP BY c.market, c.channel
HAVING AVG(c.supply_coverage_pct) < 65 AND SUM(c.spend) > 30000
ORDER BY spend DESC;

-- 3. Drip campaign holdout lift.
SELECT
  trigger,
  cohort,
  AVG(lift_pct) AS avg_lift_pct,
  SUM(incremental_rides) AS incremental_rides
FROM drip_experiments
GROUP BY trigger, cohort
ORDER BY avg_lift_pct DESC;

-- 4. Field marketing source-tag ROI.
SELECT
  market,
  placement,
  SUM(qr_scans) AS qr_scans,
  SUM(completed_rides) AS completed_rides,
  ROUND((SUM(estimated_value) - SUM(program_cost)) / NULLIF(SUM(program_cost), 0), 2) AS roi
FROM field_marketing_tests
GROUP BY market, placement
ORDER BY roi DESC;
"""
    )


def write_data_readme():
    (DATA / "README.md").write_text(
        """# Data Sources

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
"""
    )


def write_dictionary():
    (ROOT / "data_dictionary.md").write_text(
        """# Data Dictionary

| Dataset | Grain | Key fields |
|---|---|---|
| `data/markets.csv` | Market snapshot | `market`, `stage`, `modeled_weekly_requests`, `available_driver_hours`, `supply_coverage_pct`, `rider_repeat_rate_pct` |
| `data/campaign_performance.csv` | Date x market x channel | `spend`, `incremental_rides`, `incremental_rides_per_100_driver_hours`, `roi`, `channel_group` |
| `data/drip_experiments.csv` | Market x trigger | `open_rate_pct`, `click_rate_pct`, `conversion_rate_pct`, `holdout_conversion_rate_pct`, `lift_pct` |
| `data/field_marketing_tests.csv` | Market x placement | `units`, `qr_scans`, `completed_rides`, `program_cost`, `estimated_value`, `roi` |
| `data/data_quality_checks.csv` | Table x check | `check_type`, `status`, `failed_records`, `business_risk`, `fix` |
| `analysis/outputs/app_payload.json` | UI payload | Pre-aggregated metrics consumed by the static app |
"""
    )


def main():
    ensure_dirs()
    market_rows = build_market_rows()
    campaign_rows, daily_rows = build_campaign_rows(market_rows)
    drip_rows = build_drip_rows()
    field_rows = build_field_rows()
    quality_rows = build_quality_rows()
    campaign_rollup = rollup_campaigns(campaign_rows)
    recommendations = build_recommendations(campaign_rollup, drip_rows, field_rows)
    payload = build_payload(market_rows, campaign_rollup, drip_rows, field_rows, quality_rows, recommendations)

    write_csv(DATA / "markets.csv", market_rows, list(market_rows[0].keys()))
    write_csv(DATA / "campaign_performance.csv", campaign_rows, list(campaign_rows[0].keys()))
    write_csv(DATA / "daily_metrics.csv", daily_rows, list(daily_rows[0].keys()))
    write_csv(DATA / "drip_experiments.csv", drip_rows, list(drip_rows[0].keys()))
    write_csv(DATA / "field_marketing_tests.csv", field_rows, list(field_rows[0].keys()))
    write_csv(DATA / "data_quality_checks.csv", quality_rows, list(quality_rows[0].keys()))
    write_csv(OUTPUTS / "campaign_roi_queue.csv", campaign_rollup, list(campaign_rollup[0].keys()))
    write_csv(OUTPUTS / "drip_lift_queue.csv", payload["dripRows"], list(payload["dripRows"][0].keys()))
    write_csv(OUTPUTS / "field_marketing_queue.csv", payload["fieldRows"], list(payload["fieldRows"][0].keys()))

    (OUTPUTS / "app_payload.json").write_text(json.dumps(payload, indent=2) + "\n")
    (OUTPUTS / "summary.json").write_text(json.dumps(payload["summary"], indent=2) + "\n")
    write_data_js(payload)
    write_analysis_docs(payload, recommendations)
    write_sql_checks()
    write_data_readme()
    write_dictionary()
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
