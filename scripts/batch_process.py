#!/usr/bin/env python3
"""Batch Process - Process multiple job descriptions at once.

This script allows you to:
- Import multiple JDs from a folder
- Create application folders for each
- Generate a batch report
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLICATIONS_DIR = ROOT / "applications"

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def log(icon: str, msg: str, color: str = RESET):
    print(f"{color}{icon}{RESET} {msg}")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def extract_metadata(content: str) -> dict:
    """Extract company and role from JD content."""
    metadata = {"company": "", "role": ""}

    lines = content.strip().split("\n")

    # Try to find company/role from first few lines
    for line in lines[:10]:
        line = line.strip()

        # Check for "Company: X" or "Company - X" patterns
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.lower().strip()
            val = val.strip()
            if "company" in key and not metadata["company"]:
                metadata["company"] = val
            elif "role" in key or "title" in key or "position" in key:
                if not metadata["role"]:
                    metadata["role"] = val

        # Check for markdown headers
        if line.startswith("# ") and not metadata["company"]:
            # First H1 might be company or role
            header = line[2:].strip()
            if " - " in header:
                parts = header.split(" - ", 1)
                metadata["company"] = parts[0].strip()
                metadata["role"] = parts[1].strip()
            elif not metadata["role"]:
                metadata["role"] = header

    return metadata


def create_application(content: str, company: str, role: str) -> Path:
    """Create application folder from JD content."""
    date = datetime.now().strftime("%Y-%m-%d")
    slug = f"{date}-{slugify(company)}-{slugify(role)}"
    app_dir = APPLICATIONS_DIR / slug

    if app_dir.exists():
        return None  # Skip duplicates

    app_dir.mkdir(parents=True, exist_ok=True)

    # Create job_desc.md with frontmatter
    job_desc = app_dir / "job_desc.md"
    frontmatter = f"""---
company: {company}
role: {role}
date_added: {date}
status: draft
source: batch_import
---

"""
    job_desc.write_text(frontmatter + content, encoding="utf-8")
    return app_dir


def process_folder(input_dir: Path, dry_run: bool = False) -> dict:
    """Process all .md and .txt files in a folder."""
    results = {"processed": [], "skipped": [], "errors": []}

    if not input_dir.exists():
        log("✗", f"Input folder not found: {input_dir}", RED)
        return results

    files = list(input_dir.glob("*.md")) + list(input_dir.glob("*.txt"))

    if not files:
        log("⚠", "No .md or .txt files found", YELLOW)
        return results

    log("ℹ", f"Found {len(files)} job description(s)", BLUE)
    print()

    for f in files:
        try:
            content = f.read_text(encoding="utf-8")
            metadata = extract_metadata(content)

            # Try to get company/role from filename if not found
            if not metadata["company"] or not metadata["role"]:
                name = f.stem
                if "-" in name:
                    parts = name.split("-", 1)
                    if not metadata["company"]:
                        metadata["company"] = parts[0].replace("_", " ").title()
                    if not metadata["role"] and len(parts) > 1:
                        metadata["role"] = parts[1].replace("_", " ").title()

            if not metadata["company"]:
                metadata["company"] = "Unknown"
            if not metadata["role"]:
                metadata["role"] = "Position"

            if dry_run:
                log("→", f"{f.name}", BLUE)
                print(f"    Company: {metadata['company']}")
                print(f"    Role: {metadata['role']}")
                results["processed"].append(f.name)
            else:
                app_dir = create_application(
                    content, metadata["company"], metadata["role"]
                )
                if app_dir:
                    log("✓", f"{f.name} → {app_dir.name}", GREEN)
                    results["processed"].append(app_dir.name)
                else:
                    log("⚠", f"{f.name} (skipped - already exists)", YELLOW)
                    results["skipped"].append(f.name)

        except Exception as e:
            log("✗", f"{f.name}: {e}", RED)
            results["errors"].append(f.name)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch process multiple job descriptions"
    )
    parser.add_argument("input", help="Folder containing JD files (.md or .txt)")
    parser.add_argument(
        "--dry-run", "-n", action="store_true", help="Preview without creating folders"
    )

    args = parser.parse_args()
    input_dir = Path(args.input)

    print(f"\n{BOLD}Batch Processing Job Descriptions{RESET}\n")

    if args.dry_run:
        log("ℹ", "DRY RUN - No folders will be created", BLUE)
        print()

    results = process_folder(input_dir, args.dry_run)

    # Summary
    print(f"\n{BOLD}Summary{RESET}")
    print(f"  Processed: {len(results['processed'])}")
    print(f"  Skipped:   {len(results['skipped'])}")
    print(f"  Errors:    {len(results['errors'])}")

    if not args.dry_run and results["processed"]:
        print(f"\n{BOLD}Next Steps{RESET}")
        print("  1. Review job descriptions in applications/")
        print("  2. Run: python scripts/career.py list")
        print("  3. Use AI assistant with each application")

    return 0 if not results["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
