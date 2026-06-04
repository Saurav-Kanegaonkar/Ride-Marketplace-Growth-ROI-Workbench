import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const pageUrl = `file://${path.join(root, "index.html")}`;
const imageDir = path.join(root, "docs", "images");

const shots = [
  ["Market ROI", "market-roi-cockpit.png"],
  ["Drip Lab", "drip-campaign-lab.png"],
  ["Field Planner", "field-marketing-planner.png"],
  ["Memo", "recommendation-memo.png"],
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 980 }, deviceScaleFactor: 1 });
await page.goto(pageUrl);

for (const [tab, filename] of shots) {
  await page.getByRole("button", { name: tab }).click();
  await page.screenshot({ path: path.join(imageDir, filename), fullPage: false });
}

await browser.close();
console.log(`Captured ${shots.length} screenshots in ${imageDir}`);
