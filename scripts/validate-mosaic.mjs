import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const dir = path.join(root, 'src/content/scenarios');
const files = fs.readdirSync(dir).filter((x) => /^SCN-\d{3}\.md$/.test(x)).sort();
const layout = JSON.parse(fs.readFileSync(path.join(root, 'src/data/mosaic-layout.json'), 'utf8'));
let failed = false;
const fail = (m) => { failed = true; console.error(`✗ ${m}`); };
const pass = (m) => console.log(`✓ ${m}`);

if (files.length < 120) fail(`Expected at least the baseline 120 scenarios, found ${files.length}`); else pass(`${files.length} scenario files (baseline: 120)`);
const ids = files.map((x) => x.replace(/\.md$/, ''));
if (new Set(ids).size !== ids.length) fail('Scenario IDs are not unique'); else pass('Scenario IDs unique');

const slotIds = Object.keys(layout.slots);
if (slotIds.length !== 150) fail(`Expected 150 committed layout slots, found ${slotIds.length}`); else pass('150 fixed layout slots');

const assigned = layout.assignments;
if (Object.keys(assigned).length !== files.length) fail(`Assignments (${Object.keys(assigned).length}) must equal scenario files (${files.length})`); else pass(`${Object.keys(assigned).length} scenario assignments`);
const assignedSlots = Object.values(assigned);
if (new Set(assignedSlots).size !== assignedSlots.length) fail('Duplicate slot assignment'); else pass('No duplicate slot assignments');

for (const id of ids) if (!assigned[id]) fail(`${id} has no slot`);
for (const [id, slot] of Object.entries(assigned)) {
  if (!ids.includes(id)) fail(`Unknown scenario in layout: ${id}`);
  if (!layout.slots[slot]) fail(`Unknown slot ${slot} for ${id}`);
}

const reserved = layout.reservedSlots ?? [];
if (new Set(reserved).size !== reserved.length) fail('Reserved slots are not unique');
if (reserved.some((slot) => assignedSlots.includes(slot))) fail('A reserved slot is also assigned');
if (reserved.length !== slotIds.length - assignedSlots.length) fail(`Reserved slot count (${reserved.length}) should equal unassigned slot count (${slotIds.length - assignedSlots.length})`); else pass(`${reserved.length} reserved slots available`);

for (const file of files) {
  const text = fs.readFileSync(path.join(dir, file), 'utf8');
  if (!text.includes('runtime_evidence: UNVERIFIED')) fail(`${file} missing runtime_evidence`);
  for (const component of ['kristal', 'konnaxion', 'orgo', 'uckk']) {
    const match = text.match(new RegExp(`\\n  ${component}: ([0-5])(?:\\n|$)`));
    if (!match) fail(`${file} malformed ${component} score`);
  }
}

if (failed) process.exit(1);
console.log('\nMosaic data validation passed.');
