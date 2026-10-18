import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';
test('shared-life has no product image or recruitment link', async ({ page }) => {
  await page.goto(`${base}projects/shared-life/`);
  await expect(page.locator('article img')).toHaveCount(0);
  await expect(page.locator('article a[href*="open.kakao"]')).toHaveCount(0);
  await expect(page.locator('article')).toContainText('변경 버전은 아직 사용자 검증 전입니다.');
});
test('case outcomes retain their scope', async ({ page }) => {
  await page.goto(`${base}projects/speaktext/`);
  await expect(page.locator('article')).toContainText('팀 내부 사용의 정성적 피드백');
  await page.goto(`${base}projects/forgesync/`);
  await expect(page.locator('article')).toContainText('탐지 정확도가 개선됐다고 단정할 수는 없습니다');
  await page.goto(`${base}projects/reservation-system/`);
  await expect(page.locator('article')).toContainText('당시 고려하지 못했습니다');
});
