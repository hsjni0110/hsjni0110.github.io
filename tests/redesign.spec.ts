import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';

test('work evidence precedes projects and work links navigate to their cases', async ({ page }) => {
  await page.goto(base);
  expect(await page.locator('#experience').evaluate(el => !!(el.compareDocumentPosition(document.querySelector('#cases')!) & Node.DOCUMENT_POSITION_FOLLOWING))).toBe(true);
  await page.locator('.portrait-work a[href="#speaktext"]').click();
  await expect(page).toHaveURL(/#speaktext$/);
  await expect(page.locator('#speaktext .service-intro')).toBeVisible();
  await expect(page.locator('#speaktext .evidence-links a').first()).toHaveAttribute('href','https://github.com/SpeakText/backend/pull/31');
});

test('actual before and after evidence is keyboard operable without javascript', async ({ browser }) => {
  const context=await browser.newContext({javaScriptEnabled:false});
  const page=await context.newPage();
  await page.goto(base);
  const detail=page.locator('.before-evidence');
  await expect(detail.locator('img')).not.toBeVisible();
  await detail.locator('summary').focus();
  await page.keyboard.press('Enter');
  await expect(detail).toHaveAttribute('open','');
  await expect(detail.getByRole('img')).toBeVisible();
  expect(await detail.getByRole('img').evaluate((el:HTMLImageElement)=>el.complete&&el.naturalWidth>0)).toBe(true);
  await context.close();
});

test('education expands without hiding the core introduction', async ({ page }) => {
  await page.goto(base);
  const credential=page.locator('.credential').filter({hasText:'UC San Diego'});
  await expect(credential.locator('p')).not.toBeVisible();
  await credential.locator('summary').click();
  await expect(credential.locator('p')).toBeVisible();
  await expect(credential.locator('p')).toContainText('준지도학습');
});

test('reduced motion leaves content visible with no running animations', async ({ page }) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto(base);
  await page.locator('#cases').scrollIntoViewIfNeeded();
  await expect(page.locator('#cases-title')).toBeVisible();
  expect(await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length)).toBe(0);
});
