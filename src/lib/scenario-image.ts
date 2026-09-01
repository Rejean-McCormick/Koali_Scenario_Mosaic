import { existsSync } from 'node:fs';
import { join } from 'node:path';

const PNG_DIR = join(process.cwd(), 'public', 'scenarios', 'images');
const RESPONSIVE_WIDTHS = [418, 627, 836, 1254] as const;
const DEFAULT_WIDTH = 627;

export const SCENARIO_IMAGE_SIZES = '(min-width: 901px) 292px, (min-width: 721px) 220px, (min-width: 363px) 210px, 58vw';

export function scenarioPngFilename(id: string) {
  const match = id.match(/^SCN-(\d{3})$/);
  if (!match) return null;
  return `SCN-${match[1]}.png`;
}

function candidateFilename(filename: string, width: number) {
  if (width === DEFAULT_WIDTH) return filename;
  return filename.replace(/\.png$/i, `-${width}.png`);
}

export function resolveScenarioPreviewImageSet(id: string, fallback: string) {
  const filename = scenarioPngFilename(id);
  if (!filename || !existsSync(join(PNG_DIR, filename))) {
    return { src: fallback, srcset: undefined, sizes: undefined };
  }

  const src = `/scenarios/images/${filename}`;
  const candidates = RESPONSIVE_WIDTHS
    .map((width) => ({ width, filename: candidateFilename(filename, width) }))
    .filter(({ filename: candidate }) => existsSync(join(PNG_DIR, candidate)));

  const srcset = candidates.length > 1
    ? candidates.map(({ width, filename: candidate }) => `/scenarios/images/${candidate} ${width}w`).join(', ')
    : undefined;

  return {
    src,
    srcset,
    sizes: srcset ? SCENARIO_IMAGE_SIZES : undefined,
  };
}

export function resolveScenarioPreviewImage(id: string, fallback: string) {
  return resolveScenarioPreviewImageSet(id, fallback).src;
}
