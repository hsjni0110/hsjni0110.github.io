# Portfolio editorial redesign implementation plan

**Goal:** 질문으로 관심을 만들고, 실무·대표 사례가 근거를 제공하는 읽기 쉬운 포트폴리오.
**Architecture:** 기존 Astro 정적 사이트, 로컬 CSS·작은 progressive enhancement 스크립트. 새 의존성 없음.
**Spec:** docs/superpowers/specs/2026-10-24-portfolio-editorial-design.md

- [x] index.astro 재구성: 질문형 hero, 실무 우선, 두 대표 사례와 짧은 진행 중 작업, 압축 소개.
- [x] ProjectStory·Experience 개편: 서비스 소개·실제 기여·근거 링크, ForgeSync 개선 전후. 공개 범위 준수.
- [x] global/prose CSS 교체: 타이포그래피·반응형·포커스·44px, 상세 본문 강조.
- [x] SiteLayout motion: JS 없이 보이는 본문, 1회 reveal·읽기 진행 표시·reduced motion.
- [x] 기존 브라우저 검사 기대값 갱신, 비교 조작·실무 순서·motion 접근성 검사 추가.
- [x] check/build/output/e2e, desktop/mobile 실화면 검증, 로컬 커밋과 인도. 공개 배포 없음.
