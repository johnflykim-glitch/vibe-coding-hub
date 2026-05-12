from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 한글 폰트 등록
font_paths = [
    "C:/Windows/Fonts/malgun.ttf",
    "C:/Windows/Fonts/NanumGothic.ttf",
]
font_registered = False
for fp in font_paths:
    if os.path.exists(fp):
        pdfmetrics.registerFont(TTFont("Korean", fp))
        font_registered = True
        break

if not font_registered:
    raise RuntimeError("한글 폰트를 찾을 수 없습니다.")

FONT = "Korean"
W, H = A4

doc = SimpleDocTemplate(
    "C:/Users/L2404161/Desktop/도로공사_바이브코딩/업무보고서_2026-01/팀업무보고서_2026년1월.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm,
)

story = []

# ── 헤더 ──────────────────────────────────────────────
title_style = ParagraphStyle("title", fontName=FONT, fontSize=18, leading=26,
                              alignment=1, textColor=colors.HexColor("#1a3a5c"),
                              spaceAfter=2*mm)
sub_style   = ParagraphStyle("sub",   fontName=FONT, fontSize=10, leading=14,
                              alignment=1, textColor=colors.HexColor("#555555"),
                              spaceAfter=4*mm)

story.append(Paragraph("2026년 1월 팀 업무 보고서", title_style))
story.append(Paragraph("도로공사 ○○팀 &nbsp;|&nbsp; 보고일: 2026. 02. 03.", sub_style))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a3a5c")))
story.append(Spacer(1, 6*mm))

# ── 섹션 스타일 ───────────────────────────────────────
sec_title = ParagraphStyle("sec", fontName=FONT, fontSize=13, leading=18,
                            textColor=colors.white, spaceAfter=3*mm)
body_style = ParagraphStyle("body", fontName=FONT, fontSize=10, leading=16,
                             leftIndent=4*mm, spaceAfter=2*mm,
                             textColor=colors.HexColor("#222222"))
bullet_style = ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=16,
                               leftIndent=8*mm, spaceAfter=1.5*mm,
                               textColor=colors.HexColor("#333333"))

def section_header(text):
    data = [[Paragraph(text, sec_title)]]
    t = Table(data, colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#1a3a5c")),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return t

# ── 1. 이번 달 주요 업무 3가지 ────────────────────────
story.append(section_header("1.  이번 달 주요 업무 3가지"))
story.append(Spacer(1, 3*mm))

tasks = [
    ("① 국도 37호선 포장 보수 공사 완료",
     "노후화된 37호선 4.2km 구간 아스팔트 재포장을 완료하였으며, 품질 검사 기준치(평탄성 IRI 2.5 이하) 전 구간 충족."),
    ("② 도로 안전시설물 일제 점검",
     "관할 구역 내 가드레일·반사경·노면표시 등 안전시설물 총 1,240개소 점검 완료. 불량 87개소 즉시 교체 조치."),
    ("③ 동절기 제설 대응 체계 운영",
     "기습 한파(1.12~1.15) 대응으로 24시간 비상 근무 체계 가동. 제설제 총 18톤 살포, 주요 고갯길 통행 두절 없이 정상 운영."),
]

for title, desc in tasks:
    story.append(Paragraph(f"<b>{title}</b>", bullet_style))
    story.append(Paragraph(desc, ParagraphStyle("desc", fontName=FONT, fontSize=9.5,
                                                 leading=15, leftIndent=14*mm,
                                                 textColor=colors.HexColor("#444444"),
                                                 spaceAfter=3*mm)))

story.append(Spacer(1, 2*mm))

# ── 2. 진행 중 이슈 ──────────────────────────────────
story.append(section_header("2.  진행 중 이슈"))
story.append(Spacer(1, 3*mm))

issues = [
    ("● 교량 신축이음 균열 발생 (지방도 318호선 2교)",
     "원인 분석 중이며, 안전 펜스 설치 완료. 정밀 안전 진단 업체 2월 초 투입 예정."),
    ("● 민원 증가 — 야간 공사 소음",
     "인근 주민 민원 3건 접수. 야간 작업 시간 23시 이전 종료 및 방음벽 임시 설치로 협의 진행 중."),
]

for title, desc in issues:
    story.append(Paragraph(f"<b>{title}</b>", bullet_style))
    story.append(Paragraph(desc, ParagraphStyle("desc2", fontName=FONT, fontSize=9.5,
                                                  leading=15, leftIndent=14*mm,
                                                  textColor=colors.HexColor("#444444"),
                                                  spaceAfter=3*mm)))

story.append(Spacer(1, 2*mm))

# ── 3. 다음 달 계획 ──────────────────────────────────
story.append(section_header("3.  다음 달 계획"))
story.append(Spacer(1, 3*mm))

plans = [
    "교량 정밀 안전 진단 및 결과 보고 (2월 14일까지)",
    "봄철 해빙기 도로 취약 구간 사전 점검 (전 구간)",
    "도로 안전시설물 보수 공사 발주 (불량 87개소)",
    "상반기 정기 교육 — 현장 안전 관리 (2월 마지막 주)",
]

for p in plans:
    story.append(Paragraph(f"▸  {p}", bullet_style))

story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaaaaa")))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("본 보고서는 내부 공유용이며 무단 배포를 금합니다.",
                        ParagraphStyle("footer", fontName=FONT, fontSize=8,
                                       alignment=1, textColor=colors.HexColor("#999999"))))

doc.build(story)
print("PDF 생성 완료!")
