const data = window.workbenchData;

const fmtMoney = (value) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);

const fmtNumber = (value) => new Intl.NumberFormat("en-US").format(value);

const node = (tag, className, html) => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (html) element.innerHTML = html;
  return element;
};

const bar = (value, max, label) => {
  const width = Math.max(4, Math.min(100, (value / max) * 100));
  return `<div class="bar" aria-label="${label}"><span style="width:${width}%"></span></div>`;
};

function renderMetrics() {
  document.querySelector("#metrics").replaceChildren(
    ...data.cards.map(([label, value, detail]) =>
      node("article", "metric", `<small>${label}</small><strong>${value}</strong><span>${detail}</span>`)
    )
  );
}

function renderMarkets() {
  const maxGrowth = Math.max(...data.marketRows.map((row) => row.market_growth_index));
  document.querySelector("#marketList").replaceChildren(
    ...data.marketRows.map((row) =>
      node(
        "article",
        "rank-item",
        `<div class="item-head"><strong>${row.market}</strong><span>${row.stage}</span></div>
        <dl>
          <div><dt>Supply</dt><dd>${row.supply_coverage_pct}%</dd></div>
          <div><dt>Repeat</dt><dd>${row.rider_repeat_rate_pct}%</dd></div>
          <div><dt>Cancel</dt><dd>${row.cancellation_rate_pct}%</dd></div>
        </dl>
        ${bar(row.market_growth_index, maxGrowth, "Market growth index")}
        <p>${fmtNumber(row.modeled_weekly_completed_rides)} weekly completed rides from ${fmtNumber(row.active_drivers)} active drivers.</p>`
      )
    )
  );
}

function table(headers, rows) {
  return `<table><thead><tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table>`;
}

function renderCampaigns() {
  const rows = data.campaignRows.slice(0, 12).map(
    (row) =>
      `<tr>
        <td><strong>${row.market}</strong><span>${row.stage}</span></td>
        <td>${row.channel}<span>${row.channel_group}</span></td>
        <td>${fmtMoney(row.spend)}</td>
        <td>${fmtNumber(row.incremental_rides)}</td>
        <td>${row.incremental_rides_per_100_driver_hours}</td>
        <td class="${row.roi >= 0 ? "good" : "watch"}">${row.roi}x</td>
      </tr>`
  );
  document.querySelector("#campaignTable").innerHTML = `
    <h3>Campaign ROI queue</h3>
    ${table(["Market", "Channel", "Spend", "Inc rides", "Rides per 100 hrs", "ROI"], rows)}
  `;
}

function renderDrip() {
  const maxLift = Math.max(...data.dripRows.map((row) => row.lift_pct));
  document.querySelector("#dripGrid").replaceChildren(
    ...data.dripRows.map((row) =>
      node(
        "article",
        "experiment",
        `<div class="item-head"><strong>${row.trigger}</strong><span>${row.market}</span></div>
        <p>${row.cohort} cohort, ${row.deployment_status}</p>
        <dl>
          <div><dt>Lift</dt><dd>${row.lift_pct}%</dd></div>
          <div><dt>Open</dt><dd>${row.open_rate_pct}%</dd></div>
          <div><dt>Click</dt><dd>${row.click_rate_pct}%</dd></div>
          <div><dt>Inc rides</dt><dd>${fmtNumber(row.incremental_rides)}</dd></div>
        </dl>
        ${bar(row.lift_pct, maxLift, "Holdout lift")}`
      )
    )
  );
}

function renderField() {
  const maxRoi = Math.max(...data.fieldRows.map((row) => Math.max(row.roi, 0.1)));
  document.querySelector("#fieldList").replaceChildren(
    ...data.fieldRows.map((row) =>
      node(
        "article",
        "rank-item",
        `<div class="item-head"><strong>${row.placement}</strong><span>${row.market}</span></div>
        <dl>
          <div><dt>ROI</dt><dd class="${row.roi >= 0 ? "good" : "watch"}">${row.roi}x</dd></div>
          <div><dt>Scans</dt><dd>${fmtNumber(row.qr_scans)}</dd></div>
          <div><dt>Rides</dt><dd>${fmtNumber(row.completed_rides)}</dd></div>
        </dl>
        ${bar(Math.max(row.roi, 0.1), maxRoi, "Field ROI")}
        <p>${row.operator_note}. Cost ${fmtMoney(row.program_cost)}, value ${fmtMoney(row.estimated_value)}.</p>`
      )
    )
  );
}

function renderQuality() {
  const rows = data.qualityRows.map(
    (row) =>
      `<tr>
        <td><strong>${row.table_name}</strong><span>${row.expected_grain}</span></td>
        <td>${row.check_type}</td>
        <td class="${row.status === "Fail" ? "bad" : row.status === "Warn" ? "watch" : "good"}">${row.status}</td>
        <td>${fmtNumber(row.failed_records)}</td>
        <td>${row.fix}</td>
      </tr>`
  );
  document.querySelector("#qualityTable").innerHTML = `
    <h3>Data quality gates</h3>
    ${table(["Source", "Check", "Status", "Records", "Fix"], rows)}
  `;
}

function renderMemo() {
  document.querySelector("#memoList").replaceChildren(
    ...data.recommendations.map((rec) =>
      node(
        "article",
        "memo",
        `<span>${rec.priority}</span>
        <h3>${rec.theme}</h3>
        <p><strong>Evidence:</strong> ${rec.evidence}</p>
        <p><strong>Next step:</strong> ${rec.next_step}</p>
        <small>${rec.owner}</small>`
      )
    )
  );
}

function bindTabs() {
  const buttons = [...document.querySelectorAll(".tabs button")];
  const views = [...document.querySelectorAll(".view")];
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("active", item === button));
      views.forEach((view) => view.classList.toggle("active", view.id === `${button.dataset.view}View`));
    });
  });
}

renderMetrics();
renderMarkets();
renderCampaigns();
renderDrip();
renderField();
renderQuality();
renderMemo();
bindTabs();
