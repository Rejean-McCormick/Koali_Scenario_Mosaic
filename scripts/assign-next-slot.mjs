import fs from 'node:fs';
import path from 'node:path';

const id = process.argv[2];
if (!/^SCN-\d{3}$/.test(id ?? '')) {
  console.error('Usage: npm run slot:assign -- SCN-121');
  process.exit(1);
}
const root = process.cwd();
const file = path.join(root, 'src/data/mosaic-layout.json');
const layout = JSON.parse(fs.readFileSync(file, 'utf8'));
if (layout.assignments[id]) {
  console.log(`${id} is already assigned to ${layout.assignments[id]}`);
  process.exit(0);
}
const slot = layout.reservedSlots?.[0];
if (!slot) {
  console.error('No reserved mosaic slots remain. Create a new versioned layout before adding more scenarios.');
  process.exit(1);
}
layout.assignments[id] = slot;
layout.reservedSlots = layout.reservedSlots.slice(1);
fs.writeFileSync(file, JSON.stringify(layout, null, 2) + '\n');
console.log(`Assigned ${id} → ${slot}`);
