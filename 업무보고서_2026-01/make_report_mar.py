from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

for fp in ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/NanumGothic.ttf"]:
    if os.path.exists(fp):
        pdfmetrics.registerFont(TTFont("Korean", fp))
        break

FONT = "Korean"

doc = SimpleDocTemplate(
    "C:/Users/L2404161/Desktop/도로공사_바이브코딩/업무보고서_2026-01/팀업무보고서_2026년3월.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm,
)

story = []

title_style = ParagraphStyle("title", fontName=FONT, fontSize=18, leading=26,
                              alignment=1, textColor=colors.HexColor("#1a3a5c"), spaceAfter=2*mm)
sub_style   = ParagraphStyle("sub",   fontName=FONT, fontSize=10, leading=14,
                              alignment=1, textColor=colors.HexColor("#555555"), spaceAfter=4*mm)

story.append(Paragraph("2026년 3월 팀 업무 보고서", title_style))
story.append(Paragraph("도로공사 ○○팀 &nbsp;|&nbsp; 보고일: 2026. 04. 02.", sub_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a3a5c")))
story.append(Spacer(1, 6*mm))

sec_title  = ParagraphStyle("sec",    fontName=FONT, fontSize=13, leading=18, textColor=colors.white)
bullet_sty = ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=16, leftIndent=8*mm,
                              textColor=colors.HexColor("#333333"), spaceAfter=1.5*mm)
desc_sty   = ParagraphStyle("desc",   fontName=FONT, fontSize=9.5, leading=15, leftIndent=14*mm,
                              textColor=colors.HexColor("#444444"), spaceAfter=3*mm)

def section_header(text):
    t = Table([[Paragraph(text, sec_title)]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#1a3a5c")),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    return t

# ── 1. 이번 달 주요 업무 3가지 ───────────────────────
story.append(section_header("1.  이번 달 주요 업무 3가지"))
story.append(Spacer(1, 3*mm))

tasks = [
    ("① 318호선 2교 긴급 보수 공사 착공",
     "예산 승인(3.10) 이후 즉시 착공. 신축이음 전면 교체 및 상판 균열부 에폭시 주입 완료."
     " 잔여 공정(교면 방수·포장)은 4월 2주차 완공 예정으로 공정률 68% 달성."),
    ("② 봄철 도로 파손 긴급 보수 순찰반 운영",
     "해빙기 포트홀 집중 발생 구간(총 23개소) 파악 후 순찰반 2개 조 편성."
     " 3월 한 달간 긴급 패칭 작업 총 41건 완료, 민원 대응 평균 2시간 이내 처리."),
    ("③ 상반기 도로 유지관리 종합 계획 수립 완료",
     "관할 구역 전 노선 유지보수 우선순위 분류 및 예산 배분 계획 확정."
     " 총 사업비 12억 4천만 원 규모, 본부 보고 완료(3.28)."),
]
for title, desc in tasks:
    story.append(Paragraph(f"<b>{title}</b>", bullet_sty))
    story.append(Paragraph(desc, desc_sty))

story.append(Spacer(1, 2*mm))

# ── 2. 진행 중 이슈 ─────────────────────────────────
story.append(section_header("2.  진행 중 이슈"))
story.append(Spacer(1, 3*mm))

issues = [
    ("● 국도 45호선 3.8km 비탈면 침하 지속 관찰 중",
     "월간 누적 변위량 17mm로 임계치(20mm) 근접. 강우량 증가 예상되는 4월 초 전후 통제 여부 결정 예정."
     " 주민 사전 안내 문자 1차 발송 완료."),
    ("● 안전시설물 보수 공사 일부 지연",
     "낙찰 업체 자재 수급 문제로 87개소 중 31개소 미착공 상태."
     " 업체 측 4월 15일 완료 확약서 징구 및 이행 보증금 조항 적용 검토 중."),
]
for title, desc in issues:
    story.append(Paragraph(f"<b>{title}</b>", bullet_sty))
    story.append(Paragraph(desc, desc_sty))

story.append(Spacer(1, 2*mm))

# ── 3. 다음 달 계획 ─────────────────────────────────
story.append(section_header("3.  다음 달 계획"))
story.append(Spacer(1, 3*mm))

plans = [
    "318호선 2교 보수 공사 완공 및 준공 검사 (4월 2주차)",
    "45호선 비탈면 정밀 점검 및 통제 여부 최종 결정 (4월 초)",
    "안전시설물 보수 공사 잔여 31개소 완료 독촉 및 현장 확인",
    "상반기 유지관리 공사 1차 발주 (포장 보수 5개 노선)",
    "팀 내 안전 교육 실시 — 산업 안전 보건법 개정 내용 (4월 3주차)",
]
for p in plans:
    story.append(Paragraph(f"▸  {p}", bullet_sty))

story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaaaaa")))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("본 보고서는 내부 공유용이며 무단 배포를 금합니다.",
                        ParagraphStyle("footer", fontName=FONT, fontSize=8,
                                       alignment=1, textColor=colors.HexColor("#999999"))))

doc.build(story)
print("3월 PDF 생성 완료!")
