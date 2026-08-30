import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const scenarios = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './src/content/scenarios' }),
  schema: ({ image }) => z.object({
    id: z.string().regex(/^SCN-\d{3}$/),
    title: z.string().min(10),
    preview_summary: z.string().min(80).max(500),
    preview_image: image(),
    preview_image_alt: z.string().min(8),
    palette: z.array(z.string()).min(1).max(6),
    components: z.object({
      kristal: z.number().int().min(0).max(5),
      konnaxion: z.number().int().min(0).max(5),
      orgo: z.number().int().min(0).max(5),
      uckk: z.number().int().min(0).max(5),
    }),
    badges: z.array(z.string()).max(6).default([]),
    related: z.array(z.string()).max(8).default([]),
    hero: z.boolean().default(false),
  }),
});

export const collections = { scenarios };
