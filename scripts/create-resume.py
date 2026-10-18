from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/han-seokjin-resume.pdf'
pdfmetrics.registerFont(TTFont('Korean','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('LatinBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
W,H=A4
M=45
INK=HexColor('#17191d');GRAY=HexColor('#59616c');BLUE=HexColor('#1858a8');LINE=HexColor('#dde2e8')
c=canvas.Canvas(str(OUT),pagesize=A4)
c.setTitle('한석진 | 공개용 이력서');c.setAuthor('한석진');c.setSubject('업무 경험과 문제 해결 사례')
y=H-M

def text(s,size=9.4,color=INK,space=4,leading=None):
 global y
 st=ParagraphStyle('p',fontName='Korean',fontSize=size,leading=leading or size*1.55,textColor=color,wordWrap=None,splitLongWords=0,allowWidows=0,allowOrphans=0)
 p=Paragraph(s,st);_,h=p.wrap(W-2*M,1000);p.drawOn(c,M,y-h);y-=h+space

def gap(n=8):
 global y;y-=n

def section(s):
 global y
 gap(10);text(s,12,space=7)
 c.setStrokeColor(LINE);c.setLineWidth(.6);c.line(M,y+2,W-M,y+2);gap(6)

def title(s,meta=None):
 text(s,11.5,space=2)
 if meta:text(meta,8.4,GRAY,space=5)

def bullet(label,s):
 text(escape(label),9.4,BLUE,space=2,leading=13)
 text(escape(s),10.2,space=6,leading=15.2)

def link(label,url):
 text('<link href="'+escape(url,{'"':'&quot;'})+'" color="#1858a8">'+escape(label)+'</link>',8.2,space=5)

def footer(n):
 c.setStrokeColor(LINE);c.line(M,36,W-M,36)
 c.setFillColor(GRAY);c.setFont('Korean',8);c.drawString(M,23,'한석진  ·  seokjin.han010@gmail.com')
 c.drawRightString(W-M,23,f'2026.10.18  |  {n} / 2')
 if y<48:raise RuntimeError(f'page {n} overflow: {y}')

def newpage():
 global y
 footer(1);c.showPage();y=H-M
 text('한석진',16,space=2);text('프로젝트 · 구현한 기능과 검증 범위',9,GRAY,space=3)

text('한석진',29,space=8)
text('문제를 정의하고,<br/>구현과 검증까지 맡는 개발자',15.2,space=10,leading=23)
text('<link href="mailto:seokjin.han010@gmail.com" color="#1858a8">seokjin.han010@gmail.com</link>  ·  <link href="https://github.com/hsjni0110" color="#1858a8">GitHub</link>  ·  <link href="https://velog.io/@hsjni0110/posts" color="#1858a8">Velog</link>',9.2,space=4)
section('업무 경험')
title('모플 | 백엔드·데이터 파이프라인', '2025.09 - 2026.03 · 수요예측·재고관리 솔루션')
bullet('일일 데이터 배치 시간 단축', '매일 늘어나는 데이터의 배치 처리 지연 개선.')
bullet('Citus 병목 분석·증분 적재 구현', 'Citus 중앙 노드의 부하 집중·데이터 이동과 SQL·dbt 실행 계획 분석. 분산 테이블 직접 적재용 Custom Incremental 구현.')
bullet('적재 건수·업무 규칙 검증', '적재 전후 건수·업무 규칙 검증. 원인 분석부터 개선안 검토·구현·검증까지 직접 담당.')
text('PostgreSQL · Citus · dbt · SQL',8.4,GRAY,space=8)
title('스마트뉴비 | 백엔드 개발', '2024년 하반기 · 인턴십 매칭 플랫폼 인턴메이트')
bullet('공고·추천·인증 API 개발', '인턴메이트의 대외활동·채용공고, 사용자 정보 기반 추천, 인증·파일 처리 개발.')
bullet('반복 매핑·테스트 데이터 작업 개선', 'MapStruct·FixtureMonkey 도입. 주요 API 인수 테스트 작성과 GitHub 코드 리뷰 참여.')
text('Java · Spring Boot · MySQL · Redis · AWS S3',8.4,GRAY,space=2)
section('대표 프로젝트')
title('SpeakText | 발화자 확인·수정 기능 구현', '팀 프로젝트 · 2025년 · 스크립트 생성·인물 동기화·음성 생성·편집 화면과 API')
bullet('음성 청취로 발화자 연결 오류 확인', '팀원들과 생성 음성을 들으며 대사·발화자 연결 오류 확인. 원문 분할 시 같은 인물의 목소리 변화와 대사 오연결 가능성.')
bullet('작가의 인물·대사 수정 기능 도입', 'LLM 정확도 개선만으로 오류를 없애기 어렵다는 팀의 판단에 따라 검토·수정 기능 도입 결정.')
bullet('발화자 색 구분 제안·화면·API 구현', '스크립트 생성·인물 동기화·음성 생성 담당. 색 구분 개선안 제안과 편집 화면·일괄 수정 API 구현.')
bullet('팀 내부의 대사 탐색·수정 피드백', '색 구분 이후 잘못 연결된 대사를 찾고 수정하기 편해졌다는 반응. 실제 작가 대상 시험·수정 시간 측정은 미실시.')
link('SpeakText 코드·PR', 'https://github.com/SpeakText/backend')
newpage()
section('대표 프로젝트 계속')
title('ForgeSync | 기록 누락·정지 구분과 설비 기록 조회', '개인 프로젝트 · 2026년 · 기획·데이터 설계·백엔드·프런트엔드·검증')
bullet('엔지니어의 설비 구간·원본 기록 조회', '정지·가공 시간 변화 구간과 당시 기록을 조회하는 도구 구현. 아카데미·자료 조사로 가정한 상황이며 현장 인터뷰는 미실시.')
bullet('기록 누락 분리·가공 시간 중심 판정', '기록 누락을 정지에서 제외. 센서 최대 편차 대신 가공 시간 중심으로 판정하고 센서값은 참고 정보로 제공.')
bullet('하루 요약에서 원본 기록까지 연결', '요약 → 구간 선택 → 당시 기록 조회 화면 구성. 기획·데이터·백엔드·프런트엔드·검증 담당, AI 코딩 에이전트 활용.')
bullet('설비 1대·하루 기록으로 검증 범위 제한', 'NIST 공개 CNC 기록 활용. 실제 정상·불량 정답이 없어 탐지 정확도 개선은 미검증. 현장 사용성도 미검증.')
link('ForgeSync 코드·설계·평가 기록', 'https://github.com/hsjni0110/forge-sync')
gap(4)
title('캐릭터와 각자의 일을 함께하는 동시생활 앱', '개인 사이드 프로젝트 · 데스크톱·모바일 개발 중')
bullet('혼자 시작·지속하기 어려운 상황 탐색', '개인 경험에서 출발. 커뮤니티의 유사한 어려움과 함께 공부하는 영상·온라인 작업 공간 활용 사례 관찰.')
bullet('일정 입력에서 캐릭터 동행으로 전환', '캐릭터 곁에서 각자의 일을 하는 방식으로 기획 변경. 입력·조작을 줄이고 함께한 시간에 따라 관계가 쌓이는 앱 개발 중.')
bullet('기존 버전 피드백 수집·새 버전 개발', '기존 버전의 반응과 새 방향의 효과를 구분. 변경 버전은 아직 사용자 검증 전.')
section('추가 문제 해결 사례')
bullet('DB FleetOps · 백업 복원·테이블 확인', '임시 DB 복원·테이블 조회와 정리 실패 기록 구현. 전체 데이터 일치 검증·복원 실패 시 정리 보장은 후속 과제.')
bullet('예약 시스템 · 좌석 선점·미결제 해제', '결제 중 선점과 5분 미결제 만료 구현. 5분은 학습용 정책이며 결제 이벤트 지연과 만료의 충돌은 미해결.')
text('<link href="https://github.com/hsjni0110/db-fleet-ops" color="#1858a8">DB FleetOps</link>  ·  <link href="https://github.com/hsjni0110/ReservationSystem" color="#1858a8">예약 시스템</link>',8.2,space=3)
section('학력과 활동')
text('충남대학교 컴퓨터융합학부 학사 · 2020.03 - 2026.02<br/>현대자동차 HINT 제조지능화 과정 · 2026.07 - 현재<br/>멋쟁이사자처럼 대학생 · 2024년 교육생 / 2025년 백엔드 운영진<br/>UC San Diego Qualcomm Institute AI 연구 교육 프로그램 · 2025.01 - 2025.02',9,space=4)
text('SQLD · TOEIC Speaking IH',8.6,GRAY,space=0)
footer(2);c.save();print(OUT)
