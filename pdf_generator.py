"""
MAARA PDF generator
-------------------
Converts the Markdown report produced by the Report Writer Agent into a PDF
that follows the same template as the MAARA Draft / Progress Report:

  * Cover page  : title, MAARA, report type, subtitle, Field/Details table
  * Header      : "MAARA — Final Research Report" | "Dept. of AI & Data Science | 2026"
  * Footer      : "Multi-Agent AI Research Assistant (MAARA) | Pratibha Gupta" | Page N
  * Headings    : navy numbered-style headings (H1 / H2 / H3)
  * Tables      : navy header row, alternating rows, "Table N: ..." caption
  * Bullets, nested bullets, numbered lists, **bold**, *italic*

Usage (unchanged):
    from pdf_generator import create_pdf
    create_pdf(report_text, "MAARA_Final_Report.pdf")
"""

import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ============================================================
# TEMPLATE SETTINGS  (edit these if details change)
# ============================================================

PROJECT_TITLE = (
    "Multi-Agent AI Research Assistant (MAARA): Intelligent Research "
    "Paper Analysis using Large Language Models"
)
SUBMITTED_BY = "Pratibha Gupta"
DEPARTMENT = "Artificial Intelligence and Data Science"
FACULTY_MENTOR = "Savita Prashant Vibhute"
ACADEMIC_YEAR = "2026"
REPORT_LABEL = "Final Research Report"
COVER_SUBTITLE = "Literature Review, Paper Analysis & Research Gap Identification"
HEADER_LEFT = "MAARA \u2014 Final Research Report"
HEADER_RIGHT = "Dept. of AI & Data Science | 2026"
FOOTER_LEFT = "Multi-Agent AI Research Assistant (MAARA) | Pratibha Gupta"

# ============================================================
# COLORS
# ============================================================

NAVY = colors.HexColor("#1F3864")
BLUE = colors.HexColor("#2E75B6")
LIGHT_GREY = colors.HexColor("#F2F4F7")
MID_GREY = colors.HexColor("#BFC5CE")
DARK_GREY = colors.HexColor("#444444")
WHITE = colors.white
BLACK = colors.black

# ============================================================
# FONTS  (works on Windows, Linux, macOS and a local ./fonts folder)
# ============================================================

_FONT_CANDIDATES = [
    # (regular, bold, italic, bolditalic)
    (   # Windows Arial
        r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\ariali.ttf", r"C:\Windows\Fonts\arialbi.ttf",
    ),
    (   # Linux - Liberation Sans (Arial look-alike)
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
    ),
    (   # Linux - DejaVu Sans
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
    ),
    (   # macOS Arial
        "/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial Italic.ttf", "/Library/Fonts/Arial Bold Italic.ttf",
    ),
    (   # Optional: put these 4 files in a "fonts" folder next to this script
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "arial.ttf"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "arialbd.ttf"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "ariali.ttf"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "arialbi.ttf"),
    ),
]


def register_fonts():
    """Register the first available Unicode font family. Falls back to Helvetica."""
    for regular, bold, italic, bold_italic in _FONT_CANDIDATES:
        if all(os.path.exists(p) for p in (regular, bold, italic, bold_italic)):
            try:
                pdfmetrics.registerFont(TTFont("MAARA-Regular", regular))
                pdfmetrics.registerFont(TTFont("MAARA-Bold", bold))
                pdfmetrics.registerFont(TTFont("MAARA-Italic", italic))
                pdfmetrics.registerFont(TTFont("MAARA-BoldItalic", bold_italic))
                pdfmetrics.registerFontFamily(
                    "MAARA",
                    normal="MAARA-Regular",
                    bold="MAARA-Bold",
                    italic="MAARA-Italic",
                    boldItalic="MAARA-BoldItalic",
                )
                return ("MAARA-Regular", "MAARA-Bold", "MAARA-Italic", "MAARA-BoldItalic")
            except Exception:
                continue
    return ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique")


FONT_REGULAR, FONT_BOLD, FONT_ITALIC, FONT_BOLD_ITALIC = register_fonts()

# ============================================================
# TEXT CLEANING
# ============================================================

# Characters LLMs love to use that many fonts have no glyph for (shown as black squares).
_CHAR_MAP = {
    "\u2011": "-",   # non-breaking hyphen   (this was the ■ in your PDF)
    "\u2010": "-",   # hyphen
    "\u2012": "-",   # figure dash
    "\u2212": "-",   # minus sign
    "\u00a0": " ",   # non-breaking space
    "\u202f": " ",   # narrow no-break space
    "\u2009": " ",   # thin space
    "\u200a": " ",
    "\u2002": " ",
    "\u2003": " ",
    "\u200b": "",    # zero-width space
    "\u200c": "",
    "\u200d": "",
    "\ufeff": "",
    "\u2192": "->",  # arrows
    "\u2190": "<-",
    "\u21d2": "=>",
    "\u2264": "<=",
    "\u2265": ">=",
    "\u25a0": "-",   # black square
    "\ufffd": "",    # replacement char
}

_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\U0000FE0F"
    "]+",
    flags=re.UNICODE,
)


def clean_text(text):
    if not text:
        return ""
    for bad, good in _CHAR_MAP.items():
        text = text.replace(bad, good)
    text = _EMOJI_RE.sub("", text)
    return text


def format_inline(text):
    """Markdown inline -> ReportLab mini-HTML (bold, italic, code, links)."""
    if not text:
        return ""
    text = clean_text(text)
    text = re.sub(r"<br\s*/?>", "\u0001", text, flags=re.IGNORECASE)   # keep <br> from tables
    text = escape(text)
    text = text.replace("\u0001", "<br/>")

    # [label](url) -> label
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]+)\)", r"\1", text)

    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", text)
    return text


def strip_markdown(text):
    """Plain text version (for the cover table etc.)."""
    text = clean_text(text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = text.replace("`", "")
    return text.strip()


# ============================================================
# TOPIC EXTRACTION
# ============================================================

_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")


def extract_topic(report_text):
    """
    Handles all of these layouts:
        Research Topic: XYZ
        **Research Topic:** XYZ
        ## Research Topic
        XYZ
        Research Topic
        **XYZ**
    """
    lines = report_text.splitlines()

    for idx, raw in enumerate(lines):
        line = strip_markdown(raw)
        line = re.sub(r"^#+\s*", "", line).strip()

        m = re.match(r"^(research\s+topic|topic)\s*[:\-\u2013\u2014]\s*(.+)$", line, re.I)
        if m and m.group(2).strip():
            return m.group(2).strip()

        if re.match(r"^(research\s+topic|topic)\s*:?\s*$", line, re.I):
            for nxt in lines[idx + 1: idx + 6]:
                candidate = strip_markdown(nxt)
                candidate = re.sub(r"^#+\s*", "", candidate).strip()
                if candidate and not re.match(r"^[-*_]{3,}$", candidate):
                    return candidate

    return "Research Paper Analysis"


# ============================================================
# STYLES
# ============================================================

def create_styles():
    base = getSampleStyleSheet()

    s = {}
    s["cover_title"] = ParagraphStyle(
        "CoverTitle", parent=base["Title"], fontName=FONT_BOLD, fontSize=22,
        leading=27, alignment=TA_CENTER, textColor=NAVY, spaceAfter=6,
    )
    s["cover_maara"] = ParagraphStyle(
        "CoverMaara", parent=base["Normal"], fontName=FONT_BOLD, fontSize=15,
        leading=19, alignment=TA_CENTER, textColor=BLUE, spaceAfter=18,
    )
    s["cover_report"] = ParagraphStyle(
        "CoverReport", parent=base["Normal"], fontName=FONT_BOLD, fontSize=15,
        leading=19, alignment=TA_CENTER, textColor=BLACK, spaceAfter=4,
    )
    s["cover_subtitle"] = ParagraphStyle(
        "CoverSubtitle", parent=base["Normal"], fontName=FONT_ITALIC, fontSize=9.5,
        leading=14, alignment=TA_CENTER, textColor=DARK_GREY, spaceAfter=22,
    )
    s["cover_note"] = ParagraphStyle(
        "CoverNote", parent=base["Normal"], fontName=FONT_ITALIC, fontSize=8.5,
        leading=12, alignment=TA_CENTER, textColor=DARK_GREY,
    )

    s["h1"] = ParagraphStyle(
        "H1", parent=base["Heading1"], fontName=FONT_BOLD, fontSize=15,
        leading=19, textColor=NAVY, spaceBefore=16, spaceAfter=8, keepWithNext=True,
    )
    s["h2"] = ParagraphStyle(
        "H2", parent=base["Heading2"], fontName=FONT_BOLD, fontSize=12.5,
        leading=16, textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True,
    )
    s["h3"] = ParagraphStyle(
        "H3", parent=base["Heading3"], fontName=FONT_BOLD, fontSize=11,
        leading=14, textColor=BLUE, spaceBefore=9, spaceAfter=5, keepWithNext=True,
    )

    s["body"] = ParagraphStyle(
        "Body", parent=base["BodyText"], fontName=FONT_REGULAR, fontSize=10,
        leading=15, alignment=TA_JUSTIFY, textColor=BLACK, spaceAfter=7,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", parent=s["body"], leftIndent=22, bulletIndent=10, spaceAfter=3,
        alignment=TA_LEFT,
    )
    s["bullet2"] = ParagraphStyle(
        "Bullet2", parent=s["bullet"], leftIndent=42, bulletIndent=30, fontSize=9.6,
    )
    s["number"] = ParagraphStyle(
        "Number", parent=s["body"], leftIndent=22, bulletIndent=8, spaceAfter=4,
        alignment=TA_LEFT,
    )
    s["number2"] = ParagraphStyle(
        "Number2", parent=s["number"], leftIndent=42, bulletIndent=28,
    )

    s["th"] = ParagraphStyle(
        "TH", parent=s["body"], fontName=FONT_BOLD, fontSize=8.8, leading=11.5,
        textColor=WHITE, alignment=TA_LEFT, spaceAfter=0,
    )
    s["td"] = ParagraphStyle(
        "TD", parent=s["body"], fontName=FONT_REGULAR, fontSize=8.6, leading=11.5,
        textColor=BLACK, alignment=TA_LEFT, spaceAfter=0,
    )
    s["caption"] = ParagraphStyle(
        "Caption", parent=s["body"], fontName=FONT_ITALIC, fontSize=8.5, leading=11,
        textColor=DARK_GREY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10,
    )
    return s


# ============================================================
# HEADER / FOOTER  (same on every page, like the Draft Report)
# ============================================================

def add_header_footer(canvas, doc):
    canvas.saveState()
    page_w, page_h = A4
    left, right = 0.70 * inch, page_w - 0.70 * inch

    # Header
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(DARK_GREY)
    canvas.drawString(left, page_h - 0.55 * inch, HEADER_LEFT)
    canvas.drawRightString(right, page_h - 0.55 * inch, HEADER_RIGHT)
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.6)
    canvas.line(left, page_h - 0.62 * inch, right, page_h - 0.62 * inch)

    # Footer
    canvas.line(left, 0.62 * inch, right, 0.62 * inch)
    canvas.setFont(FONT_REGULAR, 7.5)
    canvas.drawString(left, 0.44 * inch, FOOTER_LEFT)
    canvas.drawRightString(right, 0.44 * inch, f"Page {doc.page}")
    canvas.restoreState()


# ============================================================
# COVER PAGE
# ============================================================

def create_info_table(topic, styles, report_date):
    rows = [
        ("Project Title", PROJECT_TITLE),
        ("Research Topic", topic),
        ("Report Type", REPORT_LABEL),
        ("Submitted by", SUBMITTED_BY),
        ("Department", DEPARTMENT),
        ("Faculty Mentor", FACULTY_MENTOR),
        ("Academic Year", ACADEMIC_YEAR),
        ("Date", report_date),
    ]
    data = [[Paragraph("Field", styles["th"]), Paragraph("Details", styles["th"])]]
    for label, value in rows:
        data.append([
            Paragraph(format_inline(label), styles["td"]),
            Paragraph(format_inline(value), styles["td"]),
        ])

    table = Table(data, colWidths=[1.75 * inch, 5.1 * inch], repeatRows=1, hAlign="CENTER")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    table.setStyle(TableStyle(style))
    return table


# ============================================================
# MARKDOWN TABLES
# ============================================================

def is_table_line(line):
    line = line.strip()
    return line.startswith("|") and line.count("|") >= 2


def is_table_separator(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{1,}:?", c) for c in cells if c != "") and any(cells)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_table(rows, styles, total_width=6.9 * inch):
    if not rows:
        return None

    col_count = max(len(r) for r in rows)
    rows = [r + [""] * (col_count - len(r)) for r in rows]

    # Column widths proportional to content length (clamped), so short columns stay narrow.
    weights = []
    for c in range(col_count):
        longest = max(len(strip_markdown(r[c])) for r in rows)
        weights.append(min(max(longest, 12), 70) ** 0.8)
    total = sum(weights)
    col_widths = [total_width * w / total for w in weights]

    data = []
    for r_idx, row in enumerate(rows):
        style = styles["th"] if r_idx == 0 else styles["td"]
        data.append([Paragraph(format_inline(cell), style) for cell in row])

    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="CENTER")
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(2, len(data), 2):
        ts.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GREY))
    table.setStyle(TableStyle(ts))
    return table


# ============================================================
# MAIN
# ============================================================

_BULLET_RE = re.compile(r"^(\s*)([-*+\u2022\u25e6\u25cb\u25aa])\s+(.*)$")
_NUMBER_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
_HR_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")


def _flush_paragraph(buf, story, styles):
    if buf:
        text = " ".join(buf).strip()
        if text:
            story.append(Paragraph(format_inline(text), styles["body"]))
        buf.clear()


def create_pdf(report_text, filename="MAARA_Final_Report.pdf", report_date=None):
    if not report_text or not str(report_text).strip():
        raise ValueError("Report text is empty. PDF cannot be generated.")

    report_text = clean_text(str(report_text)).replace("\r\n", "\n")
    report_date = report_date or datetime.now().strftime("%B %Y")

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=0.70 * inch,
        rightMargin=0.70 * inch,
        topMargin=0.90 * inch,
        bottomMargin=0.85 * inch,
        title="MAARA Final Research Report",
        author=SUBMITTED_BY,
    )
    styles = create_styles()
    story = []

    # ---------------- Cover page ----------------
    topic = extract_topic(report_text)

    story.append(Spacer(1, 1.35 * inch))
    story.append(Paragraph("MULTI-AGENT AI RESEARCH ASSISTANT", styles["cover_title"]))
    story.append(Paragraph("MAARA", styles["cover_maara"]))
    story.append(Paragraph(REPORT_LABEL, styles["cover_report"]))
    story.append(Paragraph(COVER_SUBTITLE, styles["cover_subtitle"]))
    story.append(create_info_table(topic, styles, report_date))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph(
        "This report was generated from the research papers retrieved and analysed "
        "by the Multi-Agent AI Research Assistant (MAARA).",
        styles["cover_note"],
    ))
    story.append(PageBreak())

    # ---------------- Body ----------------
    lines = report_text.split("\n")
    para_buf = []
    last_heading = ""
    table_no = 0
    i = 0

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        # blank line -> end of paragraph
        if not stripped:
            _flush_paragraph(para_buf, story, styles)
            i += 1
            continue

        # horizontal rule -> ignore (never print literal ---)
        if _HR_RE.match(stripped):
            _flush_paragraph(para_buf, story, styles)
            i += 1
            continue

        # table
        if is_table_line(stripped):
            _flush_paragraph(para_buf, story, styles)
            rows = []
            while i < len(lines) and is_table_line(lines[i].strip()):
                row_line = lines[i].strip()
                if not is_table_separator(row_line):
                    rows.append(split_row(row_line))
                i += 1
            table = build_table(rows, styles)
            if table:
                table_no += 1
                caption_text = re.sub(r"^\d+(\.\d+)*\.?\s*", "", last_heading) or "Summary"
                caption = Paragraph(
                    f"Table {table_no}: {format_inline(caption_text)}", styles["caption"]
                )
                story.append(Spacer(1, 4))
                if len(rows) <= 8:
                    story.append(KeepTogether([table, caption]))
                else:
                    story.append(table)
                    story.append(caption)
            continue

        # headings  (#, ##, ###, ####)
        m = _HEADING_RE.match(line)
        if m:
            _flush_paragraph(para_buf, story, styles)
            level = len(stripped) - len(stripped.lstrip("#"))
            title = strip_markdown(m.group(1))
            if not title:
                i += 1
                continue
            last_heading = title
            if level == 1 and title.lower() in {"maara", "research report", "final research report"}:
                i += 1
                continue
            style_key = "h1" if level <= 2 else ("h2" if level == 3 else "h3")
            story.append(Paragraph(format_inline(title), styles[style_key]))
            i += 1
            continue

        # bullets
        m = _BULLET_RE.match(line)
        if m and not re.match(r"^\s*\*\*[^*]+\*\*\s*$", stripped):
            _flush_paragraph(para_buf, story, styles)
            indent = len(m.group(1).replace("\t", "    "))
            level2 = indent >= 2
            story.append(Paragraph(
                format_inline(m.group(3)),
                styles["bullet2" if level2 else "bullet"],
                bulletText="\u2013" if level2 else "\u2022",
            ))
            i += 1
            continue

        # numbered list
        m = _NUMBER_RE.match(line)
        if m:
            _flush_paragraph(para_buf, story, styles)
            indent = len(m.group(1).replace("\t", "    "))
            story.append(Paragraph(
                format_inline(m.group(3)),
                styles["number2" if indent >= 2 else "number"],
                bulletText=f"{m.group(2)}.",
            ))
            i += 1
            continue

        # a lone **Bold line** acts as a sub-heading
        if re.fullmatch(r"\*\*[^*]+\*\*:?", stripped):
            _flush_paragraph(para_buf, story, styles)
            story.append(Paragraph(format_inline(stripped), styles["h3"]))
            i += 1
            continue

        # normal text (wrapped lines are joined into one paragraph)
        para_buf.append(stripped)
        i += 1

    _flush_paragraph(para_buf, story, styles)

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return filename