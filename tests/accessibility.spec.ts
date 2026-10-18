import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';
test('reading works without javascript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(base);
  await page.locator('[data-project="speaktext"]').getByRole('link', { name: '판단의 과정 읽기' }).click();
  await expect(page.getByRole('heading', { name: '판단', exact: true })).toBeVisible();
  await expect(page.getByRole('link', { name: '이메일로 연락하기', exact: true })).toHaveAttribute('href', 'mailto:seokjin.han010@gmail.com');
  await context.close();
});
test('keyboard reaches content and contact', async ({ page }) => {
  await page.goto(base);
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: '본문 바로가기' })).toBeFocused();
  await page.keyboard.press('Enter');
  for (let i=0;i<8;i++) { if (await page.evaluate(() => document.activeElement?.getAttribute('href') === 'mailto:seokjin.han010@gmail.com')) break; await page.keyboard.press('Tab'); }
  const focused = page.locator(':focus');
  await expect(focused).toHaveAttribute('href', 'mailto:seokjin.han010@gmail.com');
  expect(await focused.evaluate(el => getComputedStyle(el).outlineStyle)).not.toBe('none');
});
for (const width of [360,390,768,1440]) {
  test(`korean content does not overflow at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    for (const path of ['', 'projects/shared-life/', 'projects/forgesync/']) {
      await page.goto(`${base}${path}`);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBe(true);
    }
  });
}
test('reduced motion disables smooth scrolling', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto(base);
  expect(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)).not.toBe('smooth');
});
test('failed images retain context and source links', async ({ page }) => {
  await page.route('**/*.{webp,png,avif}', route=>route.abort());
  await page.goto(`${base}projects/forgesync/`);
  await expect(page.locator('figcaption')).toContainText('기록이 없는 시간');
  await expect(page.locator('figcaption a')).toHaveAttribute('href','https://github.com/hsjni0110/forge-sync');
  await expect(page.getByRole('heading',{name:'한계와 다음 단계',exact:true})).toBeVisible();
});
test('404 offers a working way home', async ({ page }) => {
  await page.goto(`${base}404.html`);
  await page.getByRole('link',{name:'첫 화면으로 돌아가기'}).click();
  await expect(page.locator('[data-project]')).toHaveCount(3);
});
test('two hundred percent zoom keeps text and contact usable', async ({ page }) => {
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(base);
  await page.evaluate(()=>{document.documentElement.style.zoom='2';});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth)).toBe(true);
  await page.locator('#contact').scrollIntoViewIfNeeded();
  await expect(page.locator('#contact').getByRole('link',{name:'이메일로 연락하기',exact:true})).toBeVisible();
});
