import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { resolve, dirname, relative, extname, join } from 'node:path';
import { createHash } from 'node:crypto';

const root = resolve('dist');
const base = process.env.BASE_PATH || '/';
async function files(dir) {
  return (await Promise.all((await readdir(dir,{withFileTypes:true})).map(x=>x.isDirectory()?files(join(dir,x.name)):join(dir,x.name)))).flat();
}
const all = await files(root);
const pages = all.filter(p=>p.endsWith('.html'));
const exists = new Set(all);
for (const path of ['index.html','404.html','resume.pdf', ...['speaktext','forgesync','db-fleet-ops','reservation-system'].map(x=>`projects/${x}/index.html`)]) {
  assert(exists.has(resolve(root,path)),`Missing output: ${path}`);
}
const allowed = new Set(['.html','.css','.js','.svg','.webp','.png','.jpg','.avif','.woff2','.txt','.xml','.pdf']);
for (const file of all) {
  const name=relative(root,file);
  assert(allowed.has(extname(file)),`Unexpected file type: ${name}`);
  assert(!/^(docs|tmp|output)\//.test(name),`Private directory emitted: ${name}`);
  assert(extname(file)!=='.pdf'||name==='resume.pdf',`Unapproved PDF: ${name}`);
}
const hash = data=>createHash('sha256').update(data).digest('hex');
assert.equal(hash(await readFile(join(root,'resume.pdf'))),hash(await readFile('output/pdf/han-seokjin-resume.pdf')),'Resume differs from approved PDF');
const htmls = new Map(await Promise.all(pages.map(async p=>[p,await readFile(p,'utf8')])));
const ids = html=>new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]));
let references=0;
for (const [file,html] of htmls) {
  assert(html.includes('lang="ko"'),`Missing Korean language: ${file}`);
  assert.equal((html.match(/<h1(?:\s|>)/g)||[]).length,1,`Expected one h1: ${file}`);
  assert(!/\/Users\/|\/private\/|취업\/|주민번호|희망연봉|최종연봉|계좌정보/.test(html),`Private source text in ${file}`);
  const refs = [...html.matchAll(/\b(?:href|src)="([^"]+)"/g)].map(m=>m[1]);
  for (const m of html.matchAll(/\bsrcset="([^"]+)"/g)) refs.push(...m[1].split(',').map(x=>x.trim().split(/\s+/)[0]));
  for (const ref of refs) {
    const raw=ref.replaceAll('&amp;','&');
    if (/^(?:https?:|mailto:|data:|tel:|\/\/)/.test(raw)) continue;
    const url=new URL(raw,`https://local.invalid${base}${relative(root,file).replace(/index\.html$/,'')}`);
    assert(url.pathname.startsWith(base),`Reference escapes base: ${raw} in ${file}`);
    const pathname=decodeURIComponent(url.pathname.slice(base.length));
    let target=resolve(root,pathname||'index.html');
    if(url.pathname.endsWith('/')) target=resolve(root,pathname,'index.html');
    if(!exists.has(target)) {
      const candidate=join(target,'index.html');
      assert(exists.has(candidate),`Broken local reference: ${raw} in ${relative(root,file)}`);
      target=candidate;
    }
    if(url.hash&&htmls.has(target)) assert(ids(htmls.get(target)).has(decodeURIComponent(url.hash.slice(1))),`Missing anchor ${raw}`);
    references++;
  }
}
// CSS is emitted under _astro; resolve each local font/image URL from its actual stylesheet.
for (const file of all.filter(p=>p.endsWith('.css'))) {
  const css=await readFile(file,'utf8');
  for(const m of css.matchAll(/url\(["']?([^\s)"']+)["']?\)/g)) {
    if(/^(data:|https?:)/.test(m[1]))continue;
    const target=m[1].startsWith('/')?resolve(root,m[1].slice(base.length)):resolve(dirname(file),m[1]);
    assert(exists.has(target),`Missing CSS asset ${m[1]}`);
  }
}
assert(!process.env.SITE_URL || URL.canParse(process.env.SITE_URL));
if(process.env.SITE_URL) {
  assert(exists.has(join(root,'robots.txt')),'Missing robots.txt');
  assert(exists.has(join(root,'sitemap-index.xml')),'Missing sitemap');
  for(const [file,html] of htmls)assert(html.includes('rel="canonical"'),`Missing canonical ${file}`);
} else {
  assert(!exists.has(join(root,'robots.txt')),'Local preview should not emit robots');
  assert(!exists.has(join(root,'sitemap-index.xml')),'Local preview should not emit sitemap');
  for(const html of htmls.values())assert(!html.includes('rel="canonical"'),'Local preview should not invent canonical');
}
assert(!exists.has(join(root,'projects/shared-life/index.html')),'Withdrawn project emitted');
for(const html of htmls.values()) {
  assert(!/shared-life|동시생활|끝났다|제 작업은 이런 질문|함께 일하는 사람으로서/.test(html),'Withdrawn copy emitted');
  assert(!/>\s*작업 기록\s*</.test(html),'Unnecessary label emitted');
  assert(!/https:\/\/github\.com\/[^\"\s]+\/pull\//.test(html),'PR link emitted');
}
console.log(`Output checked: ${pages.length} pages, ${references} local references, approved PDF hash, asset types and public-content boundaries.`);
