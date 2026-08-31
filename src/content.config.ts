import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const scenarioText = defineCollection({
  loader: glob({
    pattern: '**/SCN-*.md',
    base: './src/content/scenarios',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    id: z.string().regex(/^SCN-\d{3}$/),
    locale: z.enum(['en', 'fr']),
    title: z.string(),
    category_label: z.string(),
    pattern_label: z.string(),
    pattern: z.string(),
    continuity_gap: z.string(),
    preview_summary: z.string(),
    preview_image_alt: z.string(),
  }),
});

export const collections = { scenarioText };
