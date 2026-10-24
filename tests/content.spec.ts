import { test, expect } from '@playwright/test';
const base = process.env.TEST_BASE_PATH || '/';
test('withdrawn project is absent from public pages', async ({ page, request }) => {
  await page.goto(base);
  await expect(page.locator('a[href*="shared-life"]')).toHaveCount(0);
  await expect(page.locator('main')).not.toContainText('동시생활');
  expect((await request.get(`${base}projects/shared-life/`)).status()).toBe(404);
});
test('case outcomes retain their scope', async ({ page }) => {
  await page.goto(`${base}projects/speaktext/`);
  await expect(page.locator('article')).toContainText('팀 내부 사용의 정성적 피드백');
  await page.goto(`${base}projects/forgesync/`);
  await expect(page.locator('article')).toContainText('실제 정상·불량 정답이 없어 탐지 정확도의 개선 여부는 검증하지 못했습니다.');
  await page.goto(`${base}projects/reservation-system/`);
  await expect(page.locator('article')).toContainText('결제 이벤트 지연과 선점 만료가 겹치는 상황은 당시 고려하지 못했습니다.');
});
test('forgesync provides the actual before and after screen evidence', async ({ page }) => {
  await page.goto(`${base}projects/forgesync/`);
  await expect(page.getByRole('img',{name:'개선 전: 정지와 기록 누락을 구분하기 어려웠던 대시보드'})).toHaveCount(1);
  await expect(page.getByRole('img',{name:'작업·멈춤·기록 없음을 나눠 보여주는 대시보드',exact:true})).toHaveCount(1);
});
