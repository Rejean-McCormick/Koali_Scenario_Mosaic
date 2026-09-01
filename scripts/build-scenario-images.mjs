import { mkdir, readdir, rename, rm } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import sharp from 'sharp';

const ROOT = process.cwd();
const SOURCE_DIR = path.join(ROOT, 'src', 'assets', 'scenario-images');
const OUTPUT_DIR = path.join(ROOT, 'public', 'scenarios', 'images');
const SOURCE_SIZE = 1254;
const DEFAULT_SIZE = 627;
const RESPONSIVE_SIZES = [418, 627, 836, 1254];
const FILE_RE = /^SCN-(\d{3})\.png$/;

await mkdir(SOURCE_DIR, { recursive: true });
await mkdir(OUTPUT_DIR, { recursive: true });

const entries = (await readdir(SOURCE_DIR, { withFileTypes: true }))
  .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith('.png'))
  .map((entry) => entry.name)
  .sort();

const errors = [];
const validFiles = [];

for (const name of entries) {
  const match = name.match(FILE_RE);
  if (!match) {
    errors.push(`${name}: expected SCN-001.png … SCN-120.png`);
    continue;
  }
  const number = Number(match[1]);
  if (number < 1 || number > 120) {
    errors.push(`${name}: scenario number must be between 001 and 120`);
    continue;
  }

  const input = path.join(SOURCE_DIR, name);
  try {
    const meta = await sharp(input, { failOn: 'error' }).metadata();
    if (meta.format !== 'png') {
      errors.push(`${name}: source must be PNG`);
      continue;
    }
    if (meta.width !== SOURCE_SIZE || meta.height !== SOURCE_SIZE) {
      errors.push(`${name}: source must be exactly ${SOURCE_SIZE}×${SOURCE_SIZE}, got ${meta.width}×${meta.height}`);
      continue;
    }
    validFiles.push(name);
  } catch (error) {
    errors.push(`${name}: cannot read PNG (${error.message})`);
  }
}

if (errors.length) {
  console.error('SCENARIO IMAGE PREPARATION FAILED');
  for (const error of errors) console.error(` - ${error}`);
  process.exit(1);
}

function outputFilename(name, size) {
  if (size === DEFAULT_SIZE) return name;
  return name.replace(/\.png$/i, `-${size}.png`);
}

async function buildVariant(input, name, size) {
  const output = path.join(OUTPUT_DIR, outputFilename(name, size));
  const temp = `${output}.tmp.png`;

  try {
    await sharp(input, { failOn: 'error' })
      .resize(size, size, {
        fit: 'fill',
        kernel: sharp.kernel.lanczos3,
      })
      .png({
        compressionLevel: 9,
        adaptiveFiltering: true,
      })
      .toFile(temp);

    const meta = await sharp(temp, { failOn: 'error' }).metadata();
    if (meta.width !== size || meta.height !== size) {
      throw new Error(`generated ${meta.width}×${meta.height}, expected ${size}×${size}`);
    }

    await rename(temp, output);
  } catch (error) {
    await rm(temp, { force: true });
    throw new Error(`${name} @ ${size}px: ${error.message}`);
  }
}

async function buildOne(name) {
  const input = path.join(SOURCE_DIR, name);
  await Promise.all(RESPONSIVE_SIZES.map((size) => buildVariant(input, name, size)));
}

const CONCURRENCY = 2;
for (let i = 0; i < validFiles.length; i += CONCURRENCY) {
  await Promise.all(validFiles.slice(i, i + CONCURRENCY).map(buildOne));
}

if (validFiles.length === 0) {
  console.log(`No source PNGs found in ${path.relative(ROOT, SOURCE_DIR)}; keeping existing public images.`);
} else {
  console.log(`✓ ${validFiles.length} scenario image(s): responsive PNG set ${RESPONSIVE_SIZES.join(' / ')} px`);
  console.log(`✓ default src remains ${DEFAULT_SIZE}×${DEFAULT_SIZE} (exact 50% scale)`);
  console.log(`✓ responsive PNGs written to ${path.relative(ROOT, OUTPUT_DIR)}`);
}
