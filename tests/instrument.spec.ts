import { test, expect } from '@playwright/test';
const base=process.env.TEST_BASE_PATH||'/';
test('work selector switches the diagram and destination with keyboard', async ({page})=>{
  await page.goto(base);
  await page.locator('#select-batch').focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('#select-voice')).toBeChecked();
  await expect(page.locator('.page-voice')).toBeVisible();
  await expect(page.locator('.page-batch')).not.toBeVisible();
  await expect(page.locator('.page-voice a')).toHaveAttribute('href','#speaktext');
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('.page-record')).toBeVisible();
});
test('selector works without javascript', async ({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false});
  const page=await context.newPage();await page.goto(base);
  await page.locator('label[for="select-record"]').click();
  await expect(page.locator('.page-record')).toBeVisible();
  await page.locator('.page-record a').click();
  await expect(page).toHaveURL(/#forgesync$/);
  await context.close();
});
