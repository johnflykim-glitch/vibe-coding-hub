from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

font_paths = [
    "C:/Windows/Fonts/malgun.ttf",
    "C:/Windows/Fonts/NanumGothic.ttf",
]
for fp in font_paths:
    if os.path.exists(fp):
        pdfmetrics.registerFont(TTFont("Korean", fp))
        break

FONT = "Korean"

doc = SimpleDocTemplate(
    "C:/Users/L2404161/Desktop/도로공사_바이브코딩/업무보고서_2026-01/팀업무보고서_2026년2월.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm,
)

story = []

title_style = ParagraphStyle("title", fontName=FONT, fontSize=18, leading=26,
                              alignment=1, textColor=colors.HexColor("#1a3a5c"), spaceAfter=2*mm)
sub_style   = ParagraphStyle("sub",   fontName=FONT, fontSize=10, leading=14,
                              alignment=1, textColor=colors.HexColor("#555555"), spaceAfter=4*mm)

story.append(Paragraph("2026년 2월 팀 업무 보고서", title_style))
story.append(Paragraph("도로공사 ○○팀 &nbsp;|&nbsp; 보고일: 2026. 03. 03.", sub_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a3a5c")))
story.append(Spacer(1, 6*mm))

sec_title  = ParagraphStyle("sec",    fontName=FONT, fontSize=13, leading=18, textColor=colors.white, spaceAfter=3*mm)
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
    ("① 교량 정밀 안전 진단 완료 (지방도 318호선 2교)",
     "외부 전문 업체 투입을 통해 교량 신축이음부 균열 원인 규명. D등급 판정에 따라 긴급 보수 공사 설계 발주 착수."),
    ("② 해빙기 도로 취약 구간 사전 점검",
     "관할 내 비탈면·절개지 등 취약 구간 62개소 전수 점검 완료. 이상 구간 9개소에 대해 위험 표지 설치 및 모니터링 카메라 증설."),
    ("③ 도로 안전시설물 보수 공사 발주",
     "1월 점검에서 불량 판정된 87개소 보수 공사 입찰 공고 완료. 낙찰 업체 선정 후 3월 중 착공 예정."),
]
for title, desc in tasks:
    story.append(Paragraph(f"<b>{title}</b>", bullet_sty))
    story.append(Paragraph(desc, desc_sty))

story.append(Spacer(1, 2*mm))

# ── 2. 진행 중 이슈 ─────────────────────────────────
story.append(section_header("2.  진행 중 이슈"))
story.append(Spacer(1, 3*mm))

issues = [
    ("● 318호선 2교 긴급 보수 예산 확보 지연",
     "긴급 보수 설계비 약 3,200만 원 추가 예산 요청 중. 본부 승인 지연으로 공사 일정 2~3주 밀릴 가능성 있으며 지속 모니터링."),
    ("● 비탈면 침하 진행 중 — 국도 45호선 3.8km 지점",
     "계측기 설치 완료, 일 2회 데이터 수집 중. 변위량 임계치(20mm) 미달이나 강우 시 통제 기준 사전 수립."),
]
for title, desc in issues:
    story.append(Paragraph(f"<b>{title}</b>", bullet_sty))
    story.append(Paragraph(desc, desc_sty))

story.append(Spacer(1, 2*mm))

# ── 3. 다음 달 계획 ─────────────────────────────────
story.append(section_header("3.  다음 달 계획"))
story.append(Spacer(1, 3*mm))

plans = [
    "318호선 2교 긴급 보수 공사 착공 (예산 승인 시 3월 2주차)",
    "안전시설물 보수 공사 착공 및 공정 관리",
    "봄철 도로 파손 긴급 보수 반 편성 및 순찰 강화",
    "상반기 도로 유지관리 종합 계획 수립 (3월 말 보고 목표)",
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
print("2월 PDF 생성 완료!")
