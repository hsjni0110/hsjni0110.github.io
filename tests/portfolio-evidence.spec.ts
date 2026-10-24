import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';
test('work index omits organization names and writing links connect to actual articles', async ({ page }) => {
  await page.goto(base);
  await expect(page.locator('.portrait-work')).not.toContainText(/모플|SpeakText|ForgeSync/);
  await expect(page.locator('#writing article')).toHaveCount(2);
  await expect(page.locator('#writing a[href*="Context-Engineering"]')).toHaveCount(1);
  await expect(page.locator('.experience-row').first().locator('.tech-tags li')).toHaveText(['PostgreSQL','Citus','dbt','SQL']);
  const research=page.locator('.credential').filter({hasText:'UC San Diego'});
  await research.locator('summary').click();
  await expect(research.locator('a')).toHaveAttribute('href','https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12318857');
});
test('agent case explains context and validation with repository evidence', async ({ page }) => {
  await page.goto(`${base}projects/forgesync/#ai-workflow`);
  await expect(page.locator('#ai-workflow')).toBeVisible();
  await expect(page.locator('.prose')).toContainText('RED–GREEN–REFACTOR');
  await expect(page.locator('.prose a[href$="/scripts/verify"]')).toHaveCount(1);
  await expect(page.locator('.prose a[href$="/AGENTS.md"]')).toHaveCount(2);
});
