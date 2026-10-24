export const profile = {
  name: '한석진',
  email: 'seokjin.han010@gmail.com',
  githubUrl: 'https://github.com/hsjni0110',
  velogUrl: 'https://velog.io/@hsjni0110/posts',
  experience: [
    { company: '모플', period: '2025.09 — 2026.03', role: '백엔드 · 데이터 파이프라인', description: '매일 늘어나는 데이터를 처리하는 배치의 지연 원인을 분석했습니다. Citus의 부하 집중과 데이터 이동, SQL 실행 계획을 살펴보고 분산 테이블에 직접 적재하는 dbt Custom Incremental을 구현해 처리 시간을 줄였습니다.', contribution: '적재 전후 데이터 건수와 업무 규칙을 비교해 결과를 검증했습니다.', stack: 'PostgreSQL · Citus · dbt · SQL' },
    { company: '스마트뉴비', period: '2024년 하반기', role: '백엔드 개발', description: '인턴십 매칭 플랫폼 인턴메이트의 공고 관리 API와 사용자 정보 기반 추천 로직을 개발했습니다. 인증·파일 처리 기능을 구현하고 주요 API 인수 테스트 작성과 코드 리뷰에도 참여했습니다.', contribution: 'MapStruct로 객체 변환의 반복 코드를 줄이고, FixtureMonkey로 테스트 데이터 생성을 간소화했습니다.', stack: 'Java · Spring Boot · MySQL · Redis · AWS S3' },
  ],
  education: [
    { title: '충남대학교 컴퓨터융합학부', detail: '학사 · 2020.03 — 2026.02', description: '컴퓨터융합학부를 졸업했습니다. 재학 중 동아리의 백엔드 교육과 팀 프로젝트에 참여하고, 스타트업의 서비스 개발·데이터 처리 업무를 경험했습니다.' },
    { title: '현대자동차 HINT 제조지능화 과정', detail: '2026.07 — 현재 · 2026.10 기준', description: '제조 공정·설비와 데이터의 생성·활용 방식을 배우고 있습니다. 교육에서 생긴 궁금증을 ForgeSync로 확장해 공개 CNC 기록의 재생·조회·분석 기능을 구현했습니다.' },
    { title: 'UC San Diego Qualcomm Institute', url: 'https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12318857', linkLabel: '금융 감성 분석을 위한 BERT 모델 결합 준지도 학습 접근법', detail: 'AI 연구 교육 프로그램 · 2025.01 — 2025.02', description: '비라벨 금융 텍스트를 활용한 BERT 준지도학습을 연구했습니다. Self-training과 의사 라벨링을 적용하고, 학습 조건 조정과 교차검증을 거쳐 연구 방법·결과를 논문으로 정리했습니다.' },
  ],
  activities: [
    { title: '멋쟁이사자처럼 대학생', detail: '2024년 교육생 · 2025년 백엔드 운영진', description: 'IT 창업 동아리에서 2024년에는 백엔드를 배우고 팀 프로젝트에 참여했으며, 2025년에는 백엔드 운영진으로 활동했습니다. 다른 팀과 창업에 관심 있는 사람들의 기획을 이야기하면서, 기술적으로 구현할 수 있다는 것과 사람들이 실제로 필요로 한다는 것은 다를 수 있음을 배웠습니다. 이후에는 구현 방법을 고르기 전에 누가 어떤 상황에서 어려움을 겪는지, 기존 방법으로는 왜 해결되지 않는지를 먼저 살피게 됐습니다. 운영진으로는 PR 리뷰와 오류 재현 방법·확인 항목의 Wiki 정리도 맡았습니다.' },
  ],
} as const;
