#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"
APPLICATIONS_DIR = ROOT / "applications"
STYLE_TEX = TEMPLATES_DIR / "style.tex"
COVER_LETTER_STYLE_TEX = TEMPLATES_DIR / "cover_letter_style.tex"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
    if not m:
        return {}
    raw = m.group(1)
    result = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
    return result


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unknown"


def ensure_dirs():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd: list, cwd: Path):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)


def build_outputs(input_md: Path, company: str, role: str, formats: list):
    ensure_dirs()
    if APPLICATIONS_DIR in input_md.parents:
        out_dir = input_md.parent
    else:
        out_dir = APPLICATIONS_DIR / f"{slugify(company)}-{slugify(role)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    if which("pandoc") is None:
        print(
            "pandoc not found. Install pandoc to use the build pipeline.",
            file=sys.stderr,
        )
        sys.exit(1)
    base_name = input_md.stem
    if "pdf" in formats:
        pdf_out = out_dir / f"{base_name}.pdf"
        # Use cover letter style for cover_letter files, resume style for others
        style_file = COVER_LETTER_STYLE_TEX if "cover_letter" in base_name else STYLE_TEX
        pdf_cmd = [
            "pandoc",
            str(input_md),
            "-o",
            str(pdf_out),
            "--include-in-header",
            str(style_file),
            "--pdf-engine",
            "pdflatex",
            "--metadata=title=",
            "--metadata=author=",
            "--metadata=date=",
        ]
        r = run(pdf_cmd, ROOT)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            print("PDF build failed.", file=sys.stderr)
        else:
            print(f"Built {pdf_out}")
    if "docx" in formats:
        docx_out = out_dir / f"{base_name}.docx"
        docx_cmd = [
            "pandoc",
            str(input_md),
            "-o",
            str(docx_out),
        ]
        r = run(docx_cmd, ROOT)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            print("DOCX build failed.", file=sys.stderr)
        else:
            print(f"Built {docx_out}")
    if "txt" in formats:
        txt_out = out_dir / f"{base_name}.txt"
        txt_cmd = [
            "pandoc",
            str(input_md),
            "-t",
            "plain",
            "-o",
            str(txt_out),
        ]
        r = run(txt_cmd, ROOT)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            print("TXT build failed.", file=sys.stderr)
        else:
            print(f"Built {txt_out}")


def main():
    p = argparse.ArgumentParser(
        prog="build_resume",
        description="Build resume/cover letter outputs from Markdown.",
    )
    p.add_argument("input", help="Path to input Markdown file")
    p.add_argument("--company", help="Company name override")
    p.add_argument("--role", help="Role name override")
    p.add_argument(
        "--formats",
        default="pdf,docx,txt",
        help="Comma-separated formats: pdf,docx,txt",
    )
    args = p.parse_args()
    input_md = Path(args.input).resolve()
    if not input_md.exists():
        print("Input Markdown not found.", file=sys.stderr)
        sys.exit(1)
    text = read_file(input_md)
    fm = parse_frontmatter(text)
    company = args.company or fm.get("company") or "Company"
    role = args.role or fm.get("role") or "Role"
    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    build_outputs(input_md, company, role, formats)


if __name__ == "__main__":
    main()
