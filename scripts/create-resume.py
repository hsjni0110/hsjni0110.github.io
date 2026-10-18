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
 text('<font color="#1858a8">'+escape(label)+'</font> '+escape(s),10.2,space=6)

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
bullet('결과', '매일 늘어나는 데이터를 처리하는 배치의 실행 시간 단축')
bullet('분석·구현', 'SQL 실행 계획·dbt 증분 적재 분석, Citus 중앙 노드의 부하 집중·불필요한 데이터 이동 검토. 분산 테이블에 직접 적재하는 Custom Incremental 구현.')
bullet('검증·담당 범위', '적재 전후 건수·업무 규칙 검증. 병목 분석부터 개선안 검토·구현·결과 검증까지 직접 담당.')
text('PostgreSQL · Citus · dbt · SQL',8.4,GRAY,space=8)
title('스마트뉴비 | 백엔드 개발', '2024년 하반기 · 인턴십 매칭 플랫폼 인턴메이트')
bullet('구현', '대외활동·채용공고 관리 API, 사용자 정보 기반 추천, 인증·파일 처리 기능 개발.')
bullet('반복 작업 개선', 'MapStruct·FixtureMonkey 도입을 통한 반복 작업 감소. 주요 API 인수 테스트 작성과 GitHub 코드 리뷰 참여.')
text('Java · Spring Boot · MySQL · Redis · AWS S3',8.4,GRAY,space=2)
section('대표 프로젝트')
title('SpeakText | 발화자 확인·수정 기능 구현', '팀 프로젝트 · 2025년 · 스크립트 생성·인물 동기화·음성 생성·편집 화면과 API')
bullet('문제', '생성된 음성을 팀원들과 들으며 발화자 연결 오류 확인. 같은 인물의 목소리가 바뀌거나 대사가 다른 인물에게 연결될 경우 청자의 혼란 가능성.')
bullet('판단', 'LLM 정확도 개선만으로 오류를 없애기 어렵다는 팀의 판단. 작가의 등장인물·대사 확인·수정 기능 도입 결정.')
bullet('직접 기여', '스크립트 생성·등장인물 동기화·음성 생성 담당. 잘못 연결된 대사를 찾기 위한 발화자별 색 구분 제안, 화면·일괄 수정 API 구현.')
bullet('결과', '색 구분 이후 잘못 연결된 대사의 탐색·수정이 편해졌다는 팀 내부 피드백. 실제 작가 대상 사용성 시험과 수정 시간 측정은 미실시.')
link('SpeakText 코드·PR', 'https://github.com/SpeakText/backend')
newpage()
section('대표 프로젝트 계속')
title('ForgeSync | 기록 누락·정지 구분과 설비 기록 조회', '개인 프로젝트 · 2026년 · 기획·데이터 설계·백엔드·프런트엔드·검증')
bullet('구현·대상', '설비의 정지·가공 시간 변화 구간과 당시 원본 기록을 조회하는 도구 구현. 아카데미·자료 조사로 가정한 엔지니어의 조사 상황이며, 현장 인터뷰는 미실시.')
bullet('판단·구현', '기록 누락과 실제 정지의 분리. 작은 센서 편차가 전체 판정을 좌우하던 방식에서 가공 시간 중심의 판정으로 변경. 센서값은 참고 정보로 제공.')
bullet('화면·담당 범위', '하루 상태 요약 → 구간 선택 → 당시 기록 확인 순서의 화면 구성. 기획·데이터 설계·백엔드·프런트엔드·검증 담당, AI 코딩 에이전트 활용.')
bullet('검증 범위', 'NIST 공개 CNC 설비 1대의 하루 기록 활용. 실제 정상·불량 정답이 없어 탐지 정확도 개선은 미검증. 현장 사용성도 미검증.')
link('ForgeSync 코드·설계·평가 기록', 'https://github.com/hsjni0110/forge-sync')
gap(4)
title('캐릭터와 각자의 일을 함께하는 동시생활 앱', '개인 사이드 프로젝트 · 데스크톱·모바일 개발 중')
bullet('출발점', '혼자서는 할 일을 알아도 시작하고 이어가기 어려웠던 개인 경험. 커뮤니티의 유사한 어려움과 함께 공부하는 영상·온라인 작업 공간 활용 사례 관찰.')
bullet('기획 전환', '일정 입력·AI 대화 중심에서 캐릭터 곁에서 각자의 일을 하는 방식으로 변경. 입력·조작을 줄이고 함께한 시간에 따라 관계가 쌓이는 앱 개발 중.')
bullet('현재 단계', '기존 버전의 테스터 피드백 수집 후 기획 변경. 새 방향은 개발 중이며 아직 사용자 검증 전.')
section('추가 문제 해결 사례')
bullet('DB FleetOps', '백업 파일의 임시 DB 복원·필수 테이블 확인 구현, 정리 실패의 별도 기록. 전체 데이터 일치 검증과 복원 실패 시 정리 보장은 후속 과제.')
bullet('예약 시스템', '결제 중 좌석 선점과 5분 미결제 예약 해제 구현. 5분은 학습용 정책이며, 결제 이벤트 지연과 만료의 충돌은 미해결.')
text('<link href="https://github.com/hsjni0110/db-fleet-ops" color="#1858a8">DB FleetOps</link>  ·  <link href="https://github.com/hsjni0110/ReservationSystem" color="#1858a8">예약 시스템</link>',8.2,space=3)
section('학력과 활동')
text('충남대학교 컴퓨터융합학부 학사 · 2020.03 - 2026.02<br/>현대자동차 HINT 제조지능화 과정 · 2026.07 - 현재<br/>멋쟁이사자처럼 대학생 · 2024년 교육생 / 2025년 백엔드 운영진<br/>UC San Diego Qualcomm Institute AI 연구 교육 프로그램 · 2025.01 - 2025.02',9,space=4)
text('SQLD · TOEIC Speaking IH',8.6,GRAY,space=0)
footer(2);c.save();print(OUT)
