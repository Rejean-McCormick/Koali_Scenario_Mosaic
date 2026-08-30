import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const componentScore = z.number().int().min(0).max(5);

const scenarios = defineCollection({
  loader: glob({
    pattern: 'SCN-*.md',
    base: './src/content/scenarios',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    id: z.string().regex(/^SCN-\d{3}$/),
    title: z.string().min(8),
    primary_category: z.string().regex(/^CAT-0[1-8]$/),
    pattern_family: z.string().regex(/^PAT-\d{2}$/),
    category_label: z.string().min(2),
    pattern_label: z.string().min(2),
    palette: z.array(z.string()).min(1),
    components: z.object({
      kristal: componentScore,
      konnaxion: componentScore,
      orgo: componentScore,
      uckk: componentScore,
    }),
    preview_summary: z.string().min(100).max(1000),
    preview_image: z.string().startsWith('/'),
    preview_image_alt: z.string().min(12),
    badges: z.array(z.string()).max(8).default([]),
    related: z.array(z.string().regex(/^SCN-\d{3}$/)).max(8).default([]),
    derivation: z.enum(['EXPLICIT','COMPOSED','DERIVED','FUTURE-DESIGN']),
    runtime_evidence: z.enum(['DOCUMENTED','VALIDATED','PARTIALLY-VALIDATED','UNVERIFIED']),
    // Canon/editorial fields used by the full scenario page or corpus tooling.
    entry_trigger: z.string().optional(),
    scales: z.array(z.string()).optional(),
    settings: z.array(z.string()).optional(),
    properties: z.array(z.string()).optional(),
    domains: z.array(z.string()).optional(),
    signature_patterns: z.array(z.string()).optional(),
    canon_refs: z.array(z.string()).optional(),
    transfer_domains: z.array(z.string()).optional(),
    pattern: z.string().optional(),
    continuity_gap: z.string().optional(),
    secondary_components: z.array(z.string()).optional(),
  }),
});

export const collections = { scenarios };
