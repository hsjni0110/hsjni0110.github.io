# GitHub Pages 배포

대상 저장소: `hsjni0110/hsjni0110.github.io`
사이트 주소: `https://hsjni0110.github.io/`

## 처음 올릴 폴더

`output/github-pages/`는 사이트 소스, 사용 중인 이미지와 폰트, 공개 이력서, 빌드·테스트 도구, 배포 설정만 복사한 공개용 폴더입니다. 원래 작업 폴더의 `.git`과 내부 문서, 검증 이미지, 폐기한 시안은 포함하지 않습니다.

원래 작업 폴더의 Git 이력에는 내부 자료가 있습니다. 원래 저장소를 push하거나 복제하지 말고, 공개용 폴더에서 새 이력을 시작합니다. 내부 자료는 원래 폴더에 보존되어 있습니다.

## 최초 업로드

1. GitHub에서 `hsjni0110.github.io`라는 빈 Public 저장소를 생성합니다. 기존 저장소가 있다면 덮어쓰지 말고 먼저 내용을 확인합니다.
2. 저장소의 Settings → Pages → Source를 GitHub Actions로 선택합니다.
3. 아래 명령은 **공개용 폴더에서만** 실행합니다.

```sh
cd /Users/hanseokjin/Desktop/project/portfolio/output/github-pages
git init -b main
git add .
git commit -m "Initial portfolio"
git remote add origin https://github.com/hsjni0110/hsjni0110.github.io.git
git push -u origin main
```

4. Actions → Deploy portfolio에서 성공 여부를 확인한 뒤 사이트와 상세 페이지, 이력서 다운로드를 확인합니다.

`.github/workflows/deploy.yml`은 main push 또는 수동 실행 시 Node 24에서 타입 검사·정적 빌드·링크 및 공개 이력서 검사를 수행합니다. 성공한 dist만 GitHub Pages에 배포합니다. 별도 PAT는 필요하지 않습니다.

## 이후 수정

공개용 폴더를 저장소 작업 위치로 사용합니다. main에 커밋을 올릴 때마다 자동 배포됩니다. 원래 작업 폴더를 계속 쓴다면 변경한 소스·자산만 공개용 폴더로 옮겨 검사한 뒤 커밋합니다. `.git`이나 내부 docs 폴더를 복사하지 않습니다.

## 로컬 확인

```sh
npm ci
npm run dev -- --port 4322
```

전체 검사:

```sh
npx playwright install chromium
SITE_URL=https://hsjni0110.github.io BASE_PATH=/ npm run verify
```

정적 미리보기: `npm run preview` → http://127.0.0.1:4321/

`output/pdf/han-seokjin-resume.pdf`는 공개 이력서의 검증용 사본으로 포함합니다. 공개 PDF와 검증용 사본을 함께 갱신해야 합니다. 이력서 생성은 로컬에서 ReportLab과 macOS Arial Unicode 폰트를 사용합니다. Pages 배포 자체에는 Python이 필요하지 않습니다.

저장소 이름을 portfolio처럼 바꾸면 BASE_PATH를 `/portfolio/`로 변경해야 합니다. 현재 설정은 사용자 루트 사이트 전용입니다.

현재 원격 업로드와 실제 배포는 수행하지 않았습니다.
