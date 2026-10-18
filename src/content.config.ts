import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
const projects = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/projects' }),
  schema: ({ image }) => z.object({
    title: z.string(), description: z.string(), lead: z.string(), kind: z.enum(['team', 'personal']),
    period: z.string(), role: z.string(), status: z.enum(['completed', 'in-development']),
    order: z.number(), featured: z.boolean(), sources: z.array(z.object({ label: z.string(), url: z.url() })),
    summary: z.object({ problem: z.string(), decision: z.string(), outcome: z.string() }),
    hero: z.object({ src: image(), alt: z.string(), caption: z.string(), sourceUrl: z.url().optional() }).optional(),
  }),
});
export const collections = { projects };
