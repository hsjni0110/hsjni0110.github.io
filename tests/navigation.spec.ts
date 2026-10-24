import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';
test('homepage has email and resume links', async ({ page }) => {
  await page.goto(base);
  await expect(page.getByRole('link', { name: '이메일로 연락하기', exact: true }).first()).toHaveAttribute('href', 'mailto:seokjin.han010@gmail.com');
  await expect(page.getByRole('link', { name: '이력서 PDF', exact: true }).first()).toHaveAttribute('href', `${base}resume.pdf`);
});
for (const id of ['speaktext', 'forgesync', 'db-fleet-ops', 'reservation-system']) {
  test(`${id} works by direct navigation and refresh`, async ({ page }) => {
    const response = await page.goto(`${base}projects/${id}/`);
    expect(response?.status()).toBe(200);
    await expect(page.locator('.case-body .prose > h2').last()).toBeVisible();
    await page.reload();
    await expect(page.locator('.case-body .prose > h2').first()).toBeVisible();
    await expect(page.getByRole('link', { name: '전체 사례로 돌아가기' })).toHaveAttribute('href', `${base}#cases`);
  });
}
test('homepage introduces the developer and orders the main cases', async ({ page }) => {
  await page.goto(base);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('한석진입니다.');
  expect(await page.locator('[data-project]').evaluateAll(nodes => nodes.map(n => n.getAttribute('data-project')))).toEqual(['speaktext', 'forgesync']);
});
test('approved PDF, fonts and project images load from the configured base', async ({ page, request }) => {
  const pdf = await request.get(`${base}resume.pdf`);
  expect(pdf.ok()).toBe(true);
  expect((await pdf.body()).subarray(0,5).toString()).toBe('%PDF-');
  await page.goto(base);
  expect(await page.evaluate(async()=>{await document.fonts.load('18px Pretendard');return document.fonts.check('18px Pretendard');})).toBe(true);
  for (const path of ['', 'projects/forgesync/']) {
    await page.goto(`${base}${path}`);
    for (const image of await page.locator('main img:visible').all()) {
      await image.scrollIntoViewIfNeeded();
      await expect(image).toHaveJSProperty('complete', true);
      expect(await image.evaluate((el: HTMLImageElement)=>el.naturalWidth)).toBeGreaterThan(0);
    }
  }
});
test('project figure offers its full size approved image', async ({ page, request }) => {
  await page.goto(`${base}projects/forgesync/`);
  const link=page.getByRole('link',{name:'화면 크게 보기'}).first();
  await expect(link).toBeVisible();
  const url=await link.getAttribute('href');expect(url).toBeTruthy();
  const response=await request.get(url!);expect(response.ok()).toBe(true);expect(response.headers()['content-type']).toContain('image/');
});
