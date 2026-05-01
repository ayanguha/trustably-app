from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line, Polygon, Wedge
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics import renderPDF
from reportlab.platypus.flowables import Flowable
import math
import pandas as pd

# ── LOAD SUGGESTED ACTIONS FROM XLSX ──────────────────────────────────────────
def load_actions(xlsx_path):
    df = pd.read_excel(xlsx_path, sheet_name="Curated Suggested actions")
    df['trait_clean']    = df['trait'].str.strip()
    df['subtrait_clean'] = df['sub-Trait'].str.strip()
    df['subtrait_name']  = df['subtrait_clean'].str.split(' - ').str[-1].str.strip()
    return df


# ── BRAND COLOURS ──────────────────────────────────────────────────────────────
C_DARK    = colors.HexColor('#1A1A2E')   # dark navy
C_PRIMARY = colors.HexColor('#C1694F')   # trustably orange-red
C_GREEN   = colors.HexColor('#4A7C59')   # trustably green
C_AMBER   = colors.HexColor('#D4A843')   # amber highlight
C_LIGHT   = colors.HexColor('#F5F0E8')   # warm off-white
C_MID     = colors.HexColor('#E8E0D0')   # mid tone
C_GRAY    = colors.HexColor('#666666')   # body text gray
C_LGRAY   = colors.HexColor('#AAAAAA')   # light gray
C_WHITE   = colors.white

W, H = A4

FOCUS_ORDER = {
    'Functional Governance': 0,
    'Observability': 1,
    'Culture': 2,
    'Unified Platform': 3,
    'Security': 4
    }

CARE_ORDER = {
    'Consistent': 0,
    'Accurate': 1,
    'Reliable': 2,
    'Effective': 3 
}

# ── SAMPLE DATA ────────────────────────────────────────────────────────────────
ORG_NAME  = "Acme Technologies Pty Ltd"
REPORT_DT = "April 2026"
ASSESSOR  = "Trustably Framework v1.0"

FOCUS_SCORES = {
    'Functional\nGovernance': 6.4,
    'Observability':          4.8,
    'Culture':                3.9,
    'Unified\nPlatform':      6.1,
    'Security':               5.2,
}
OVERALL = round(sum(FOCUS_SCORES.values()) / len(FOCUS_SCORES), 1)

CELL_SCORES = {
    # (care, focus): score
    ('Consistent',    'Functional Governance'): 4, ('Consistent',    'Observability'): 3, ('Consistent',    'Culture'): 2, ('Consistent',    'Unified Platform'): 3, ('Consistent',    'Security'): 2,
    ('Accurate',     'Functional Governance'): 7, ('Accurate',     'Observability'): 5, ('Accurate',     'Culture'): 4, ('Accurate',     'Unified Platform'): 7, ('Accurate',     'Security'): 5,
    ('Reliable', 'Functional Governance'): 8, ('Reliable', 'Observability'): 7, ('Reliable', 'Culture'): 6, ('Reliable', 'Unified Platform'): 8, ('Reliable', 'Security'): 7,
    ('Effective',    'Functional Governance'): 9, ('Effective',    'Observability'): 7, ('Effective',    'Culture'): 6, ('Effective',    'Unified Platform'): 9, ('Effective',    'Security'): 7,
}

CARE_SCORES = {
    'Consistent':  {'Strategic':6.5, 'Viable':5.8, 'Resilient':4.2},
    'Accurate':    {'Valid':6.1, 'Unbiased':4.9, 'Explainable':5.3, 'Integrated':5.7},
    'Reliable':    {'Observable':4.8, 'Transparent':5.9, 'Accountable':6.2, 'Interoperable':4.4},
    'Effective':   {'Desirable':6.8, 'Secure':5.2, 'Context-Aware':4.7, 'Safe':5.1},
}

GAPS = [
    ("Culture × Observability",        "Experiment", "Enable",  "HIGH",   "Implement enterprise AI literacy programme; define monitoring awareness standards"),
    ("Security × Culture",             "Experiment", "Enable",  "HIGH",   "Deploy AI-specific security training; establish data classification awareness"),
    ("Observability × Unified Platform","Experiment", "Enable",  "MEDIUM", "Standardise logging and tracing across platform; centralise metrics dashboard"),
    ("Culture × Functional Governance", "Experiment", "Enable",  "MEDIUM", "Embed governance education into onboarding; link policy to engineering workflow"),
    ("Security × Observability",        "Enable",    "Embrace", "LOW",    "Automate security observability; integrate threat detection into monitoring stack"),
]

ROADMAP = [
    ("1–4 weeks",  "Immediate",  C_PRIMARY, [
        "Launch AI literacy baseline assessment across all teams",
        "Appoint AI governance lead with cross-functional mandate",
        "Audit current AI tool inventory and classify data exposure risk",
        "Define and document decision rights for AI agent actions",
    ]),
    ("1–3 months", "Short-term", C_GREEN, [
        "Deploy enterprise-wide AI awareness training programme",
        "Implement centralised logging and metrics platform",
        "Formalise AI risk assessment process aligned to NIST AI RMF",
        "Establish data classification framework for AI workloads",
        "Standardise MLOps pipeline across all production AI systems",
    ]),
    ("3–12 months","Strategic",  C_AMBER, [
        "Achieve Enable-level maturity across Culture and Security pillars",
        "Integrate AI governance controls into CI/CD delivery pipeline",
        "Deploy automated bias and drift detection across all models",
        "Implement agentic AI authorisation framework with audit trail",
        "Begin Embrace-level capability development in Platform and Governance",
    ]),
]

# ── STYLES ─────────────────────────────────────────────────────────────────────
def styles():
    return {
        'cover_title': ParagraphStyle('ct', fontName='Helvetica-Bold',   fontSize=32, textColor=C_WHITE,   leading=40, spaceAfter=8),
        'cover_sub':   ParagraphStyle('cs', fontName='Helvetica',        fontSize=14, textColor=C_AMBER,   leading=20, spaceAfter=4),
        'cover_body':  ParagraphStyle('cb', fontName='Helvetica',        fontSize=11, textColor=C_MID,     leading=16),
        'h1':          ParagraphStyle('h1', fontName='Helvetica-Bold',   fontSize=18, textColor=C_DARK,    leading=24, spaceBefore=18, spaceAfter=8),
        'h2':          ParagraphStyle('h2', fontName='Helvetica-Bold',   fontSize=13, textColor=C_PRIMARY, leading=18, spaceBefore=14, spaceAfter=6),
        'h3':          ParagraphStyle('h3', fontName='Helvetica-Bold',   fontSize=11, textColor=C_GREEN,   leading=15, spaceBefore=10, spaceAfter=4),
        'body':        ParagraphStyle('bd', fontName='Helvetica',        fontSize=10, textColor=C_DARK,    leading=15, spaceAfter=4),
        'small':       ParagraphStyle('sm', fontName='Helvetica',        fontSize=8,  textColor=C_DARK,   leading=12),
        'label':       ParagraphStyle('lb', fontName='Helvetica-Bold',   fontSize=9,  textColor=C_DARK,    leading=13),
        'caption':     ParagraphStyle('cp', fontName='Helvetica-Oblique',fontSize=9,  textColor=C_GRAY,   leading=11, spaceAfter=6),
        'white_h2':    ParagraphStyle('wh', fontName='Helvetica-Bold',   fontSize=13, textColor=C_WHITE,   leading=18),
        'white_body':  ParagraphStyle('wb', fontName='Helvetica',        fontSize=10, textColor=C_MID,     leading=15),
        'band_label':  ParagraphStyle('bl', fontName='Helvetica-Bold',   fontSize=10, textColor=C_WHITE,   leading=14),
        'toc':         ParagraphStyle('tc', fontName='Helvetica',        fontSize=11, textColor=C_DARK,    leading=20),
        'toc_num':     ParagraphStyle('tn', fontName='Helvetica-Bold',   fontSize=11, textColor=C_PRIMARY, leading=20),
    }

S = styles()

# ── HELPERS ────────────────────────────────────────────────────────────────────
def score_color(s):
    if s >= 7: return C_GREEN
    if s >= 5: return C_AMBER
    return C_PRIMARY

def band_label(s):
    if s >= 9: return "EMBRACE"
    if s >= 6: return "ENABLE"
    if s >= 3: return "EXPERIMENT"
    return "EXPLORE"

def hr(color=C_MID, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

# ── CUSTOM FLOWABLES ───────────────────────────────────────────────────────────

class CoverPage(Flowable):
    def __init__(self, w, h):
        Flowable.__init__(self)
        self.width = w
        self.height = h

    def draw(self):
        c = self.canv
        # Dark background
        c.setFillColor(C_DARK)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # Orange accent bar left
        c.setFillColor(C_PRIMARY)
        c.rect(0, 0, 8*mm, self.height, fill=1, stroke=0)
        # Green accent bar left (thin)
        c.setFillColor(C_GREEN)
        c.rect(8*mm, 0, 3*mm, self.height, fill=1, stroke=0)
        # Light grid pattern (subtle)
        c.setStrokeColor(colors.HexColor('#2A2A4E'))
        c.setLineWidth(0.3)
        for x in range(20, int(self.width), 28):
            c.line(x, 0, x, self.height)
        for y in range(0, int(self.height), 28):
            c.line(20, y, self.width, y)
        # Big score circle
        cx, cy = self.width - 55*mm, 95*mm
        r = 32*mm
        c.setFillColor(colors.HexColor('#252545'))
        c.circle(cx, cy, r, fill=1, stroke=0)
        c.setStrokeColor(C_PRIMARY)
        c.setLineWidth(3)
        c.circle(cx, cy, r, fill=0, stroke=1)
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 36)
        c.drawCentredString(cx, cy + 8, f"{OVERALL}")
        c.setFont('Helvetica', 11)
        c.setFillColor(C_LGRAY)
        c.drawCentredString(cx, cy - 10, "/ 10.0  Overall")
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(score_color(OVERALL))
        lbl = band_label(OVERALL)
        c.drawCentredString(cx, cy - 26, lbl)
        # Title block
        tx = 20*mm
        c.setFillColor(C_PRIMARY)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(tx, 230*mm, "TRUSTABLY  ·  APPLIED AI ADOPTION FRAMEWORK")
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 30)
        c.drawString(tx, 200*mm, "AI Adoption")
        c.drawString(tx, 170*mm, "Assessment")
        c.setFont('Helvetica-Bold', 30)
        c.setFillColor(C_PRIMARY)
        c.drawString(tx, 140*mm, "Report")
        # Org details
        c.setFillColor(C_MID)
        c.setFont('Helvetica', 12)
        c.drawString(tx, 120*mm, ORG_NAME)
        c.setFont('Helvetica', 10)
        c.setFillColor(C_LGRAY)
        c.drawString(tx, 112*mm, f"Assessment Period: {REPORT_DT}")
        c.drawString(tx, 104*mm, f"Framework: {ASSESSOR}")
        # Footer bar
        c.setFillColor(C_PRIMARY)
        c.rect(0, 0, self.width, 18*mm, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica', 8)
        c.drawString(tx, 8*mm, "CONFIDENTIAL  ·  trustably.super.site  ·  © 2026 Trustably AI Adoption Framework")
        # Focus area mini scores
        focuses = list(FOCUS_SCORES.items())
        bx = tx
        by = 38*mm
        bw = 28*mm
        for i, (name, score) in enumerate(focuses):
            bx2 = tx + i * (bw + 4*mm)
            c.setFillColor(colors.HexColor('#252545'))
            c.roundRect(bx2, by, bw, 22*mm, 3*mm, fill=1, stroke=0)
            c.setFillColor(score_color(score))
            c.setFont('Helvetica-Bold', 14)
            c.drawCentredString(bx2 + bw/2, by + 13*mm, f"{score}")
            c.setFillColor(C_LGRAY)
            c.setFont('Helvetica', 7)
            label = name.replace('\n', ' ')
            c.drawCentredString(bx2 + bw/2, by + 5*mm, label[:14])

    def wrap(self, *args):
        return self.width, self.height


class RadarChart(Flowable):
    def __init__(self, size=120):
        Flowable.__init__(self)
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        labels = ['F.Gov', 'Observ.', 'Culture', 'U.Plat.', 'Security']
        values = [FOCUS_SCORES[k] for k in FOCUS_SCORES]
        n = len(labels)
        cx = self.size / 2
        cy = self.size / 2
        r_max = self.size / 2 - 18
        # Grid rings
        for ring in [2, 4, 6, 8, 10]:
            pts = []
            for i in range(n):
                angle = math.pi/2 + 2*math.pi*i/n
                rx = cx + r_max * (ring/10) * math.cos(angle)
                ry = cy + r_max * (ring/10) * math.sin(angle)
                pts.append((rx, ry))
            c.setStrokeColor(C_MID)
            c.setLineWidth(0.4)
            path = c.beginPath()
            path.moveTo(pts[0][0], pts[0][1])
            for px, py in pts[1:]:
                path.lineTo(px, py)
            path.close()
            c.drawPath(path)
        # Spokes
        for i in range(n):
            angle = math.pi/2 + 2*math.pi*i/n
            c.setStrokeColor(C_LGRAY)
            c.setLineWidth(0.4)
            c.line(cx, cy, cx + r_max * math.cos(angle), cy + r_max * math.sin(angle))
        # Score polygon
        pts = []
        for i, v in enumerate(values):
            angle = math.pi/2 + 2*math.pi*i/n
            rx = cx + r_max * (v/10) * math.cos(angle)
            ry = cy + r_max * (v/10) * math.sin(angle)
            pts.append((rx, ry))
        c.setFillColor(colors.HexColor('#4A7C5940'))
        c.setStrokeColor(C_GREEN)
        c.setLineWidth(1.5)
        path = c.beginPath()
        path.moveTo(pts[0][0], pts[0][1])
        for px, py in pts[1:]:
            path.lineTo(px, py)
        path.close()
        c.drawPath(path, fill=1, stroke=1)
        # Dots
        for px, py in pts:
            c.setFillColor(C_GREEN)
            c.circle(px, py, 2.5, fill=1, stroke=0)
        # Labels
        for i, label in enumerate(labels):
            angle = math.pi/2 + 2*math.pi*i/n
            lx = cx + (r_max + 12) * math.cos(angle)
            ly = cy + (r_max + 12) * math.sin(angle)
            c.setFillColor(C_DARK)
            c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(lx, ly - 3, label)

    def wrap(self, *args):
        return self.size, self.size


class ScoreBar(Flowable):
    """Horizontal score bar with band zones."""
    def __init__(self, label, score, width=160*mm, height=10*mm):
        Flowable.__init__(self)
        self.label = label
        self.score = score
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        bw = self.width - 50*mm
        bh = 5*mm
        by = (self.height - bh) / 2
        bx = 48*mm
        # Label
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(C_DARK)
        c.drawRightString(46*mm, by + 1.5*mm, self.label)
        # Background zones
        zones = [(0, 0.2, C_PRIMARY), (0.2, 0.5, C_AMBER), (0.5, 0.8, C_GREEN), (0.8, 1.0, colors.HexColor('#2E6B3E'))]
        for start, end, col in zones:
            c.setFillColor(colors.HexColor(col.hexval() + '40') if hasattr(col, 'hexval') else col)
            c.rect(bx + start*bw, by, (end-start)*bw, bh, fill=1, stroke=0)
        # Filled portion
        fill_w = (self.score/10) * bw
        c.setFillColor(score_color(self.score))
        c.rect(bx, by, fill_w, bh, fill=1, stroke=0)
        # Border
        c.setStrokeColor(C_MID)
        c.setLineWidth(0.5)
        c.rect(bx, by, bw, bh, fill=0, stroke=1)
        # Score label
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(C_DARK)
        c.drawString(bx + bw + 4*mm, by + 1.5*mm, f"{self.score:.1f}  {band_label(self.score)}")

    def wrap(self, *args):
        return self.width, self.height


class HeatmapCell(Flowable):
    def __init__(self, stages, focuses, cell_scores, w=145*mm, h=90*mm):
        Flowable.__init__(self)
        self.stages = stages
        self.focuses = focuses
        self.cell_scores = cell_scores
        self.width = w
        self.height = h

    def draw(self):
        c = self.canv
        n_stages = len(self.stages)
        n_focus  = len(self.focuses)
        header_h = 14*mm
        label_w  = 22*mm
        cell_w   = (self.width - label_w) / n_focus
        cell_h   = (self.height - header_h) / n_stages

        # Column headers
        for j, f in enumerate(self.focuses):
            x = label_w + j*cell_w
            c.setFillColor(C_DARK)
            c.rect(x, self.height - header_h, cell_w - 1, header_h - 1, fill=1, stroke=0)
            c.setFillColor(C_WHITE)
            c.setFont('Helvetica-Bold', 6.5)
            c.drawCentredString(x + cell_w/2, self.height - header_h + 5, f)

        # Rows
        for i, stage in enumerate(self.stages):
            y = self.height - header_h - (i+1)*cell_h
            # Row label
            c.setFillColor(C_DARK)
            c.rect(0, y, label_w - 1, cell_h - 1, fill=1, stroke=0)
            c.setFillColor(C_WHITE)
            c.setFont('Helvetica-Bold', 7.5)
            c.drawCentredString(label_w/2, y + cell_h/2 - 3, stage)
            # Cells
            for j, focus in enumerate(self.focuses):
                key = (stage, focus)
                score = self.cell_scores.get(key, 5)
                x = label_w + j*cell_w
                # Cell fill
                alpha_hex = ['20','35','55','75','88','99','AA','BB','CC','DD','EE'][min(score, 10)]
                fill_col = score_color(score)
                c.setFillColor(fill_col)
                c.rect(x, y, cell_w-1, cell_h-1, fill=1, stroke=0)
                # Score text
                c.setFillColor(C_WHITE if score >= 5 else C_DARK)
                c.setFont('Helvetica-Bold', 9)
                c.drawCentredString(x + cell_w/2, y + cell_h/2 - 3, str(score))
                # Band
                c.setFont('Helvetica', 5.5)
                c.drawCentredString(x + cell_w/2, y + 2, band_label(score)[:3])

    def wrap(self, *args):
        return self.width, self.height


class PageHeader(Flowable):
    def __init__(self, section_title, page_w=A4[0]):
        Flowable.__init__(self)
        self.title = section_title
        self.width = page_w - 30*mm
        self.height = 12*mm

    def draw(self):
        c = self.canv
        c.setFillColor(C_DARK)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFillColor(C_PRIMARY)
        c.rect(0, 0, 4*mm, self.height, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(8*mm, 4*mm, self.title)
        c.setFillColor(C_LGRAY)
        c.setFont('Helvetica', 8)
        c.drawRightString(self.width - 20*mm, 4*mm, f"{ORG_NAME}  ·  {REPORT_DT}")

    def wrap(self, *args):
        return self.width, self.height


class CareBar(Flowable):
    def __init__(self, trait, sub_scores, w=170*mm, h=28*mm):
        Flowable.__init__(self)
        self.trait = trait
        self.sub_scores = sub_scores
        self.width = w
        self.height = h

    def draw(self):
        c = self.canv
        n = len(self.sub_scores)
        bar_w = (self.width - 32*mm) / n
        # Trait label
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(0, self.height/2 - 3, self.trait)
        bx = 32*mm
        for i, (sub, score) in enumerate(self.sub_scores.items()):
            x = bx + i * bar_w
            bh = (score / 10) * (self.height - 10*mm)
            by = 8*mm
            # Background
            c.setFillColor(C_MID)
            c.rect(x + 1, by, bar_w - 4, self.height - 10*mm, fill=1, stroke=0)
            # Fill
            c.setFillColor(score_color(score))
            c.rect(x + 1, by, bar_w - 4, bh, fill=1, stroke=0)
            # Label
            c.setFillColor(C_DARK)
            c.setFont('Helvetica', 6.5)
            c.drawCentredString(x + bar_w/2 - 1, 4*mm, sub[:10])
            c.setFont('Helvetica-Bold', 8)
            c.drawCentredString(x + bar_w/2 - 1, by + bh + 2, f"{score}")

    def wrap(self, *args):
        return self.width, self.height


# ── BUILD PDF ──────────────────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_LGRAY)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(20*mm, 10*mm, f"Trustably AI Adoption Assessment  ·  {ORG_NAME}  ·  CONFIDENTIAL")
    canvas.drawRightString(W - 20*mm, 10*mm, f"Page {doc.page}")
    canvas.setStrokeColor(C_MID)
    canvas.setLineWidth(0.3)
    canvas.line(20*mm, 14*mm, W - 20*mm, 14*mm)
    canvas.restoreState()


def build_report(output_file_path: str):
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate

    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    body_frame  = Frame(20*mm, 20*mm, W - 40*mm, H - 40*mm,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='body')

    def body_page(canvas, doc):
        if doc.page > 1:
            add_footer(canvas, doc)

    doc = BaseDocTemplate(
        output_file_path,
        pagesize=A4,
        title=f"Trustably Assessment Report",
    )
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[cover_frame], onPage=lambda c,d: None),
        PageTemplate(id='Body',  frames=[body_frame],  onPage=body_page),
    ])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(NextPageTemplate('Body'))
    story.append(CoverPage(W, H))
    story.append(PageBreak())

    # ── TABLE OF CONTENTS ──────────────────────────────────────────────────────
    story.append(PageHeader("Table of Contents"))
    story.append(Spacer(1, 8*mm))
    toc_items = [
        ("1", "Executive Summary"),
        ("2", "Detailed Current State"),
        ("3", "Gap Analysis"),
        ("4", "Roadmap"),
        ("5", "Implementation Details"),
        ("6", "Scoring & Methodology"),
        ("7", "Appendix — CARE Sub-Capability Scores"),
    ]
    toc_data = []
    for num, title in toc_items:
        toc_data.append([
            Paragraph(num, S['toc_num']),
            Paragraph(title, S['toc']),
        ])
    toc_table = Table(toc_data, colWidths=[15*mm, 140*mm])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.3, C_MID),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # ── 1. EXECUTIVE SUMMARY ──────────────────────────────────────────────────
    story.append(PageHeader("1  —  Executive Summary"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Assessment Overview", S['h1']))
    story.append(Paragraph(
        f"<b>{ORG_NAME}</b> completed a Trustably Applied AI Adoption Framework assessment in {REPORT_DT}. "
        f"The assessment evaluated institutional AI maturity across 4 stages and 5 FOCUS areas, "
        f"scored against the 15 CARE sub-capability quality standard. The assessment was completed "
        f"by respondents across 4 roles: Executive/Head of AI, Risk/Governance Lead, Tech Lead/Architect, "
        f"and Practitioner/Engineer.",
        S['body']))
    story.append(Spacer(1, 4*mm))

    # Overall score + radar side by side
    radar = RadarChart(size=85*mm)
    score_section = [
        [Paragraph("Overall Maturity Score", S['h2']),
         Paragraph("Maturity Radar", S['h2'])],
        [_overall_score_block(), radar],
    ]
    score_table = Table(score_section, colWidths=[100*mm, 80*mm])
    score_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Focus Area Summary", S['h2']))
    for name, score in FOCUS_SCORES.items():
        story.append(ScoreBar(name.replace('\n', ' '), score))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("Key Findings", S['h2']))
    findings = [
        ("Strength", "Functional Governance and Unified Platform are operating at Enable level (6.4 and 6.1), "
         "providing a solid technical and policy foundation."),
        ("Priority Gap", "Culture (3.9) and Observability (4.8) are both at Experiment level — the human "
         "and monitoring dimensions of AI adoption are lagging behind the technical infrastructure."),
        ("Critical Risk", "The gap between Platform maturity (6.1) and Culture maturity (3.9) creates a "
         "governance deficit: capable systems are being operated by teams whose awareness and accountability "
         "practices have not kept pace."),
        ("Next Stage", "To reach Enable level across all five FOCUS areas, the organisation must close "
         "the Culture gap as the primary priority over the next 1–3 months."),
    ]
    for tag, text in findings:
        story.append(_finding_row(tag, text))
    story.append(PageBreak())

    # ── 2. DETAILED CURRENT STATE ──────────────────────────────────────────────
    story.append(PageHeader("2  —  Detailed Current State"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("4E × FOCUS Scoring Matrix", S['h1']))
    story.append(Paragraph(
        "Each cell shows the current score (1–10) and maturity band. Colour indicates band: "
        "green = Enable/Embrace, amber = Experiment, red/orange = Explore.",
        S['body']))
    story.append(Spacer(1, 4*mm))

    cares = sorted(list(set([x[0] for x in CELL_SCORES])), key=lambda x: CARE_ORDER.get(x, 99))
    focuses = sorted(list(set([x[1] for x in CELL_SCORES])), key=lambda x: FOCUS_ORDER.get(x, 99))
    story.append(HeatmapCell(cares, focuses, CELL_SCORES))
    story.append(Spacer(1, 3*mm))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Focus Area Detail", S['h2']))
    fa_details = {
        'Functional Governance': ('6.4 — Enable', C_GREEN,
            "Governance is structured and enforced. AI policy framework is approved and active. "
            "Risk inventory and artefact management are in place. Change management processes are "
            "defined. The organisation has strong foundational governance but has not yet reached "
            "the proactive, self-improving governance characteristic of Embrace stage."),
        'Observability': ('4.8 — Experiment', C_AMBER,
            "Observability is pilot-scoped and not yet enterprise-wide. Metrics are defined for "
            "priority systems but centralised logging and drift detection are not operational. "
            "Monitoring results are not yet routinely communicated to governance stakeholders. "
            "This represents the largest technical gap."),
        'Culture': ('3.9 — Experiment', C_PRIMARY,
            "AI awareness is patchy and role-dependent. Training exists for some teams but is not "
            "enterprise-wide. Roles and responsibilities for AI oversight are partially defined. "
            "The organisation has identified AI champions but has not embedded a harm-prevention "
            "mindset into delivery standards. This is the highest-priority gap."),
        'Unified Platform': ('6.1 — Enable', C_GREEN,
            "The AI platform is standardised and operational. MLOps and DataOps pipelines are "
            "defined and repeatable. Infrastructure-as-code is deployed. The platform supports "
            "current use cases but does not yet provide agentic-ready isolation or self-optimising "
            "cost management."),
        'Security': ('5.2 — Experiment', C_AMBER,
            "Security controls are emerging. Basic access controls and data classification are in "
            "place for priority systems. AI-specific guardrails are partially implemented. "
            "Threat modelling for LLM-specific vulnerabilities (prompt injection, model extraction) "
            "is not yet formalised. Moving to Enable requires a structured AI security programme."),
    }
    for fa, (score_label, col, desc) in fa_details.items():
        story.append(_fa_detail_block(fa, score_label, col, desc))
    story.append(PageBreak())

    # ── 3. GAP ANALYSIS ────────────────────────────────────────────────────────
    story.append(PageHeader("3  —  Gap Analysis"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Identified Gaps", S['h1']))
    story.append(Paragraph(
        "Gaps are identified where a sub-category score falls below the threshold required for the "
        "next maturity band. Priority is assigned based on the size of the gap, the risk exposure "
        "created, and the dependency of other FOCUS areas on the gap being closed.",
        S['body']))
    story.append(Spacer(1, 4*mm))

    gap_data = [
        [Paragraph("Gap", S['label']),
         Paragraph("Current", S['label']),
         Paragraph("Target", S['label']),
         Paragraph("Priority", S['label']),
         Paragraph("Recommended Action", S['label'])],
    ]
    for gap_name, current, target, priority, action in GAPS:
        pri_col = C_PRIMARY if priority == "HIGH" else (C_AMBER if priority == "MEDIUM" else C_GREEN)
        gap_data.append([
            Paragraph(gap_name, S['body']),
            Paragraph(current, S['small']),
            Paragraph(target, S['small']),
            Paragraph(f"<font color='#{pri_col.hexval()[2:]}'><b>{priority}</b></font>", S['body']),
            Paragraph(action, S['small']),
        ])
    gap_table = Table(gap_data, colWidths=[42*mm, 22*mm, 22*mm, 18*mm, 62*mm])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  C_DARK),
        ('TEXTCOLOR',    (0,0), (-1,0),  C_WHITE),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0),  9),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
        ('GRID',         (0,0), (-1,-1), 0.3, C_MID),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 4),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("CARE Sub-Capability Gaps", S['h2']))
    story.append(Paragraph(
        "The following CARE sub-capabilities are scoring below 5.0 (Experiment band) and represent "
        "quality gaps that cut across multiple FOCUS areas.",
        S['body']))
    story.append(Spacer(1, 3*mm))

    care_gaps = [
        ('Resilient',     'Consistent', 4.2, "Stress-testing and degradation planning not yet systematic"),
        ('Observable',    'Reliable',   4.8, "Centralised instrumentation not yet deployed enterprise-wide"),
        ('Interoperable', 'Reliable',   4.4, "Tool fragmentation across teams limits shared observability"),
        ('Context-Aware', 'Effective',  4.7, "Risk-profile calibration of AI systems not yet formalised"),
        ('Unbiased',      'Accurate',   4.9, "Bias detection processes defined for pilots only"),
    ]
    cg_data = [
        [Paragraph("Sub-capability", S['label']),
         Paragraph("CARE Quality", S['label']),
         Paragraph("Score", S['label']),
         Paragraph("Gap Description", S['label'])],
    ]
    for sub, quality, score, desc in care_gaps:
        cg_data.append([
            Paragraph(f"<b>{sub}</b>", S['body']),
            Paragraph(quality, S['small']),
            Paragraph(f"<font color='#C1694F'><b>{score}</b></font>", S['body']),
            Paragraph(desc, S['small']),
        ])
    cg_table = Table(cg_data, colWidths=[32*mm, 28*mm, 16*mm, 90*mm])
    cg_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), C_DARK),
        ('TEXTCOLOR',     (0,0), (-1,0), C_WHITE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
        ('GRID',          (0,0),(-1,-1), 0.3, C_MID),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 4),
    ]))
    story.append(cg_table)
    story.append(PageBreak())

    # ── 4. ROADMAP ────────────────────────────────────────────────────────────
    story.append(PageHeader("4  —  Prioritised Roadmap"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Recommended Actions by Horizon", S['h1']))
    story.append(Paragraph(
        "The roadmap is structured across three time horizons. Each section shows the FOCUS area, "
        "CARE sub-capability alignment, and detailed suggested actions drawn from the Trustably "
        "action library grounded in NIST AI RMF, DASF, and AWS WAR AI Lens.",
        S['body']))
    story.append(Spacer(1, 5*mm))

    # Load actions from spreadsheet
    try:
        actions_df = load_actions('/mnt/user-data/uploads/final_-_AEF_Risks_and_Actions.xlsx')
        has_actions = True
    except Exception:
        has_actions = False

    # Define roadmap items with FOCUS area + CARE sub-capability mappings
    ROADMAP_DETAILED = [
        {
            "horizon": "1–4 weeks",
            "label": "Immediate Actions",
            "col": C_PRIMARY,
            "priority": "CRITICAL",
            "items": [
                {
                    "number": "1.1",
                    "title": "Culture — Active Awareness",
                    "focus": "Culture",
                    "subcategory": "Active Awareness",
                    "care_trait": "Reliable",
                    "care_sub": "Accountable",
                    "overview": "Establish AI risk ownership and awareness across all relevant functions before any further AI deployment.",
                    "benefit": "Reduces ungoverned AI use risk. Creates the accountability foundation that all other governance improvements depend on.",
                    "priority_tag": "HIGH",
                },
                {
                    "number": "1.2",
                    "title": "Culture — Operating Model",
                    "focus": "Culture",
                    "subcategory": "Operating Model",
                    "care_trait": "Reliable",
                    "care_sub": "Accountable",
                    "overview": "Define roles, responsibilities, and escalation paths for AI risk management across the organisation.",
                    "benefit": "Closes the accountability gap identified as the primary Culture sub-capability weakness.",
                    "priority_tag": "HIGH",
                },
                {
                    "number": "1.3",
                    "title": "Security — Access Control",
                    "focus": "Security",
                    "subcategory": "Access Control",
                    "care_trait": "Effective",
                    "care_sub": "Secure",
                    "overview": "Implement AI-specific identity and access controls including MFA, SSO, and least-privilege enforcement for all AI workloads.",
                    "benefit": "Directly addresses the Security gap. Prevents unauthorised access to AI systems and sensitive training data.",
                    "priority_tag": "HIGH",
                },
            ],
        },
        {
            "horizon": "1–3 months",
            "label": "Short-Term Plan",
            "col": C_GREEN,
            "priority": "HIGH",
            "items": [
                {
                    "number": "2.1",
                    "title": "Culture — Intention of Use",
                    "focus": "Culture",
                    "subcategory": "Intention of Use",
                    "care_trait": "Effective",
                    "care_sub": "Desirable",
                    "overview": "Define the purpose, intended use, and expected benefits of all priority AI systems. Identify human-AI interaction risks.",
                    "benefit": "Ensures AI investment is connected to real business outcomes rather than technology-led deployment.",
                    "priority_tag": "HIGH",
                },
                {
                    "number": "2.2",
                    "title": "Observability — Define and Instrument",
                    "focus": "Observability",
                    "subcategory": "Define and Instrument",
                    "care_trait": "Reliable",
                    "care_sub": "Observable",
                    "overview": "Define assessment scales and measurement frameworks for AI system performance. Implement centralised logging and metrics infrastructure.",
                    "benefit": "Closes the Observability gap. Enables data-driven governance and drift detection across all production AI systems.",
                    "priority_tag": "HIGH",
                },
                {
                    "number": "2.3",
                    "title": "Security — Safe Guards & Guardrails",
                    "focus": "Security",
                    "subcategory": "Safe Guards & Guardrails",
                    "care_trait": "Effective",
                    "care_sub": "Safe",
                    "overview": "Deploy guardrails enforcing safety, moderation, and compliance on AI outputs. Implement output filtering and data access controls.",
                    "benefit": "Reduces AI safety and compliance exposure. Prevents harmful or non-compliant outputs from reaching end users.",
                    "priority_tag": "MEDIUM",
                },
            ],
        },
        {
            "horizon": "3–12 months",
            "label": "Strategic Initiatives",
            "col": C_AMBER,
            "priority": "MEDIUM",
            "items": [
                {
                    "number": "3.1",
                    "title": "Governance — AI Risk Management",
                    "focus": "Governance",
                    "subcategory": "AI Risk Management",
                    "care_trait": "Consistent",
                    "care_sub": "Strategic",
                    "overview": "Formalise AI risk assessment processes aligned to NIST AI RMF. Establish risk tolerance thresholds and escalation procedures.",
                    "benefit": "Moves governance from Experiment to Enable. Provides the risk management backbone for all future AI scaling.",
                    "priority_tag": "MEDIUM",
                },
                {
                    "number": "3.2",
                    "title": "Observability — Monitor and Action",
                    "focus": "Observability",
                    "subcategory": "Monitor and Action",
                    "care_trait": "Reliable",
                    "care_sub": "Observable",
                    "overview": "Deploy automated drift detection, bias monitoring, and performance degradation alerting across all production AI systems.",
                    "benefit": "Achieves Enable-level Observability. Enables proactive rather than reactive AI operations management.",
                    "priority_tag": "MEDIUM",
                },
                {
                    "number": "3.3",
                    "title": "Platform — Resilience",
                    "focus": "Platform",
                    "subcategory": "Resilience",
                    "care_trait": "Consistent",
                    "care_sub": "Resilient",
                    "overview": "Define storage, retention, and recovery procedures. Implement backup and recovery controls for AI model artefacts and data pipelines.",
                    "benefit": "Closes the Resilient CARE gap (currently 4.2). Ensures AI platform continuity under failure conditions.",
                    "priority_tag": "LOW",
                },
            ],
        },
    ]

    for section in ROADMAP_DETAILED:
        story.append(_roadmap_section_header(section['horizon'], section['label'], section['col']))
        story.append(Spacer(1, 3*mm))
        for item in section['items']:
            actions_list = []
            if has_actions:
                mask = (
                    (actions_df['Focus Area'] == item['focus']) &
                    (actions_df['Sub Category'].str.strip() == item['subcategory'].strip()) &
                    (actions_df['subtrait_name'] == item['care_sub'])
                )
                actions_list = actions_df[mask]['Suggested Action'].tolist()[:5]
            story.append(_roadmap_detail_card(item, actions_list))
            story.append(Spacer(1, 3*mm))
        story.append(Spacer(1, 3*mm))
    story.append(PageBreak())

    # ── 5. IMPLEMENTATION DETAILS ────────────────────────────────────────────
    story.append(PageHeader("5  —  Implementation Details"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Maturity Targets", S['h1']))
    story.append(Paragraph(
        "The table below shows current scores, target scores for the next assessment cycle (6 months), "
        "and the strategic target (18 months). Targets are set using the threshold progression model — "
        "a FOCUS area advances to the next band only when all sub-categories meet the minimum threshold.",
        S['body']))
    story.append(Spacer(1, 4*mm))

    targets_data = [
        [Paragraph(x, S['label']) for x in ["FOCUS Area", "Current", "6-Month Target", "18-Month Target", "Key Enablers"]],
        ["Functional Governance", "6.4 (Enable)", "7.5 (Enable+)", "9.0 (Embrace)", "Policy automation, proactive risk monitoring"],
        ["Observability",         "4.8 (Experiment)", "6.5 (Enable)", "8.5 (Embrace)", "Centralised platform, drift detection, agentic tracing"],
        ["Culture",               "3.9 (Experiment)", "6.2 (Enable)", "7.5 (Enable+)", "Enterprise training, AI literacy programme, champions"],
        ["Unified Platform",      "6.1 (Enable)", "7.0 (Enable+)", "9.0 (Embrace)", "Agentic isolation, self-optimising infra"],
        ["Security",              "5.2 (Experiment)", "6.5 (Enable)", "8.0 (Embrace)", "AI threat modelling, guardrails, automated testing"],
    ]
    for i in range(1, len(targets_data)):
        targets_data[i] = [Paragraph(str(x), S['small']) for x in targets_data[i]]
    targets_table = Table(targets_data, colWidths=[35*mm, 25*mm, 27*mm, 27*mm, 55*mm])
    targets_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), C_DARK),
        ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
        ('GRID',         (0,0),(-1,-1), 0.3, C_MID),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ]))
    story.append(targets_table)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph("Respondent Coverage", S['h2']))
    story.append(Paragraph(
        "The assessment was completed by respondents across the following roles. Confidence ratings "
        "reflect the number of respondents and their domain coverage for each FOCUS area.",
        S['body']))
    story.append(Spacer(1, 3*mm))

    resp_data = [
        [Paragraph(x, S['label']) for x in ["Role", "Respondents", "FOCUS Areas Covered", "Confidence"]],
        ["Executive / Head of AI",    "2", "All 5", "High"],
        ["Risk / Governance Lead",     "1", "Gov, Culture", "Medium"],
        ["Tech Lead / Architect",      "2", "Obs, Platform, Security", "High"],
        ["Practitioner / Engineer",    "3", "Platform, Security, Obs", "High"],
    ]
    for i in range(1, len(resp_data)):
        resp_data[i] = [Paragraph(str(x), S['small']) for x in resp_data[i]]
    resp_table = Table(resp_data, colWidths=[50*mm, 28*mm, 55*mm, 35*mm])
    resp_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), C_DARK),
        ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
        ('GRID',         (0,0),(-1,-1), 0.3, C_MID),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ]))
    story.append(resp_table)
    story.append(PageBreak())

    # ── 6. SCORING & METHODOLOGY ─────────────────────────────────────────────
    story.append(PageHeader("6  —  Scoring & Methodology"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("How Trustably Scores AI Maturity", S['h1']))

    meth_sections = [
        ("The 4E Maturity Spine",
         "Trustably assesses organisational AI maturity across four progressive stages: Explore "
         "(decentralised discovery), Experiment (risk-mapped pilots), Enable (standardised platform "
         "and governance), and Embrace (AI as self-governing business utility). These stages describe "
         "qualitatively different operating modes — not just more of the same capability."),
        ("The FOCUS Pillars",
         "Five vertical pillars (Functional Governance, Observability, Culture, Unified Platform, "
         "Security) provide the scoring dimensions. Each pillar contains three sub-categories that "
         "persist across all four 4E stages — what changes is the depth and quality of practice."),
        ("The 1–10 Scale",
         "Each scoring cell is assessed on a 1–10 scale mapped to the four bands: 1–2 Explore, "
         "3–5 Experiment, 6–8 Enable, 9–10 Embrace. This means a single cell score simultaneously "
         "locates practice on the 4E spine and describes its quality through CARE."),
        ("How Maturity Levels Are Earned",
         "A FOCUS area advances to the next band only when all sub-categories within it meet the "
         "minimum threshold for that band. A single sub-category below threshold anchors the entire "
         "pillar at the lower level. This mirrors CMMI threshold logic — preventing organisations "
         "from over-investing in strengths while leaving foundational gaps unaddressed."),
        ("CARE Quality Standard",
         "The 15 CARE sub-capabilities (Consistent, Accurate, Reliable, Effective) provide the "
         "quality rubric within every scoring cell. Questions are grounded in NIST AI RMF, "
         "Databricks DASF, and AWS Well-Architected AI Lens, giving each score external credibility."),
        ("Respondent Variance",
         "Where respondents for the same cell differ by more than 2 points, the output flags a "
         "confidence gap — indicating a perception problem that itself requires action. The recommended "
         "minimum is three respondents covering at least three of the four designated roles."),
    ]
    for title, body in meth_sections:
        story.append(Paragraph(title, S['h2']))
        story.append(Paragraph(body, S['body']))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Score Band Reference", S['h2']))
    band_data = [
        [Paragraph(x, S['label']) for x in ["Score", "Band", "Descriptor", "Typical State"]],
        ["9–10", "EMBRACE", "Optimised, self-improving", "AI is core self-governing utility; governance is proactive"],
        ["6–8",  "ENABLE",  "Defined, standardised",     "Platform-stage; consistent enforcement across organisation"],
        ["3–5",  "EXPERIMENT","Emerging, pilot-scoped",  "Structured pilots; inconsistent enterprise application"],
        ["1–2",  "EXPLORE",  "Ad hoc, individual-led",   "Decentralised discovery; no shared infrastructure or policy"],
    ]
    band_colors = [C_DARK, colors.HexColor('#2E6B3E'), C_GREEN, C_AMBER, C_PRIMARY]
    for i in range(1, len(band_data)):
        band_data[i] = [Paragraph(str(x), S['small']) for x in band_data[i]]
    band_table = Table(band_data, colWidths=[18*mm, 28*mm, 42*mm, 80*mm])
    ts = TableStyle([
        ('BACKGROUND',   (0,0), (-1,0), C_DARK),
        ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
        ('GRID',         (0,0),(-1,-1), 0.3, C_MID),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ])
    for i, col in enumerate(band_colors[1:], 1):
        ts.add('BACKGROUND', (0,i), (0,i), col)
        ts.add('TEXTCOLOR',  (0,i), (0,i), C_WHITE)
        ts.add('FONTNAME',   (0,i), (0,i), 'Helvetica-Bold')
        ts.add('BACKGROUND', (1,i), (1,i), col)
        ts.add('TEXTCOLOR',  (1,i), (1,i), C_WHITE)
        ts.add('FONTNAME',   (1,i), (1,i), 'Helvetica-Bold')
    band_table.setStyle(ts)
    story.append(band_table)
    story.append(PageBreak())

    # ── 7. APPENDIX ──────────────────────────────────────────────────────────
    story.append(PageHeader("7  —  Appendix: CARE Sub-Capability Scores"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Full CARE Sub-Capability Breakdown", S['h1']))
    story.append(Paragraph(
        "The following charts show scores for all 15 CARE sub-capabilities, grouped by quality. "
        "Scores represent the average across all relevant FOCUS area assessments.",
        S['body']))
    story.append(Spacer(1, 5*mm))

    for trait, sub_scores in CARE_SCORES.items():
        story.append(Paragraph(trait, S['h2']))
        story.append(CareBar(trait, sub_scores))
        story.append(Spacer(1, 4*mm))
        # Detail table
        sub_data = [[Paragraph(x, S['label']) for x in ["Sub-capability", "Score", "Band", "Description"]]]
        descriptions = {
            'Strategic':    "AI use and systems are aligned to organisational goals and purposeful outcomes",
            'Viable':       "Practices and systems are economically and operationally sustainable",
            'Resilient':    "Systems degrade gracefully under failure; practitioners maintain engagement under pressure",
            'Valid':        "Systems behave as intended; AI is applied where genuinely fit for purpose",
            'Unbiased':     "Outputs are free from discriminatory patterns; practitioners check before acting",
            'Explainable':  "Outcomes are traceable and interpretable; practitioners can articulate AI rationale",
            'Integrated':   "Accuracy is coherent end-to-end; outputs are connected meaningfully to context",
            'Observable':   "Continuous monitoring and instrumentation; practitioners know how to check system health",
            'Transparent':  "AI use and limitations are disclosed; practitioners are open about AI's role",
            'Accountable':  "Clear roles, governance, and escalation; practitioners own AI-assisted outcomes",
            'Interoperable':"Systems are modular and composable; practitioners collaborate across tools and teams",
            'Desirable':    "Systems address real demand; practitioners prioritise value over performance",
            'Secure':       "Systems are protected from unauthorised access; practitioners handle tools with discretion",
            'Context-Aware':"Systems incorporate intent into authorisation; practitioners read the situation first",
            'Safe':         "Systems do not negatively impact society; practitioners know when to apply human override",
        }
        for sub, score in sub_scores.items():
            sub_data.append([
                Paragraph(f"<b>{sub}</b>", S['small']),
                Paragraph(f"<font color='#{'4A7C59' if score>=6 else 'D4A843' if score>=4 else 'C1694F'}'><b>{score}</b></font>", S['body']),
                Paragraph(band_label(score), S['small']),
                Paragraph(descriptions.get(sub, ""), S['small']),
            ])
        sub_table = Table(sub_data, colWidths=[30*mm, 16*mm, 26*mm, 95*mm])
        sub_table.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,0), C_DARK),
            ('TEXTCOLOR',    (0,0),(-1,0), C_WHITE),
            ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
            ('GRID',         (0,0),(-1,-1), 0.3, C_MID),
            ('VALIGN',       (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING',   (0,0),(-1,-1), 4),
            ('BOTTOMPADDING',(0,0),(-1,-1), 4),
            ('LEFTPADDING',  (0,0),(-1,-1), 4),
        ]))
        story.append(sub_table)
        story.append(Spacer(1, 4*mm))

    # Framework reference
    story.append(Paragraph("Framework Reference", S['h2']))
    ref_data = [
        [Paragraph(x, S['label']) for x in ["Framework", "Version", "Trustably Mapping"]],
        ["NIST AI Risk Management Framework", "AI RMF 1.0 + GenAI Profile", "Functional Governance, Culture sub-categories"],
        ["Databricks AI Security Framework", "DASF 2.0", "Security, Observability sub-categories"],
        ["AWS Well-Architected AI Lens",      "Dec 2025",  "Unified Platform, Observability sub-categories"],
    ]
    for i in range(1, len(ref_data)):
        ref_data[i] = [Paragraph(str(x), S['small']) for x in ref_data[i]]
    ref_table = Table(ref_data, colWidths=[55*mm, 35*mm, 78*mm])
    ref_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,0), C_DARK),
        ('TEXTCOLOR',    (0,0),(-1,0), C_WHITE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_LIGHT, C_WHITE]),
        ('GRID',         (0,0),(-1,-1), 0.3, C_MID),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "This report was generated using the Trustably Applied AI Adoption Framework v1.0. "
        "For more information visit trustably.super.site. All scores and findings in this report "
        "are based on self-assessment responses and should be validated through evidence review "
        "during a Trustably Rapid Assessment engagement.",
        S['small']))

    doc.build(story)
    print("Done")


# ── HELPER BUILDERS ────────────────────────────────────────────────────────────
def _overall_score_block():
    col_hex = score_color(OVERALL).hexval()[2:]
    items = [
        Spacer(1, 2*mm),
        Paragraph(
            f"<font size='32' color='#{col_hex}'><b>{OVERALL}</b></font>"
            f"<font size='13' color='#666666'> / 10.0</font>",
            ParagraphStyle('sc', leading=40, spaceAfter=4)),
        Paragraph(
            f"<font size='13' color='#{col_hex}'><b>{band_label(OVERALL)}</b></font>",
            ParagraphStyle('sb', leading=18, spaceAfter=6)),
        Paragraph(
            "The organisation is broadly operating at <b>Experiment to Enable</b> level. "
            "Technical capabilities (Platform, Governance) are ahead of the human dimensions "
            "(Culture, Observability).",
            S['body']),
    ]
    t = Table([[item] for item in items], colWidths=[90*mm])
    t.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
    ]))
    return t


def _finding_row(tag, text):
    tag_colors = {'Strength': C_GREEN, 'Priority Gap': C_AMBER, 'Critical Risk': C_PRIMARY, 'Next Stage': C_DARK}
    col = tag_colors.get(tag, C_DARK)
    data = [[
        Paragraph(f"<b>{tag}</b>", ParagraphStyle('ft', fontName='Helvetica-Bold', fontSize=9,
                  textColor=C_WHITE, leading=13)),
        Paragraph(text, S['body']),
    ]]
    t = Table(data, colWidths=[28*mm, 130*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(0,0), col),
        ('BACKGROUND',   (1,0),(1,0), C_LIGHT),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('LINEBELOW',    (0,0),(-1,-1), 0.3, C_MID),
    ]))
    return t


def _fa_detail_block(title, score_label, col, desc):
    data = [[
        Paragraph(f"<b>{title}</b>", ParagraphStyle('fat', fontName='Helvetica-Bold', fontSize=10,
                  textColor=C_WHITE, leading=14)),
        Paragraph(f"<b>{score_label}</b>", ParagraphStyle('fas', fontName='Helvetica-Bold', fontSize=10,
                  textColor=C_WHITE, leading=14)),
        Paragraph(desc, S['small']),
    ]]
    t = Table(data, colWidths=[42*mm, 28*mm, 97*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(0,0), C_DARK),
        ('BACKGROUND',   (1,0),(1,0), col),
        ('BACKGROUND',   (2,0),(2,0), C_LIGHT),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('LINEBELOW',    (0,0),(-1,-1), 0.5, C_MID),
    ]))
    return t


def _roadmap_band(horizon, label, col, actions):
    items_para = [Paragraph(f"• {a}", S['body']) for a in actions]
    data = [[
        Paragraph(f"<b>{horizon}</b>\n{label}", ParagraphStyle('rh', fontName='Helvetica-Bold',
                  fontSize=10, textColor=C_WHITE, leading=15)),
        items_para,
    ]]
    inner = Table([[p] for p in items_para], colWidths=[138*mm])
    inner.setStyle(TableStyle([
        ('TOPPADDING',   (0,0),(-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
    ]))
    data = [[
        Paragraph(f"<b>{horizon}</b><br/><font size='8'>{label}</font>",
                  ParagraphStyle('rh', fontName='Helvetica-Bold', fontSize=11,
                                 textColor=C_WHITE, leading=16)),
        inner,
    ]]
    t = Table(data, colWidths=[28*mm, 140*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(0,0), col),
        ('BACKGROUND',   (1,0),(1,0), C_LIGHT),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('BOX',          (0,0),(-1,-1), 0.5, C_MID),
    ]))
    return t


def _roadmap_section_header(horizon, label, col):
    data = [[
        Paragraph(f"<b>{horizon}</b>", ParagraphStyle('rsh', fontName='Helvetica-Bold',
                  fontSize=12, textColor=C_WHITE, leading=16)),
        Paragraph(label.upper(), ParagraphStyle('rsl', fontName='Helvetica-Bold',
                  fontSize=9, textColor=C_WHITE, leading=14, spaceAfter=0)),
    ]]
    t = Table(data, colWidths=[40*mm, 130*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), col),
        ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('LINEBELOW',    (0,0),(-1,-1), 1.5, colors.HexColor('#00000030')),
    ]))
    return t


def _roadmap_detail_card(item, actions_list):
    pri_col = C_PRIMARY if item['priority_tag'] == 'HIGH' else (C_AMBER if item['priority_tag'] == 'MEDIUM' else C_GREEN)
    pri_bg  = colors.HexColor('#C1694F15') if item['priority_tag'] == 'HIGH' else (
              colors.HexColor('#D4A84315') if item['priority_tag'] == 'MEDIUM' else
              colors.HexColor('#4A7C5915'))

    # LEFT SIDEBAR
    sidebar_items = [
        Paragraph(item['number'], ParagraphStyle('rn', fontName='Helvetica-Bold',
                  fontSize=20, textColor=C_DARK, leading=24, spaceAfter=4)),
        Paragraph(item['focus'], ParagraphStyle('rf', fontName='Helvetica-Bold',
                  fontSize=8, textColor=C_PRIMARY, leading=11, spaceAfter=2)),
        Paragraph(item['subcategory'], ParagraphStyle('rs', fontName='Helvetica',
                  fontSize=8, textColor=C_GRAY, leading=11, spaceAfter=6)),
        Spacer(1, 3*mm),
        Paragraph("CARE ALIGNMENT", ParagraphStyle('rca', fontName='Helvetica-Bold',
                  fontSize=7, textColor=C_LGRAY, leading=10, spaceAfter=2)),
        Paragraph(item['care_trait'], ParagraphStyle('rct', fontName='Helvetica-Bold',
                  fontSize=8, textColor=C_DARK, leading=11, spaceAfter=1)),
        Paragraph(item['care_sub'], ParagraphStyle('rcs', fontName='Helvetica',
                  fontSize=8, textColor=C_GRAY, leading=11, spaceAfter=6)),
        Spacer(1, 3*mm),
        _priority_badge(item['priority_tag'], pri_col),
    ]
    sidebar_table = Table([[p] for p in sidebar_items], colWidths=[38*mm])
    sidebar_table.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('RIGHTPADDING', (0,0),(-1,-1), 3),
        ('TOPPADDING',   (0,0),(-1,-1), 1),
        ('BOTTOMPADDING',(0,0),(-1,-1), 1),
        ('BACKGROUND',   (0,0),(-1,-1), C_LIGHT),
    ]))

    # RIGHT PANEL
    right_items = [
        Paragraph(f"<b>{item['title']}</b>",
                  ParagraphStyle('rt', fontName='Helvetica-Bold', fontSize=11,
                                 textColor=C_DARK, leading=15, spaceAfter=4)),
        Paragraph("OVERVIEW", ParagraphStyle('rov_lbl', fontName='Helvetica-Bold',
                  fontSize=7, textColor=C_LGRAY, leading=10, spaceAfter=2)),
        Paragraph(item['overview'],
                  ParagraphStyle('rov', fontName='Helvetica', fontSize=9,
                                 textColor=C_GRAY, leading=13, spaceAfter=5)),
    ]

    if actions_list:
        right_items.append(Paragraph("SUGGESTED ACTIONS",
                  ParagraphStyle('sa_lbl', fontName='Helvetica-Bold', fontSize=7,
                                 textColor=C_LGRAY, leading=10, spaceAfter=3)))
        for i, action in enumerate(actions_list):
            right_items.append(
                Paragraph(f"<font color='#{C_PRIMARY.hexval()[2:]}'><b>{i+1}</b></font>  {action}",
                          ParagraphStyle('sa', fontName='Helvetica', fontSize=8,
                                         textColor=C_DARK, leading=12, spaceAfter=2,
                                         leftIndent=0)))

    right_items.append(Spacer(1, 2*mm))
    right_items.append(Paragraph("MAIN BENEFIT",
              ParagraphStyle('mb_lbl', fontName='Helvetica-Bold', fontSize=7,
                             textColor=C_LGRAY, leading=10, spaceAfter=2)))
    right_items.append(Paragraph(f"• {item['benefit']}",
              ParagraphStyle('mb', fontName='Helvetica-Oblique', fontSize=8,
                             textColor=C_GREEN, leading=12)))

    right_table = Table([[p] for p in right_items], colWidths=[128*mm])
    right_table.setStyle(TableStyle([
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 1),
        ('BOTTOMPADDING',(0,0),(-1,-1), 1),
        ('BACKGROUND',   (0,0),(-1,-1), C_WHITE),
    ]))

    # Combine sidebar + right panel
    card = Table([[sidebar_table, right_table]], colWidths=[40*mm, 130*mm])
    card.setStyle(TableStyle([
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1), 0),
        ('TOPPADDING',   (0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
        ('BOX',          (0,0),(-1,-1), 0.5, C_MID),
        ('LINEAFTER',    (0,0),(0,-1),  0.5, C_MID),
    ]))
    return card


def _priority_badge(label, col):
    data = [[Paragraph(f"<b>{label}</b>",
             ParagraphStyle('pb', fontName='Helvetica-Bold', fontSize=8,
                            textColor=C_WHITE, leading=11))]]
    t = Table(data, colWidths=[28*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), col),
        ('TOPPADDING',   (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('LEFTPADDING',  (0,0),(-1,-1), 5),
        ('ROUNDEDCORNERS', [2]),
    ]))
    return t


if __name__ == '__main__':
    output_file_path = "./sample.pdf"
    build_report(output_file_path)
