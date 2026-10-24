from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/han-seokjin-resume.pdf'
pdfmetrics.registerFont(TTFont('Korean', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
W, H = A4
M = 45
INK = HexColor('#17191d')
GRAY = HexColor('#59616c')
BLUE = HexColor('#1858a8')
LINE = HexColor('#dde2e8')
TOTAL_PAGES = 3
c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('한석진 | 공개용 이력서')
c.setAuthor('한석진')
c.setSubject('업무 경험, 프로젝트, 교육과 활동')
y = H - M
page_number = 1


def text(s, size=10.2, color=INK, space=6, leading=None):
    global y
    style = ParagraphStyle('p', fontName='Korean', fontSize=size,
                           leading=leading or size * 1.5, textColor=color,
                           wordWrap=None, splitLongWords=0)
    paragraph = Paragraph(s, style)
    _, height = paragraph.wrap(W - 2 * M, 1000)
    if y - height < 49:
        raise RuntimeError(f'page {page_number} text overflow: {y - height}')
    paragraph.drawOn(c, M, y - height)
    y -= height + space


def gap(n=8):
    global y
    y -= n


def section(s):
    gap(10)
    text(s, 12, space=7)
    c.setStrokeColor(LINE)
    c.setLineWidth(.6)
    c.line(M, y + 2, W - M, y + 2)
    gap(6)


def title(s, meta):
    text(s, 11.5, space=3)
    text(meta, 8.5, GRAY, space=7)


def detail(label, body):
    text(escape(label), 9.4, BLUE, space=3, leading=13)
    text(escape(body), space=5)


def link(label, url):
    text('<link href="' + escape(url, {'"': '&quot;'}) + '" color="#1858a8">'
         + escape(label) + '</link>', 8.4, space=7)


def footer():
    c.setStrokeColor(LINE)
    c.line(M, 36, W - M, 36)
    c.setFillColor(GRAY)
    c.setFont('Korean', 8)
    c.drawString(M, 23, '한석진  ·  seokjin.han010@gmail.com')
    c.drawRightString(W - M, 23, f'2026.10.18  |  {page_number} / {TOTAL_PAGES}')


def newpage(subtitle):
    global y, page_number
    footer()
    c.showPage()
    page_number += 1
    y = H - M
    text('한석진', 16, space=2)
    text(subtitle, 9, GRAY, space=5)


text('한석진', 29, space=8)
text('문제를 정의하고,<br/>구현과 검증까지 맡는 개발자', 15.2, space=10, leading=23)
text('<link href="mailto:seokjin.han010@gmail.com" color="#1858a8">seokjin.han010@gmail.com</link>  ·  '
     '<link href="https://github.com/hsjni0110" color="#1858a8">GitHub</link>  ·  '
     '<link href="https://velog.io/@hsjni0110/posts" color="#1858a8">Velog</link>', 9.2, space=4)
section('업무 경험')
title('모플 | 백엔드·데이터 파이프라인', '2025.09 - 2026.03 · 수요예측·재고관리 솔루션')
detail('일일 배치 지연의 원인 분석',
       '매일 늘어나는 데이터를 처리하는 배치의 실행 시간이 길어져 원인을 분석했습니다. SQL 실행 계획과 dbt 증분 적재 과정을 살펴보고, Citus Coordinator에 연산이 집중되는 구간과 불필요한 데이터 이동을 확인했습니다.')
detail('분산 테이블 직접 적재 방식 구현',
       '기존 dbt Incremental의 중간 처리 단계를 분석하고, 분산 대상 테이블에 직접 적재하는 Custom Incremental을 구현해 처리 시간을 줄였습니다. 분산 키·조인 조건과 Worker-local 처리 방식도 함께 검토했습니다.')
detail('적재 결과 검증',
       '속도 개선 이후에는 적재 전후 데이터 건수와 업무 규칙을 비교해 결과를 확인했습니다.')
text('PostgreSQL · Citus · dbt · SQL', 8.4, GRAY, space=10)
title('스마트뉴비 | 백엔드 개발', '2024.07 - 2024.12 · 인턴십 매칭 플랫폼 인턴메이트')
detail('공고·맞춤 추천·인증·파일 처리 개발',
       'Java·Spring Boot·MySQL로 대외활동·채용공고 관리 API와 사용자 정보 기반 공고 추천 로직을 개발했습니다. Redis·AWS S3를 활용한 인증과 파일 처리 기능도 구현했습니다.')
detail('반복 코드·테스트 데이터 생성 작업 개선',
       'DTO·Entity 변환의 반복 코드를 줄이기 위해 MapStruct를 도입하고, FixtureMonkey로 테스트 데이터 생성을 간소화했습니다. 주요 API 인수 테스트 작성과 GitHub 코드 리뷰에 참여해 기능 동작을 확인했습니다.')
text('Java · Spring Boot · MySQL · Redis · AWS S3', 8.4, GRAY, space=3)
section('학력·자격')
title('충남대학교 컴퓨터융합학부 | 학사 졸업', '2020.03 - 2026.02')
text('재학 중 백엔드 개발 교육과 팀 프로젝트에 참여했고, 스타트업의 서비스 개발·데이터 처리 업무를 경험했습니다. 졸업 이후에는 제조 도메인 교육과 개인 제품 개발로 관심 영역을 넓히고 있습니다.', size=9.8)
text('SQLD · TOEIC Speaking IH', 9, GRAY)

newpage('프로젝트 · 서비스 소개와 직접 수행한 작업')
section('대표 프로젝트')
title('SpeakText | 소설의 스크립트·음성 생성과 편집', '팀 프로젝트 · 2025년')
text('소설을 등장인물별 대사가 담긴 스크립트와 음성으로 변환하는 서비스입니다. 작가는 생성된 등장인물·목소리·대사 연결을 확인하고 잘못된 부분을 수정할 수 있습니다.', size=9.8, color=GRAY, space=8)
detail('인물 연결 오류와 작가의 직접 수정 기능 도입',
       '긴 원문을 나눠 처리해도 같은 인물이 이어지도록 이전 인물 정보와 인물 ID를 연결했습니다. 하지만 팀원들과 생성 음성을 듣는 과정에서 발화자 연결 오류를 확인했습니다. 팀은 LLM 정확도 개선만으로 오류를 없애기 어렵다고 보고 작가의 검토·수정 기능 도입을 결정했습니다.')
detail('발화자 색 구분 제안과 편집 화면·API 구현',
       '저는 스크립트 생성·인물 동기화·음성 생성을 맡았고, 잘못 연결된 대사를 찾기 위한 색 구분을 제안해 편집 화면과 일괄 수정 API를 구현했습니다. 팀원들은 대사를 찾고 수정하기 편해졌다고 평가했습니다. 이는 내부의 정성적 반응이며, 실제 작가 대상 사용성 시험과 수정 시간 측정은 진행하지 않았습니다.')
link('SpeakText 코드·PR', 'https://github.com/SpeakText/backend')
title('ForgeSync | CNC 설비 기록 재생·분석 도구', '개인 프로젝트 · 2026년')
text('CNC 설비의 하루 기록을 재생하고 작업·멈춤·기록 누락을 확인하는 디지털 트윈 프로젝트입니다. 엔지니어가 정지·가공 시간 변화 구간을 조사하는 상황을 가정해, 당시 상태와 원본 기록을 조회하는 기능을 구현했습니다.', size=9.8, color=GRAY, space=8)
detail('하루 상태 요약에서 관심 구간·원본 기록까지 연결',
       '하루 상태 요약에서 구간을 선택한 뒤 해당 시점의 상태·원본 기록을 확인하는 화면을 구성했습니다. 기획·데이터 설계·백엔드·프런트엔드·검증을 맡았고 AI 코딩 에이전트를 활용했습니다. 도메인 규칙은 직접 정했으며, 실제 현장 사용자의 인터뷰를 바탕으로 한 프로젝트는 아닙니다.')
detail('기록 누락 분리와 가공 시간 중심 판정',
       '기록이 없다는 이유만으로 정지를 확정하지 않았습니다. 미세한 센서 편차가 전체 판정을 좌우하던 방식은 가공 시간 중심으로 바꾸고 센서값은 참고 정보로 제공했습니다. NIST 공개 설비 1대의 하루 기록으로 구현했으며, 정상·불량 정답이 없어 탐지 정확도 개선은 입증하지 못했습니다. 현장 사용성도 미검증입니다.')
link('ForgeSync 코드·설계·평가 기록', 'https://github.com/hsjni0110/forge-sync')
newpage('교육·활동 · 학습 내용과 수행 범위')
section('교육·학내외 활동')
title('UC San Diego Qualcomm Institute | AI 연구 교육', '2025.01 - 2025.02 · 미국 · AI Project 과정 수료')
detail('비라벨 금융 데이터를 활용한 BERT 준지도학습 연구',
       '기존 FinBERT의 최신 금융 데이터 반영 한계를 다루기 위해 Self-training·Pseudo-labeling을 적용했습니다. 비라벨 금융 텍스트에 의사 라벨을 부여해 학습에 활용하고, 신뢰도 임계값과 반복 학습 횟수를 조정했습니다. 5-Fold 교차검증과 문장 임베딩 기반 유사성 분석으로 결과를 살펴보고 연구 방법·실험 결과를 학술 논문으로 정리했습니다.')
title('현대자동차 K-뉴딜 아카데미 HINT | 제조지능화', '현대엔지비 · 2026.07 - 현재 · 2026.10.18 기준 교육 참여 중')
detail('제조 공정·설비·데이터의 이해와 개인 프로젝트 적용',
       '제조 공정과 설비, 제조 데이터가 현장에서 생성되고 활용되는 방식을 학습하고 있습니다. 교육에서 생긴 궁금증을 개인 프로젝트 ForgeSync로 확장해 공개 CNC 기록의 상태 분류·재생·조회 기능을 구현했습니다.')
title('멋쟁이사자처럼 대학생 | 백엔드 운영진', '2025.03 - 2025.12')
detail('교육생의 이해도에 따른 코드 리뷰와 오류 분석 자료 작성',
       '교육생의 GitHub PR을 검토하며 기본 개념이 부족한 경우에는 학습 키워드를 안내하고, 이해도가 높은 경우에는 로그·코드에서 원인을 찾을 수 있는 질문을 남겼습니다. 과제를 빠르게 해결한 교육생에게는 예외 상황과 추가 요구사항을 제시했습니다. 반복되는 질문은 재현 방법·확인 항목·관련 개념을 담은 Wiki로 정리했습니다.')
title('멋쟁이사자처럼 대학생 | 백엔드 교육생', '2024.03 - 2024.12')
detail('백엔드 개발 학습과 팀 프로젝트·창업 관심자 교류',
       '백엔드 교육과 과제, 팀 프로젝트에 참여했습니다. 다른 팀과 창업에 관심 있는 사람들을 만나며 기술적 완성도와 실제 수요가 다를 수 있다는 점을 느꼈습니다. 이 경험은 구현 방법보다 누구의 어떤 문제를 해결하는지 먼저 살피는 계기 중 하나였습니다.')
section('추가 학습 프로젝트')
detail('DB FleetOps | 백업 복원·테이블 확인',
       '백업 파일의 생성 여부를 넘어 임시 DB 복원과 필수 테이블 조회를 확인하는 기능을 구현했습니다. 검증 성공과 정리 실패를 별도로 기록했습니다. 전체 데이터 일치 검증과 복원 실패 경로의 정리 보장은 남은 과제입니다.')
link('DB FleetOps 코드·설계·테스트', 'https://github.com/hsjni0110/db-fleet-ops')
detail('예약 시스템 | 좌석 선점·미결제 예약 해제',
       '결제 중인 좌석을 선점하고 5분 미결제 예약을 해제하는 기능을 구현했습니다. 5분은 학습용 정책입니다. 결제 이벤트 지연과 선점 만료가 겹치는 상황은 당시 고려하지 못했으며, 우선순위 규칙과 충돌 재현 검증이 필요합니다.')
link('예약 시스템 코드·제약조건', 'https://github.com/hsjni0110/ReservationSystem')
assert page_number == TOTAL_PAGES
footer()
c.save()
print(OUT)
