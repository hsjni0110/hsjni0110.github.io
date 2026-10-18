export const profile = {
  name: '한석진',
  email: 'seokjin.han010@gmail.com',
  githubUrl: 'https://github.com/hsjni0110',
  velogUrl: 'https://velog.io/@hsjni0110/posts',
  experience: [
    { company: '모플', period: '2025.09 — 2026.03', role: '백엔드 · 데이터 파이프라인', description: '매일 늘어나는 데이터를 처리하는 배치의 실행 시간 단축. SQL 실행 계획·분산 처리 구조 분석, dbt Custom Incremental 구현과 결과 검증.', contribution: '병목 분석부터 개선안 검토, 구현과 결과 검증까지 직접 담당', stack: 'PostgreSQL · Citus · dbt · SQL' },
    { company: '스마트뉴비', period: '2024년 하반기', role: '백엔드 개발', description: '인턴십 매칭 플랫폼 인턴메이트의 공고 관리 API, 사용자 정보 기반 추천, 인증·파일 처리 구현. 인수 테스트 작성과 코드 리뷰 참여.', contribution: '초기 서비스 기능 개발과 반복적인 개발 작업 개선', stack: 'Java · Spring Boot · MySQL · Redis · AWS S3' },
  ],
  education: [
    { title: '충남대학교 컴퓨터융합학부', detail: '학사 · 2020.03 — 2026.02' },
    { title: '현대자동차 HINT 제조지능화 과정', detail: '2026.07 — 현재 · 2026.10 기준' },
    { title: 'UC San Diego Qualcomm Institute', detail: 'AI 연구 교육 프로그램 · 2025.01 — 2025.02' },
  ],
  activities: [
    { title: '멋쟁이사자처럼 대학생', detail: '2024년 교육생 · 2025년 백엔드 운영진' },
  ],
} as const;
