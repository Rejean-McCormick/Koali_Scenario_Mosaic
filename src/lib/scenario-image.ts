import { existsSync } from 'node:fs';
import { join } from 'node:path';

const PNG_DIR = join(process.cwd(), 'public', 'scenarios', 'images');
const THUMBNAIL_DIR = join(process.cwd(), 'public', 'scenarios', 'thumbnails');

export function scenarioPngFilename(id: string) {
  const match = id.match(/^SCN-(\d{3})$/);
  if (!match) return null;
  return `SCN-${match[1]}.png`;
}

export function resolveScenarioPreviewImage(id: string, fallback: string) {
  const filename = scenarioPngFilename(id);
  if (!filename) return fallback;

  return existsSync(join(PNG_DIR, filename))
    ? `/scenarios/images/${filename}`
    : fallback;
}

export function resolveScenarioThumbnail(id: string) {
  const filename = scenarioPngFilename(id);
  if (!filename) return null;

  return existsSync(join(THUMBNAIL_DIR, filename))
    ? `/scenarios/thumbnails/${filename}`
    : null;
}
