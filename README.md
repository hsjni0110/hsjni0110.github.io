# 한석진 포트폴리오

누구의 어떤 문제인지 먼저 이해하고, 상황에 맞는 해결책을 끝까지 만드는 개발자의 경험을 소개하는 한국어 정적 사이트입니다.

## 로컬 확인

Node.js는 설치된 Astro 패키지의 engine 조건을 만족해야 합니다. 이 작업은 Node 24 환경에서 확인했습니다.

```sh
npm ci
npm run dev -- --port 4322
```

브라우저에서 http://127.0.0.1:4322/ 를 엽니다. 서버는 로컬 주소에만 바인딩하며 외부에 배포하지 않습니다.

완성된 정적 출력 확인:

```sh
npm run build
npm run preview
```

미리보기 주소는 http://127.0.0.1:4321/ 입니다. 서버를 종료하려면 실행한 터미널에서 Ctrl+C를 누릅니다.

## 검사

```sh
npx playwright install chromium
npm run verify
```

타입·콘텐츠 스키마, 정적 빌드, 로컬 참조·공개 파일·PDF 동일성, 브라우저 탐색·접근성 검사를 순서대로 실행합니다. 텍스트 검사만으로 모든 개인정보나 주장 정확성이 검증되는 것은 아니므로 공개 문안·시각 자료를 별도로 검수합니다.

## 콘텐츠 수정

- `src/content/projects/`: 네 사례의 본문과 메타, 메인 요약의 단일 출처
- `src/data/profile.ts`: 공개 연락처·실무 경력·활동
- `src/pages/index.astro`: 메인 구성
- `src/styles/`: 색·타이포그래피·반응형 스타일

사진과 실제 화면은 `src/assets/`에 선별 보관합니다. 취업 서류 원본이나 회사 내부 자료를 `public/`에 넣지 않습니다. 

## 이력서 갱신

공개용 이력서의 생성 원본은 `scripts/create-resume.py`입니다. ReportLab을 사용할 수 있는 Python으로 실행하면 `output/pdf/han-seokjin-resume.pdf`를 갱신합니다. 렌더링한 세 페이지를 확인한 뒤 같은 파일을 `public/resume.pdf`로 복사합니다. `npm run verify`가 두 파일의 SHA-256 일치를 확인합니다. 공개 전 주소·전화번호·연봉·계좌 등 제외 항목과 PDF 화면을 다시 확인합니다.

## 배포

`hsjni0110.github.io` 저장소의 main에 push하면 GitHub Actions가 검사 후 배포합니다. 최초 연결과 로컬 실행 방법은 [배포 안내](docs/deployment.md)에 있습니다. 원격 업로드는 아직 수행하지 않았습니다.
