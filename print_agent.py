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
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
import reportlab


DEFAULT_BASE_URL = "https://gute-nachrichten.info"
DEFAULT_OUTPUT_DIR = Path("output/pdf")
SIGNATURE_PATH = Path(__file__).resolve().parent / "assets" / "signature.png"
SIGNATURE_WIDTH = 48 * mm


def _layout_sizes(news):
    text_length = len(news)
    if text_length <= 850:
        return {"title": 28, "title_leading": 34, "body": 18, "body_leading": 25}
    if text_length <= 1200:
        return {"title": 26, "title_leading": 32, "body": 17, "body_leading": 24}
    if text_length <= 1600:
        return {"title": 24, "title_leading": 30, "body": 16, "body_leading": 23}
    return {"title": 22, "title_leading": 28, "body": 15, "body_leading": 22}


def _split_weather_fallback(paragraph):
    weather_start = None
    weather_pattern = re.compile(
        r" (?=(?:In|Über|Für|Bei) [A-ZÄÖÜ][^.!?]{0,90}"
        r"\b(?:liegt|ziehen|herrscht|zeigt|weht|breitet|hängt|scheint|sorgt|wirkt|bleibt|ist)\b)"
    )
    for match in weather_pattern.finditer(paragraph):
        if match.start() > len(paragraph) * 0.55:
            weather_start = match.start() + 1

    if weather_start is None:
        return [paragraph]

    return [
        paragraph[:weather_start].strip(),
        paragraph[weather_start:].strip(),
    ]


def split_news_paragraphs(news):
    normalized = re.sub(r"\r\n?", "\n", news).strip()
    paragraphs = [
        re.sub(r"\s*\n\s*", " ", part).strip()
        for part in re.split(r"\n\s*\n", normalized)
        if part.strip()
    ]
    if len(paragraphs) == 1:
        return _split_weather_fallback(paragraphs[0])
    return paragraphs


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


def draw_signature(canvas, _doc):
    if not SIGNATURE_PATH.exists():
        return

    image = ImageReader(str(SIGNATURE_PATH))
    image_width, image_height = image.getSize()
    signature_height = SIGNATURE_WIDTH * image_height / image_width
    page_width, _page_height = A4
    x = page_width - 16 * mm - SIGNATURE_WIDTH
    y = 8 * mm
    canvas.drawImage(
        image,
        x,
        y,
        width=SIGNATURE_WIDTH,
        height=signature_height,
        mask="auto",
    )


def build_pdf(news, output_path):
    fonts = register_fonts()
    sizes = _layout_sizes(news)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=20 * mm,
        bottomMargin=24 * mm,
    )
    title_style = ParagraphStyle(
        "Title",
        fontName=fonts["bold"],
        fontSize=sizes["title"],
        leading=sizes["title_leading"],
        spaceAfter=8 * mm,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName=fonts["regular"],
        fontSize=sizes["body"],
        leading=sizes["body_leading"],
    )

    paragraphs = split_news_paragraphs(news)
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
            story.append(Spacer(1, 6 * mm))
            story.append(Paragraph(escape(paragraph), body_style))

    doc.build(story, onFirstPage=draw_signature, onLaterPages=draw_signature)


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
