import { access, mkdir, rm, stat } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const PNG_DIR = join(ROOT, 'public', 'scenarios', 'images');
const FALLBACK_DIR = join(ROOT, 'public', 'scenarios', 'placeholders');
const OUT_DIR = join(ROOT, 'public', 'scenarios', 'thumbnails');
const SIZE = 96;

async function exists(path) {
  try {
    await access(path, constants.R_OK);
    return true;
  } catch {
    return false;
  }
}

await rm(OUT_DIR, { recursive: true, force: true });
await mkdir(OUT_DIR, { recursive: true });

let generated = 0;
let bytes = 0;
const missing = [];

for (let n = 1; n <= 120; n += 1) {
  const id = `SCN-${String(n).padStart(3, '0')}`;
  const png = join(PNG_DIR, `${id}.png`);
  const fallback = join(FALLBACK_DIR, `${id}.svg`);
  const source = await exists(png) ? png : await exists(fallback) ? fallback : null;

  if (!source) {
    missing.push(id);
    continue;
  }

  const output = join(OUT_DIR, `${id}.png`);
  await sharp(source)
    .resize(SIZE, SIZE, { fit: 'cover', position: 'centre' })
    .png({ compressionLevel: 9, palette: true, quality: 72, effort: 10 })
    .toFile(output);

  generated += 1;
  bytes += (await stat(output)).size;
}

const kb = (bytes / 1024).toFixed(1);
console.log(`Scenario thumbnails: ${generated}/120 generated at ${SIZE}x${SIZE} (${kb} KiB total).`);
if (missing.length) {
  console.warn(`Missing source images for: ${missing.join(', ')}`);
}
