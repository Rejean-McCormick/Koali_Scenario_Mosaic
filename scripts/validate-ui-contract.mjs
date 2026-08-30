import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const css = fs.readFileSync(path.join(root, 'src/styles/mosaic.css'), 'utf8');
const previewComponent = fs.readFileSync(path.join(root, 'src/components/ScenarioPreview.astro'), 'utf8');
const mosaicComponent = fs.readFileSync(path.join(root, 'src/components/UsageMosaic.astro'), 'utf8');
const scenarioPage = fs.readFileSync(path.join(root, 'src/pages/uses/[id].astro'), 'utf8');
const offline = fs.readFileSync(path.join(root, 'preview/index.html'), 'utf8');

function assert(condition, message) {
  if (!condition) throw new Error(message);
  console.log(`✓ ${message}`);
}

assert(/\.scenario-preview\s*\{[\s\S]*?height:330px/.test(css), 'Desktop preview reserves a fixed 330px height');
assert(/@media\(max-width:900px\)[\s\S]*?\.scenario-preview\s*\{[\s\S]*?height:392px/.test(css), 'Tablet preview reserves a fixed 392px height');
assert(/@media\(max-width:620px\)[\s\S]*?\.scenario-preview\s*\{[\s\S]*?height:622px/.test(css), 'Mobile preview reserves a fixed 622px height');
assert(css.includes('-webkit-line-clamp:2') && css.includes('-webkit-line-clamp:3'), 'Variable title and summary copy is line-clamped');

for (const marker of [
  'data-preview-profile',
  'data-preview-category-label',
  'data-preview-pattern',
  'data-preview-activities',
  'data-preview-scales',
  'data-preview-context',
  'data-preview-properties',
]) {
  assert(previewComponent.includes(marker), `Astro preview includes ${marker}`);
  assert(offline.includes(marker), `Offline preview includes ${marker}`);
}

for (const technicalLabel of ['Kristal', 'Konnaxion', 'Orgo', 'UCKK']) {
  assert(!previewComponent.includes(technicalLabel), `Public hover does not expose internal label ${technicalLabel}`);
}

assert(mosaicComponent.includes('activities: getPublicActivities(entry.data.palette)'), 'Hover payload exposes public activity indicators');
assert(mosaicComponent.includes('scales,') && mosaicComponent.includes('contexts,') && mosaicComponent.includes('properties,'), 'Hover payload exposes public scale, context, and special-condition metadata');
assert(css.includes('.activity-indicator.is-active'), 'Public activity profile has a visible active state');
assert(css.includes('data-category="CAT-08"'), 'Scenario profile accent supports all category families');
assert(!scenarioPage.includes('scenario-components'), 'Detailed page no longer promotes internal component gauges');
assert(scenarioPage.includes('Special conditions') && scenarioPage.includes('What happens here'), 'Detailed page uses the same public scenario profile language');

const jsonMatch = offline.match(/<script type="application\/json" data-mosaic-data>([\s\S]*?)<\/script>/);
assert(Boolean(jsonMatch), 'Offline preview embeds scenario hover data');
const data = JSON.parse(jsonMatch[1]);
const scenarios = Object.values(data);
assert(scenarios.length === 120, 'Offline hover payload contains all 120 scenarios');
assert(new Set(scenarios.map((s) => s.categoryId)).size === 8, 'Hover indicators cover all 8 public category families');
assert(new Set(scenarios.map((s) => s.pattern)).size === 24, 'Hover indicators cover all 24 public pattern labels');
assert(scenarios.every((s) => Array.isArray(s.palette) && Array.isArray(s.scales) && Array.isArray(s.contexts) && Array.isArray(s.properties) && Array.isArray(s.related)), 'Offline preview preserves public array-valued scenario metadata');
assert(scenarios.every((s) => s.activities && Object.keys(s.activities).length === 7 && Object.values(s.activities).every((v) => typeof v === 'boolean')), 'Every scenario exposes the seven public activity indicators');
assert(new Set(scenarios.map((s) => JSON.stringify(s.activities))).size > 20, 'Public activity profiles vary meaningfully across scenarios');
assert(scenarios.every((s) => s.scales.length >= 1), 'Every scenario has at least one public scale indicator');
assert(scenarios.every((s) => s.contexts.length >= 1), 'Every scenario has at least one public context indicator');

console.log('\nUI contract validation passed.');
