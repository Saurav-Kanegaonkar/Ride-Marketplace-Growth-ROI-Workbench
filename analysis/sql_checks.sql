-- Portfolio SQL checks for a ride marketplace growth ROI operating workbench.

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
