"""Local scholarship workspace and deliberately limited Markdown PDF builder."""
import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]


def validate(path):
    content = path.read_text(encoding="utf-8-sig")
    if not content.strip():
        raise ValueError("文件不可空白")
    if re.search(r"\{\{|\}\}|\bTODO\b|\bTBD\b|待補|待確認|\[ \]", content):
        raise ValueError("仍有占位符、待確認內容或未完成清單")
    if re.search(r"(?m)^\s*\||```|!\[|<[^>]+>", content):
        raise ValueError("含不支援的表格、程式碼區塊、圖片或 HTML；請使用專用文件工具")
    return content


def initialize(case_id):
    if not re.fullmatch(r"[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
        raise ValueError("案件 ID 格式須為 2026-esun")
    case = ROOT / "applications" / case_id
    for folder in ("private/source", "drafts", "output", "submission"):
        (case / folder).mkdir(parents=True, exist_ok=True)
    for source, destination in (
        (ROOT / "templates/case.md", case / "private/status.md"),
        (ROOT / "templates/profile.md", ROOT / "private/profile.md"),
        (ROOT / "templates/evidence.md", ROOT / "private/evidence-index.md"),
    ):
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    (ROOT / "private/evidence").mkdir(parents=True, exist_ok=True)
    print(f"案件已建立（保留既有檔案）：{case}")


def build_pdf(source, output):
    content = validate(source)
    if output.suffix.lower() != ".pdf":
        raise ValueError("輸出副檔名必須為 .pdf")
    if output.exists():
        raise ValueError("輸出檔已存在；請另用版本名稱，避免覆蓋")
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

    pdfmetrics.registerFont(UnicodeCIDFont("MSung-Light"))
    base = dict(fontName="MSung-Light", wordWrap="CJK", alignment=TA_LEFT)
    styles = {
        "body": ParagraphStyle("body", fontSize=11, leading=19, spaceAfter=9, **base),
        "h1": ParagraphStyle("h1", fontSize=21, leading=29, spaceAfter=18, **base),
        "h2": ParagraphStyle("h2", fontSize=15, leading=23, spaceBefore=12, spaceAfter=9, **base),
        "h3": ParagraphStyle("h3", fontSize=12, leading=20, spaceBefore=8, spaceAfter=6, **base),
    }
    story = []
    paragraph = []

    def inline(value):
        # Expose link destinations in print instead of silently discarding them.
        value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", value)
        value = value.replace("**", "").replace("`", "")
        return escape(value)

    def flush():
        if paragraph:
            story.append(Paragraph(inline(" ".join(paragraph)), styles["body"]))
            paragraph.clear()

    for line in content.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        bullet = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", line)
        if not line.strip():
            flush()
        elif heading:
            flush()
            story.append(Paragraph(inline(heading[2]), styles[f"h{min(len(heading[1]), 3)}"]))
        elif bullet:
            flush()
            story.append(Paragraph(inline(line.strip()), styles["body"]))
        else:
            paragraph.append(line.strip())
    flush()

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("MSung-Light", 9)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.drawCentredString(A4[0] / 2, 28, str(document.page))
        canvas.restoreState()

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=52,
        leftMargin=52, topMargin=50, bottomMargin=48, title=source.stem)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF 已產出，仍需逐頁視覺與官方格式審查：{output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("case_id")
    check = commands.add_parser("check")
    check.add_argument("source", type=Path)
    pdf = commands.add_parser("pdf")
    pdf.add_argument("source", type=Path)
    pdf.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "init":
            initialize(args.case_id)
        elif args.command == "check":
            content = validate(args.source)
            print(f"基本檢查通過；含空白字元 {len(content)} 字元。非官方字數計算或送件認證。")
        else:
            build_pdf(args.source, args.output)
    except (ValueError, OSError, ImportError) as error:
        parser.exit(1, f"錯誤：{error}\n")


if __name__ == "__main__":
    main()
