import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const stale = [
  'Koali Use Mosaic',
  'KOALI USE MOSAIC',
  'koali-use-mosaic',
  'Koali Usage Mosaic',
  'KOALI_USAGE_MOSAIC',
  'koali-usage-mosaic',
  'UsageMosaic',
];
const binaryExt = new Set(['.png','.jpg','.jpeg','.webp','.gif','.ico','.zip','.pyc']);
const errors = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir,{withFileTypes:true})) {
    if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === '__pycache__') continue;
    if (entry.name === 'validate-name.mjs') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else {
      if (binaryExt.has(path.extname(entry.name).toLowerCase())) continue;
      let text;
      try { text = fs.readFileSync(full,'utf8'); } catch { continue; }
      for (const token of stale) if (text.includes(token)) errors.push(`${path.relative(root,full)} contains stale name: ${token}`);
    }
  }
}
walk(root);

const pkg = JSON.parse(fs.readFileSync(path.join(root,'package.json'),'utf8'));
if (pkg.name !== 'koali-scenario-mosaic') errors.push(`package name is ${pkg.name}`);
if (!fs.existsSync(path.join(root,'src/components/ScenarioMosaic.astro'))) errors.push('ScenarioMosaic.astro missing');
if (fs.existsSync(path.join(root,'src/components/UsageMosaic.astro'))) errors.push('UsageMosaic.astro should not exist');

const required = [
  ['README.md','Koali Scenario Mosaic'],
  ['src/layouts/BaseLayout.astro','Koali Scenario Mosaic'],
  ['src/components/ScenarioPreview.astro','KOALI SCENARIO MOSAIC'],
  ['preview/index.html','KOALI SCENARIO MOSAIC'],
  ['public/mosaic-cover.svg','KOALI SCENARIO MOSAIC'],
];
for (const [file,token] of required) {
  const full=path.join(root,file);
  if (!fs.existsSync(full) || !fs.readFileSync(full,'utf8').includes(token)) errors.push(`${file} missing canonical name ${token}`);
}

if (errors.length) {
  console.error('NAMING VALIDATION FAILED');
  for (const error of errors) console.error(' -',error);
  process.exit(1);
}
console.log('✓ canonical product name: Koali Scenario Mosaic');
console.log('✓ npm package: koali-scenario-mosaic');
console.log('✓ no stale public/product name found');
