-- Illustrative checks for Ride Marketplace Growth ROI Workbench
select signal, owner, risk
from source_events
where risk in ('High', 'Medium');
