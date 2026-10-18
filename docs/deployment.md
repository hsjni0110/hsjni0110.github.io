# 로컬 확인과 배포 준비

현재 결과물은 로컬 전용입니다. 원격 저장소 생성·푸시·호스팅 등록·공개 배포는 수행하지 않았습니다.

## 실행과 검사

`npm ci`, `npm run verify`, `npm run dev -- --port 4322`로 확인합니다. Chromium이 없으면 `npx playwright install chromium`을 먼저 실행합니다. 별도 서버용 환경변수는 필요하지 않습니다.

`npm run preview`는 production build를 127.0.0.1:4321에서 제공합니다. 개발 서버와 테스트 서버는 서로 다른 포트를 씁니다.

## 주소 설정

- `SITE_URL`: 실제 배포 HTTPS origin. 경로 없이 예를 들어 `https://사용자도메인` 형식으로 지정합니다. 실제 주소가 정해지기 전에는 생략합니다.
- `BASE_PATH`: `/` 기본값. 저장소 하위 배포라면 `/저장소명/`처럼 선행·후행 슬래시를 포함합니다.
- `TEST_BASE_PATH`: Playwright가 검사할 동일한 하위 경로. 일반 로컬 검사에서는 생략합니다.

SITE_URL이 없으면 canonical·절대 OG 이미지 URL·sitemap·robots를 만들지 않습니다. 로컬 화면과 나머지 메타데이터는 그대로 확인할 수 있습니다. 실제 주소가 정해진 공개 빌드에만 SITE_URL을 전달합니다.

## 하위 경로의 로컬 회귀 검사

다음은 공개 배포가 아닌 시험용 빌드입니다.

```sh
SITE_URL=https://example.invalid BASE_PATH=/portfolio/ TEST_BASE_PATH=/portfolio/ npm run verify
```

시험 후 일반 `npm run verify`를 실행해 가상 주소와 시험 base를 제거한 기본 로컬 출력을 다시 만듭니다. `.invalid` 주소의 결과물을 외부에 올리지 않습니다.

## 추후 GitHub Pages를 사용할 경우

실제 계정·저장소·사용자 사이트 여부를 정한 뒤 Astro 공식 GitHub Pages 가이드에 따라 Actions를 구성합니다. 기본 명령은 `npm ci`, `npm run verify`, 결과 폴더는 `dist/`입니다. 프로젝트 사이트는 BASE_PATH가 필요하고 사용자 루트 사이트는 `/`를 사용합니다. 이번 구현에는 자동 배포 workflow를 추가하지 않았습니다.

공개 직전 확인:

1. 실제 SITE_URL·BASE_PATH로 빌드하고 링크·서체·PDF를 다시 검사합니다.
2. 사이트 이름과 공개 본문·이미지·PDF의 개인정보 및 근거 범위를 다시 검수합니다.
3. HINT 진행·수료 상태와 상대 시점 표현을 현재 기준으로 확인합니다.
4. 서비스에서 `/projects/speaktext/` 같은 상세 직접 접근·새로고침과 존재하지 않는 경로의 HTTP 404를 확인합니다.
5. canonical·OG 이미지·sitemap URL이 실제 주소이며 robots가 sitemap을 가리키는지 확인합니다.
6. 재배포 시 HTML 캐시와 해시된 자산 경로를 점검하고, 이메일 링크와 PDF 다운로드를 실제 브라우저에서 확인합니다.

외부 호스팅에서의 HTTP·캐시 동작은 아직 검증하지 않았습니다. 공개 배포는 별도의 요청으로 진행합니다.
