import argparse
import re
import time
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import reportlab


DEFAULT_BASE_URL = "https://gute-nachrichten.info"
DEFAULT_OUTPUT_DIR = Path("output/pdf")


def _layout_sizes(news):
    text_length = len(news)
    if text_length <= 850:
        return {"title": 36, "title_leading": 43, "body": 24, "body_leading": 33}
    if text_length <= 1200:
        return {"title": 34, "title_leading": 40, "body": 22, "body_leading": 30}
    if text_length <= 1600:
        return {"title": 31, "title_leading": 37, "body": 20, "body_leading": 27}
    return {"title": 28, "title_leading": 34, "body": 18, "body_leading": 25}


def _find_reportlab_font(filename):
    path = Path(reportlab.__file__).resolve().parent / "fonts" / filename
    if path.exists():
        return path
    return None


def register_fonts():
    regular = _find_reportlab_font("Vera.ttf")
    bold = _find_reportlab_font("VeraBd.ttf")
    if regular:
        pdfmetrics.registerFont(TTFont("GoodNews", regular))
    if bold:
        pdfmetrics.registerFont(TTFont("GoodNews-Bold", bold))

    return {
        "regular": "GoodNews" if regular else "Helvetica",
        "bold": "GoodNews-Bold" if bold else "Helvetica-Bold",
    }


def safe_filename(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value or "goodnews"


def build_pdf(news, output_path):
    fonts = register_fonts()
    sizes = _layout_sizes(news)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    title_style = ParagraphStyle(
        "Title",
        fontName=fonts["bold"],
        fontSize=sizes["title"],
        leading=sizes["title_leading"],
        spaceAfter=10 * mm,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName=fonts["regular"],
        fontSize=sizes["body"],
        leading=sizes["body_leading"],
    )

    paragraphs = [part.strip() for part in news.split("\n\n") if part.strip()]
    story = []
    if paragraphs:
        first = paragraphs[0]
        prefix = "Gute Nachricht!"
        if first.startswith(prefix):
            story.append(Paragraph(escape(prefix), title_style))
            rest = first[len(prefix):].strip()
            if rest:
                story.append(Paragraph(escape(rest), body_style))
        else:
            story.append(Paragraph(escape(first), body_style))

        for paragraph in paragraphs[1:]:
            story.append(Spacer(1, 7 * mm))
            story.append(Paragraph(escape(paragraph), body_style))

    doc.build(story)


def fetch_jobs(base_url, timeout):
    response = requests.get(f"{base_url.rstrip('/')}/print/jobs", timeout=timeout)
    response.raise_for_status()
    return response.json()["jobs"]


def mark_done(base_url, job_id, timeout):
    response = requests.post(
        f"{base_url.rstrip('/')}/print/jobs/{job_id}/done",
        timeout=timeout,
    )
    response.raise_for_status()


def process_once(base_url, output_dir, timeout):
    jobs = fetch_jobs(base_url, timeout)
    created = []
    for job in jobs:
        timestamp = datetime.fromtimestamp(job["created_at"]).strftime("%Y%m%d-%H%M%S")
        filename = safe_filename(f"goodnews-{job['id']}-{timestamp}.pdf")
        output_path = output_dir / filename
        build_pdf(job["news"], output_path)
        mark_done(base_url, job["id"], timeout)
        created.append(output_path)
        print(f"Saved {output_path}")
    return created


def main():
    parser = argparse.ArgumentParser(description="Fetch Good News print jobs and save PDFs.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    while True:
        process_once(args.base_url, args.output_dir, args.timeout)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
