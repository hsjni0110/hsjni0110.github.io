import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
const site = process.env.SITE_URL;
if (site && (!URL.canParse(site) || new URL(site).protocol !== 'https:' || new URL(site).pathname !== '/')) throw new Error('SITE_URL must be an HTTPS origin without a path');
const base = process.env.BASE_PATH || '/';
if (!/^\/(?:[a-zA-Z0-9_-]+\/)*$/.test(base)) throw new Error('BASE_PATH must start and end with /');
export default defineConfig({ output: 'static', devToolbar: { enabled: false }, trailingSlash: 'always', site, base, integrations: site ? [sitemap()] : [], vite: { build: { sourcemap: false } } });
