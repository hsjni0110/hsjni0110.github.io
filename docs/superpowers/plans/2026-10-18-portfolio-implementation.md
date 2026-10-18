# Portfolio Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 한국어로 문제 인식·판단·실행·검증을 전달하는 메인과 상세 사례 5개, 공개 이력서·연락 경로를 갖춘 정적 포트폴리오를 만든다.

**Architecture:** Astro에서 로컬 Markdown 사례를 빌드 시 읽어 메인·상세 HTML을 생성한다. 공통 레이아웃·상세 템플릿·CSS를 공유하고 서버·CMS·클라이언트 프레임워크 없이 제공한다. 근거 장부는 내부 문서로 보관하고, 공개용 본문과 선별 자산만 정적 출력에 포함한다.

**Tech Stack:** Astro, TypeScript strict, Markdown Content Collections, 일반 CSS, Astro 이미지 처리, Pretendard WOFF2. 개발 검증은 Astro Check, Playwright와 Node 기본 라이브러리. 패키지 관리는 npm과 package-lock.json. React·Tailwind·애니메이션 라이브러리는 도입하지 않는다.

**Spec:** [확정 설계](../specs/2026-10-18-portfolio-design.md). 2026-10-18 사용자 승인 완료. 구현자는 이 문서와 설계를 함께 읽는다.

## Global Constraints

- “누구의 어떤 문제인지 먼저 이해하고, 상황에 맞는 해결책을 끝까지 만드는 동료.”를 중심에 둔다.
- 한국어 중심이고 기술명·프로젝트명은 원래 표기를 사용한다.
- 메인 우선순위: SpeakText → ForgeSync → 동시생활 앱 → 실무 경험 → 심화 사례 → 소개·연락.
- 현재 앱의 실제 화면·모집 링크가 없고 변경 버전의 미검증 상태가 명확하다.
- 주소, 전화번호, 생년월일, 주민번호, 계좌, 연봉을 공개하지 않는다.
- 사용자 진술, 코드·문서 근거, 실제 실행 결과를 구분한다.
- 첫 버전은 밝은 테마이며 강제 스크롤·자동 재생 영상·다크 테마·폼·분석 도구를 넣지 않는다.
- 본문 대비 4.5:1 이상. 모바일 터치 영역 약 44px 이상. `prefers-reduced-motion`에서 부드러운 이동을 제거한다.
- 기본 색: `#FFFFFF`, `#F5F6F8`, `#1D1D1F`, `#525A65`, `#005FCC`, `#DDE2E8`.
- 본문 폭 680~740px, 넓은 자료 최대 약 1120px. 제목 56~72px/34~44px, 본문 17~18px/16~17px, 줄높이 약 1.7.
- 사이트는 로컬 정적 출력까지 제작한다. 원격 저장소 생성·푸시·공개 배포는 별도 실행 범위다.
- 현재 폴더는 Git 저장소가 아니다. 구현 시작 시 로컬 Git을 초기화하고 작업 단위로 커밋한다. 원격은 임의로 만들지 않는다.

## Review Focus

1. 상세 URL 직접 접근·새로고침과 하위 경로 배포에서도 사진·PDF·복귀 링크가 작동해야 한다. Task 4·7의 경로 테스트가 담당한다.
2. 긴 한글 제목과 360px 화면·200% 확대에서도 본문이나 연락 경로가 잘리면 안 된다. Task 6의 반응형 검사와 시각 검수가 담당한다.
3. JavaScript 비활성·동작 줄이기·키보드 입력에서도 콘텐츠와 탐색이 가능해야 한다. Task 3·6의 브라우저 검사가 담당한다.
4. 이미지 파일이 없거나 실패해도 실제 근거와 캡션은 읽혀야 하며 가짜 화면으로 대체하면 안 된다. Task 2·6이 담당한다.
5. 새 앱 화면·미확인 성과·민감한 원본 자료가 HTML·자산·PDF에 포함되면 안 된다. Task 1·7의 공개 검수가 담당한다.

---

## 1. 결정과 작업 환경

### 1.1 기술·호스팅 결정

Astro는 로컬 콘텐츠의 정적 HTML 생성과 이미지 처리를 지원하므로 이 사이트에 사용한다. 첫 구현은 일반 CSS와 서버 렌더링된 HTML만으로 완결하며, 모바일 메뉴는 줄바꿈 가능한 항상 보이는 링크로 처리해 별도 상태 관리가 필요 없게 한다. 이미지 확대와 이메일 복사 기능은 첫 버전에서 생략한다. 캡션·원본 근거 링크·선택 가능한 이메일 텍스트를 제공한다.

기본 로컬 경로는 `/`, `output: 'static'`, `trailingSlash: 'always'`, 출력은 `dist/`다. `SITE_URL`과 `BASE_PATH`를 빌드 환경에서 받는다. `SITE_URL` 없이는 canonical·절대 OG URL·sitemap·robots를 생략하고 로컬 미리보기를 허용한다. 공개용 빌드는 유효한 HTTPS 주소를 요구한다. `BASE_PATH`는 `/` 또는 `/portfolio/` 같은 선행·후행 슬래시 형식이다.

정적 호스팅의 우선 후보는 GitHub Pages다. 저장소명·실제 주소·사용자 사이트 여부는 확정되지 않았으므로 호스팅 계정이나 URL을 만들지 않는다. 호스팅 안내는 작성하되 자동 배포 워크플로는 아직 추가하지 않는다.

실행 시 공식 패키지의 안정 버전과 Node engine을 확인해 정확한 버전을 lockfile에 고정한다. 현재 번들 Node는 v24.19.0이다. 필요한 경우 요구 조건에 맞는 제공 런타임을 사용하며 시스템 Node를 덮어쓰지 않는다.

공식 참고: [Content Collections](https://docs.astro.build/en/guides/content-collections/), [Images](https://docs.astro.build/en/guides/images/), [Sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/), [GitHub Pages](https://docs.astro.build/en/guides/deploy/github/). 2026-10-18 확인. 실행 시 설치한 버전의 API와 대조한다.

### 1.2 파일 책임

```text
astro.config.mjs                 정적 출력·site·base·sitemap 조건
package.json / package-lock.json 실행 명령과 고정 의존성
tsconfig.json                    Astro strict 설정
.gitignore                       node_modules/dist/.astro/tmp 제외
src/content.config.ts            projects 컬렉션과 공개 메타 스키마
src/content/projects/*.md        5개 상세 사례의 최종 공개 본문
src/data/profile.ts              이름·이메일·경력·교육·외부 링크
src/lib/paths.ts                 base 경로를 적용하는 단일 URL 함수
src/layouts/SiteLayout.astro     head·탐색·main·푸터
src/layouts/ProjectLayout.astro  사례 요약·목차·본문·관련 사례
src/components/SiteHeader.astro  네비게이션과 본문 바로가기
src/components/ContactLinks.astro 이메일·PDF·GitHub·Velog
src/components/ProjectStory.astro 메인 사례 요약·화면·상세 링크
src/components/Figure.astro      실제 화면과 대체 텍스트·캡션·근거
src/components/Experience.astro  회사 경력
src/pages/index.astro            메인 이야기 구성
src/pages/projects/[id].astro    정적 상세 경로 생성
src/pages/404.astro              없는 페이지와 복귀
src/pages/[metadata].txt.ts          SITE_URL 있을 때 robots.txt 정적 생성
src/styles/global.css           토큰·기본·반응형·포커스
src/styles/prose.css            사례 본문·표·목차 스타일
src/assets/portrait.webp        승인된 사진의 웹용 파생본
src/assets/projects/forgesync/   PDF에서 선별한 실제 화면
src/assets/og.png               이름·핵심 문장의 공유 이미지
public/fonts/                   Pretendard 파일·라이선스
public/resume.pdf               승인 PDF의 동일 복사본
scripts/check-output.mjs        정적 파일·내부 참조·노출 검사
playwright.config.ts            빌드된 사이트 검사
tests/navigation.spec.ts       URL·연락·PDF·목차 검사
tests/accessibility.spec.ts    키보드·JS 없음·모션 감소·모바일
tests/content.spec.ts          비공개 앱 화면·과장·한계 표시 확인
docs/content/evidence.md        주장별 근거와 확인 범위, 비공개
docs/content/assets.md          자산 출처·버전·재현 여부, 비공개
docs/deployment.md              로컬 실행과 배포 준비·환경변수
```

상세 파일은 `speaktext.md`, `forgesync.md`, `shared-life.md`, `db-fleet-ops.md`, `reservation-system.md`다. 프로젝트별 전용 컴포넌트는 실제로 필요한 시점에만 추가한다.

### 1.3 데이터 계약

- `ProjectId`: 위 다섯 파일명의 확장자 없는 값.
- 컬렉션 frontmatter: `title: string`, `description: string`, `lead: string`, `kind: 'team' | 'personal'`, `period: string`, `role: string`, `status: 'completed' | 'in-development'`, `order: number`, `featured: boolean`, `sources: { label: string; url: string }[]`.
- `summary: { problem: string; decision: string; outcome: string }`는 메인 요약의 단일 출처다. 상세 요약도 이를 사용해 상태·성과가 달라지지 않게 한다.
- 선택 필드 `hero: { src: ImageMetadata; alt: string; caption: string; sourceUrl?: string }`. 컬렉션의 이미지 스키마로 로컬 파일을 검증한다. 동시생활 앱에는 `hero`를 두지 않는다.
- 본문은 Markdown. 표준 H2 제목은 맥락·판단·실행·확인·한계와 다음 단계. Astro의 Markdown heading 정보에서 목차를 만든다.
- `profile`: `name`, `email`, `githubUrl`, `velogUrl`, `experience[]`, `education[]`, `activities[]`를 담는 빌드 시 상수다. PDF 경로는 `/resume.pdf`다.
- `withBase(path: string): string`는 사이트 루트 상대 경로에 `import.meta.env.BASE_URL`을 한 번 적용한다. 외부 URL·메일 주소에는 사용하지 않는다.
- `SiteLayout` props: `title`, `description`, 선택 `ogImage`. canonical은 `Astro.url.pathname`과 검증된 `SITE_URL`로 만든다.
- `ProjectLayout` props: `project: CollectionEntry<'projects'>`, `headings: { depth: number; slug: string; text: string }[]`. 본문은 default slot이다.
- `Experience`는 Task 1의 `profile.experience`를 직접 import해 경력을 출력하며 props를 받지 않는다. `ContactLinks`는 profile과 `withBase`를 직접 사용하고 props를 받지 않는다.
- `ProjectStory` props: `project: CollectionEntry<'projects'>`. `Figure` props: `src: ImageMetadata`, `alt`, `caption`, 선택 `sourceUrl`, `eager?: boolean`.

## 2. 작업 순서

### Task 1: 공개 본문과 근거 장부 확정

**Files:** Create `docs/content/evidence.md`, `src/content/projects/{speaktext,forgesync,shared-life,db-fleet-ops,reservation-system}.md`, `src/data/profile.ts`.

**Interfaces:** 설계 6~8장의 사실·공개 기준을 소비한다. 1.3의 메타와 표준 H2 본문을 후속 작업에 제공한다. 이 시점에는 앱을 실행하지 않는다.

- [ ] Step 1: 기존 Git 유무·작업 파일을 재확인하고 없으면 이 폴더만 로컬 `git init`한다. 기존 PDF·설계 문서는 보존한다.
- [ ] Step 2: 주장 장부에 주장, 대상 페이지, 사용자 확인/문서/코드/테스트 읽기/미검증, 출처, 허용 문장을 기록한다. 개인정보 원문은 복사하지 않는다.
- [ ] Step 3: 5개 상세 본문과 메타를 작성한다. SpeakText 공동 결정·정성 피드백, ForgeSync 현장 가정·정답 없음, 앱 변경 버전 미검증을 각각 확인·한계 절에 넣는다.
- [ ] Step 4: 경력·활동 상수를 작성한다. 스마트뉴비는 `2024년 하반기`, HINT는 `2026.07 - 현재`로 유지한다. 수료 사실을 새로 확인하지 않으면 완료로 바꾸지 않는다.
- [ ] Step 5: 설계와 본문을 나란히 검수한다. 모플의 미확인 수치·고객 영향, 앱 화면·링크, 예약 경계 해결 주장이 없어야 한다. 글의 맞춤법·중복·역할 분리를 사람이 읽어 확인한다. 정적인 문안 자체를 위한 단위 테스트는 만들지 않는다.
- [ ] Step 6: 공개 본문과 근거 장부만 명시적으로 선택해 `docs: prepare reviewed portfolio content`로 커밋한다. 민감한 원본·`tmp/`를 추가하지 않는다.

### Task 2: 승인된 화면·사진·PDF 준비

**Files:** Create `docs/content/assets.md`, `src/assets/portrait.webp`, `src/assets/projects/forgesync/{overview,before,detail,factory}.webp`, `public/resume.pdf`. SpeakText 실제 캡처 확보 시 `src/assets/projects/speaktext/editor.webp`만 추가한다.

**Interfaces:** 사용자 승인 원본 사진·ForgeSync PDF·공개용 이력서를 소비하고, `ImageMetadata`로 import 가능한 승인 자산과 자산 장부를 제공한다.

- [ ] Step 1: 사진·원본 PDF 경로와 `output/pdf/han-seokjin-resume.pdf`의 존재·2쪽 내용을 확인한다. 승인되지 않은 자소서 파일은 자산 폴더에 복사하지 않는다.
- [ ] Step 2: 사진은 자연스러운 비율을 유지한 웹용 파생본, ForgeSync는 기존 PDF의 실제 화면 이미지를 추출한다. 텍스트가 읽히는 해상도로 WebP를 만들고 원본을 변경하지 않는다.
- [ ] Step 3: 모든 자산을 시각 확인하고 크기·출처·원본 페이지·시점·재현 여부를 장부에 기록한다. ForgeSync 화면은 과거 화면임을 필요 시 캡션에 밝힌다.
- [ ] Step 4: SpeakText 실제 편집 캡처를 추가 조사한다. 없으면 첫 버전은 해당 사례를 이미지 없이 구성한다. 가짜 다중 선택 화면·API 캡처로 대체하지 않는다. 로컬 재현은 별도 후속 작업으로 남겨 제작을 막지 않는다.
- [ ] Step 5: 승인된 이력서만 `public/resume.pdf`로 복사하고 SHA-256이 원본과 같은지 확인한다. PDF 문자 추출과 시각 검수로 비공개 항목을 확인한다.
- [ ] Step 6: `assets: prepare approved portfolio media`로 선별 파일만 커밋한다.

### Task 3: 정적 기반과 공통 레이아웃

**Files:** Create `package.json`, `package-lock.json`, `astro.config.mjs`, `tsconfig.json`, `.gitignore`, `src/content.config.ts`, `src/lib/paths.ts`, `src/layouts/SiteLayout.astro`, `src/components/{SiteHeader,ContactLinks}.astro`, `src/styles/global.css`, `src/pages/index.astro`, `playwright.config.ts`, `tests/navigation.spec.ts`, `public/fonts/`.

**Interfaces:** Task 1의 콘텐츠 계약·profile을 소비한다. `withBase`·`SiteLayout`·연락 링크를 Task 4~7에 제공한다.

- [ ] Step 1: 공식 안정 패키지와 engines를 확인하고 최소 Astro·TypeScript·Astro Check 및 개발용 Playwright를 설치·고정한다. 기존 폴더를 덮어쓰는 scaffold는 사용하지 않는다. scripts는 `dev`, `check`, `build`, `preview`, `test:e2e`, `verify`로 정의한다.
- [ ] Step 2: 정적 설정과 Content Collections 스키마를 작성한다. `SITE_URL` 누락은 로컬 허용, 주어진 값이 HTTPS URL이 아니면 명확한 빌드 오류. `BASE_PATH` 형식도 검증한다.
- [ ] Step 3: Playwright는 production build의 Astro preview를 `127.0.0.1:4321`에서 실행하도록 설정한다. 첫 테스트는 `homepage has email and resume links`: `mailto:seokjin.han010@gmail.com`과 base가 적용된 PDF 링크 존재를 단언한다. `npm run test:e2e --tests/navigation.spec.ts`는 아직 링크가 없어 실패해야 한다.
- [ ] Step 4: common layout·본문 바로가기·상단 네비게이션·연락 블록을 구현한다. 모바일에서도 메뉴가 사라지지 않고 44px 터치 영역으로 줄바꿈되게 한다. 프로필 폰트는 Pretendard 원본 라이선스와 함께 자체 제공, `font-display: swap`을 적용한다.
- [ ] Step 5: `npm run check && npm run build`와 첫 navigation 테스트를 실행한다. 스키마·링크 테스트 통과와 빈 canonical 부재를 확인한다.
- [ ] Step 6: `feat: add static site foundation and contact navigation`으로 커밋한다.

### Task 4: 상세 사례 5개와 문서형 읽기 경험

**Files:** Create `src/layouts/ProjectLayout.astro`, `src/pages/projects/[id].astro`, `src/components/Figure.astro`, `src/styles/prose.css`. Modify `tests/navigation.spec.ts`. Create `tests/content.spec.ts`.

**Interfaces:** `getCollection('projects')`, `render(entry)`, Task 3의 layout·base 함수를 사용한다. 다섯 고정 상세 경로·실제 heading anchor·관련 링크를 제공한다.

- [ ] Step 1: `all five detail pages work by direct navigation` 테스트를 추가한다. 각 URL로 바로 이동해 프로젝트 제목, H2 `확인`, `한계와 다음 단계`, 해당 목차 anchor와 메인 복귀 링크를 단언한다. `npm run test:e2e --tests/navigation.spec.ts`가 상세 페이지 부재로 실패하는지 확인한다.
- [ ] Step 2: `getStaticPaths()`로 컬렉션의 다섯 ID를 생성한다. `render` 결과의 Content와 headings를 `ProjectLayout`에 넘긴다. 잘못된 ID는 이후 404로 처리한다.
- [ ] Step 3: 상단 요약·역할·유형·기간·상태, Markdown 본문, H2 목차, 관련 사례를 구현한다. 좁은 본문과 넓은 이미지의 위계를 설정하고 모바일에서는 목차를 일반 흐름에 둔다.
- [ ] Step 4: Figure는 Astro Image로 크기와 alt를 제공하고 캡션·출처 링크를 이미지 외부 HTML로 남긴다. 큰 화면 원본은 링크로 제공하고 modal 확대는 만들지 않는다.
- [ ] Step 5: content 테스트 `shared-life has no product image or recruitment link`는 앱 상세에 제품 이미지·외부 모집 CTA가 없고 개발 중·새 버전 검증 전 문장이 있음을 확인한다. `case outcomes retain their scope`는 SpeakText 팀 내부 피드백, ForgeSync 불량 정확도 미검증, 예약 충돌 한계가 렌더링됨을 단언한다. 구현 전 실패를 확인한 뒤 공개 본문과 템플릿 연결을 완성한다.
- [ ] Step 6: `npm run check && npm run build` 및 navigation·content 테스트가 통과하면 `feat: publish five evidence-based case studies`로 커밋한다.

### Task 5: 메인 이야기와 시각 구성 완성

**Files:** Modify `src/pages/index.astro`, `src/styles/global.css`. Create `src/components/ProjectStory.astro`, `src/components/Experience.astro`. Modify `tests/navigation.spec.ts`.

**Interfaces:** Task 1 profile과 컬렉션의 summary·lead·featured·order·hero를 소비한다. 메인 `#cases`, `#experience`, `#about`, `#contact`를 탐색 대상으로 제공한다.

- [ ] Step 1: 첫 화면 이름·정확한 핵심 제목과 메인 사례 순서를 검증하는 navigation 시나리오를 추가해 현재 미완성 화면에서 실패를 확인한다. 의미 있는 링크·heading만 검사하며 CSS 구현을 테스트에 복제하지 않는다.
- [ ] Step 2: 큰 제목·작은 사진·관점 소개를 배치한다. 메인 H1은 `누구의 어떤 문제인지부터 생각합니다.`이며 이름은 즉시 식별 가능해야 한다.
- [ ] Step 3: SpeakText → ForgeSync → 현재 앱을 구성한다. 실제 이미지가 있는 사례는 크게, 현재 앱은 기획 전후의 글 비교로 배치한다. 기간은 시간순이라는 잘못된 인상을 주지 않게 표기한다.
- [ ] Step 4: 모플·스마트뉴비 실무 경험, 심화 사례 두 개, 학력·활동·관심과 연락을 배치한다. summary와 상세의 성과 표현이 달라지지 않는지 읽어 확인한다.
- [ ] Step 5: 1440px·768px·390px에서 실제 캡처를 비교해 여백·한글 제목 줄바꿈·사진 크기·이미지 가독성을 수정한다. 내비게이션이 데스크톱 한 줄, 모바일에서 본문을 가리지 않는지 확인한다.
- [ ] Step 6: navigation·content 테스트 및 정적 빌드가 통과하면 `feat: compose the portfolio narrative homepage`로 커밋한다.

### Task 6: 모바일·접근성·실패 상태 검증

**Files:** Create `tests/accessibility.spec.ts`, `src/pages/404.astro`. Modify 해당 layout·CSS·Figure. Modify `tests/navigation.spec.ts`.

**Interfaces:** Task 3~5의 실제 링크·heading·본문 DOM을 소비한다. 새 데이터 계약은 추가하지 않는다.

- [ ] Step 1: `reading works without javascript`는 JS 비활성 context에서 메인→상세→연락 링크와 본문 표시를 단언한다. `keyboard reaches content and contact`는 Tab으로 skip link와 연락 링크 접근·focus 표시를 확인한다.
- [ ] Step 2: `narrow korean content does not overflow`는 폭 360·390에서 메인과 가장 긴 상세의 `scrollWidth <= clientWidth`를 검사한다. `reduced motion disables smooth scrolling`은 reduce 환경에서 root computed scroll-behavior가 smooth가 아님을 단언한다. 기본 위반이 있으면 실패를 확인하고 CSS를 수정한다. 초기부터 충족하는 경우 테스트를 위해 위반을 만들지 않는다.
- [ ] Step 3: `failed images retain context`는 이미지 요청 차단 후 캡션·출처 링크·본문이 보이는지 확인한다. `.astro` 오류 화면이나 비어 있는 섹션으로 바뀌지 않아야 한다.
- [ ] Step 4: 404 페이지를 구현하고 `/404.html`의 복귀 링크를 검사한다. 배포 서버에서 실제 없는 경로의 HTTP 404 동작은 Task 8 안내에 별도 확인 항목으로 둔다.
- [ ] Step 5: 키보드로 실제 탐색하고 200% 확대, 긴 한글·URL, 360/768/1440 화면, 이미지 실패를 시각 확인한다. 본문 대비 4.5:1, 타깃 약 44px, 초점이 header에 가려지지 않는지 측정한다.
- [ ] Step 6: 전체 Playwright 검사 통과 후 `fix: refine responsive reading and accessible navigation`으로 커밋한다.

### Task 7: 메타데이터·공개 출력·하위 경로 검증

**Files:** Modify `astro.config.mjs`, `src/layouts/SiteLayout.astro`. Create `src/pages/[metadata].txt.ts`, `src/assets/og.png`, `scripts/check-output.mjs`. Modify package scripts·tests/navigation.spec.ts.

**Interfaces:** `SITE_URL`, `BASE_PATH`, `dist/`, 모든 페이지 메타·정적 자산을 소비한다. `npm run verify`와 공개용 출력 검사 명령을 제공한다.

- [ ] Step 1: Node 기본 `assert`·파일 읽기로 검사 스크립트를 작성한다. 다섯 `dist/projects/<id>/index.html`, 메인, 404, PDF와 모든 로컬 href/src의 존재를 검사한다. HTML의 내부 anchor는 ID가 존재해야 한다. 원격 링크는 형식과 사용 목적을 검수하며 접속 성공을 빌드의 필수 조건으로 삼지 않는다.
- [ ] Step 2: 출력 allowlist는 HTML·CSS·JS·이미지·WOFF2·라이선스·이력서·메타 파일뿐이다. docx·원본 취업 PDF·`docs/`·`tmp/`·source map·개인 절대 경로가 dist에 없음을 검사한다. PDF는 승인 파일과 hash 일치로 확인한다. 문자열 검사만으로 개인정보 안전이 증명된다고 주장하지 않는다.
- [ ] Step 3: 로컬 빌드에서 canonical·sitemap·robots가 생기지 않음을 확인하고, `SITE_URL=https://example.invalid BASE_PATH=/portfolio/ npm run build`에서 상세·이미지·PDF·복귀 링크에 base가 한 번만 붙는지 확인한다. `.invalid`는 로컬 시험 전용이며 최종 dist로 전달하지 않는다.
- [ ] Step 4: SITE_URL이 있는 빌드에만 공식 sitemap 통합과 robots를 추가한다. `[metadata].txt.ts`의 `getStaticPaths()`는 SITE_URL이 있으면 `metadata: 'robots'` 한 경로를, 없으면 빈 배열을 반환한다. 페이지별 한국어 title·description·`lang=ko`·canonical·OG를 제공하고 OG는 이름과 핵심 문장만으로 만든다. 앱 화면은 사용하지 않는다.
- [ ] Step 5: navigation 테스트에 환경변수 `TEST_BASE_PATH`를 적용해 `/portfolio/` 직접 접근·새로고침·PDF를 확인한다. `SITE_URL=https://example.invalid BASE_PATH=/portfolio/ TEST_BASE_PATH=/portfolio/ npm run verify` 후 일반 환경 `npm run verify`를 다시 실행해 시험 주소를 제거한다.
- [ ] Step 6: 모든 최종 공개 본문·이미지·PDF를 사람이 한 번 더 검수하고 `feat: verify static output and sharing metadata`로 커밋한다.

`verify`는 `astro check` → `astro build` → `node scripts/check-output.mjs` → `playwright test` 순서다. 별도 테스트 러너·HTML 파서를 검사 편의만을 위해 추가하지 않는다. 경로 추출은 이 사이트가 생성하는 quoted href/src와 srcset의 URL을 다루고 외부 프로토콜을 건너뛰며 base 접두사를 제거한 뒤 dist와 비교한다.

### Task 8: 완성본 검토와 배포 준비 문서

**Files:** Create `docs/deployment.md`, `README.md`. Modify evidence·assets 장부에 최종 확인 일자·출처 버전 기록. 실행 보고서는 `docs/verification/2026-10-18-site-review.md`에 작성하며 실제 날짜가 달라지면 해당 날짜를 사용한다.

**Interfaces:** 최종 코드·dist·실행 결과와 승인 PDF를 소비한다. 사용자가 실행·수정·배포할 수 있는 안내와 검토 가능한 로컬 사이트를 제공한다.

- [ ] Step 1: `npm ci && npm run verify`로 깨끗한 의존성 설치와 전체 검증을 실행한다. 오류가 있으면 해당 작업을 수정한 뒤 관련 검사부터 다시 수행한다.
- [ ] Step 2: 최종 메인과 사례 5개의 데스크톱·모바일 화면을 확인한다. 확인하지 않은 브라우저·성능·외부 서비스에 성공 주장을 붙이지 않는다.
- [ ] Step 3: 검증 기록에 실행 명령·결과·화면 크기·알려진 제한·미확보 SpeakText 시각 자료 상태를 남긴다. HINT 상태와 상대 시점 표현을 공개 직전에 다시 확인할 항목으로 적는다.
- [ ] Step 4: README에 실행·콘텐츠 수정·승인 PDF 갱신 방법을, deployment 문서에 실제 SITE_URL/BASE_PATH 설정·GitHub Pages 적용 방법·실제 404/캐시/링크 점검 절차를 작성한다. 원격 생성·푸시·배포를 실행하지 않는다.
- [ ] Step 5: 로컬 사이트와 결과물을 사용자에게 보여준다. 외부 공개를 진행하려면 실제 주소·호스팅 대상이 정해지고 공개 단계가 요청돼야 한다.
- [ ] Step 6: 문서와 검증 결과를 `docs: record site verification and deployment instructions`로 커밋한다. 작업 트리 상태와 커밋을 확인하고 완료 보고한다.

## 3. 자기 검토와 인수 기준

| 설계 범위 | 담당 작업 | 인수 근거 |
| --- | --- | --- |
| 이야기·역할·사실·공개 범위 | 1, 4, 5, 7 | 근거 장부·본문 검수·content 테스트·출력 검사 |
| 사진·실제 화면·PDF | 2, 4, 7 | 자산 장부·시각 검수·PDF hash·누락 이미지 검사 |
| 메인·상세·연락·404 | 3~6 | navigation·직접 경로·목차·JS 없음 검사 |
| 색·타이포·여백·모바일 | 3, 5, 6 | 실제 크기별 캡처·가로 넘침·대비·확대 검수 |
| 정적 출력·SEO·base 경로 | 3, 7 | clean build·출력 검사·하위 경로 테스트 |
| 유지보수·배포 준비 | 8 | README·배포 안내·실행 결과 |

이 계획은 사이트 제작 한 흐름이며 별도 하위 프로젝트로 나눌 필요가 없다. 단순 문안·CSS 값마다 단위 테스트를 만들지 않고, 경로·공개 범위·접근성과 실패 조건을 중심으로 검증한다. 단위 테스트가 필요한 실제 로직이 생기면 Node 기본 테스트를 먼저 사용한다.

작업 의존성은 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8이다. 실행은 현재 세션에서 순차 수행하는 방식을 추천한다. 콘텐츠와 시각 자산·화면 표현이 서로 밀접하고 변경 범위가 작은 정적 사이트여서 맥락을 유지하는 편이 적합하다. 사용자가 실행 방법을 선택하기 전에는 이 계획으로 사이트 제작을 시작하지 않는다.

## 4. 이번 계획에 포함하지 않는 것

실제 배포·사용자 지정 도메인 연결, 영어·다크 테마, 계정·CMS·연락 폼, 분석 추적, Velog 런타임 수집, 현재 앱 화면·모집 링크, 회사 내부 자료, 미확인 성과 수치, 사이트와 무관한 기존 프로젝트 버그 수정은 포함하지 않는다.
