import {test,expect} from '@playwright/test';
const base=process.env.TEST_BASE_PATH||'/';
test('character motion pauses and respects reduced motion',async({page})=>{
 await page.goto(base);
 const player=page.locator('.character-player');
 await expect(player).toHaveAttribute('data-playing','true');
 expect(await page.locator('.coding-sprite').evaluate(el=>getComputedStyle(el).animationDuration)).toBe('4.8s');
 await page.getByRole('button',{name:'움직임 일시정지',exact:true}).click();
 await expect(player).toHaveAttribute('data-playing','false');
 await page.getByRole('button',{name:'움직임 재생',exact:true}).click();
 await expect(player).toHaveAttribute('data-playing','true');
 await page.emulateMedia({reducedMotion:'reduce'});
 await expect(player).toHaveAttribute('data-playing','false');
 await expect(page.getByRole('button',{name:'정지 화면',exact:true})).toBeDisabled();
});
test('work link text has room at narrow and desktop widths',async({page})=>{
 for(const width of [360,726,1100]){
 await page.setViewportSize({width,height:850});await page.goto(base);
 for(const title of await page.locator('.portrait-work strong').all())expect((await title.boundingBox())!.width).toBeGreaterThan(150);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth)).toBe(true);
 }
});


test('each case has a readable pencil explanation without motion',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const id of ['speaktext','forgesync','db-fleet-ops','reservation-system']){
  await page.goto(`${base}projects/${id}/`);
  await expect(page.locator('.pencil-figure')).toHaveCount(1);
  await expect(page.locator('.pencil-stage')).toHaveCount(3);
  await expect(page.locator('.pencil-figure figcaption')).toBeVisible();
  expect(await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length)).toBe(0);
 }
});
