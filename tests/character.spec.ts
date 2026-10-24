import {test,expect} from '@playwright/test';
const base=process.env.TEST_BASE_PATH||'/';
test('character motion pauses and respects reduced motion',async({page})=>{
 await page.goto(base);
 const player=page.locator('.character-player');
 await expect(player).toHaveAttribute('data-playing','true');
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
