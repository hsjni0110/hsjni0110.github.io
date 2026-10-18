import type { APIRoute } from 'astro';
export function getStaticPaths() {
  return process.env.SITE_URL ? [{ params: { metadata: 'robots' } }] : [];
}
export const GET: APIRoute = ({ site }) => {
  const base = import.meta.env.BASE_URL;
  return new Response(`User-agent: *\nAllow: /\nSitemap: ${new URL(`${base.replace(/^\//, '')}sitemap-index.xml`, site).href}\n`, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
