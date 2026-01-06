#!/usr/bin/env python3
"""Career Architect CLI - Unified command interface for job application workflow.

Usage:
    python scripts/career.py <command> [options]

Commands:
    new         Create a new job application
    build       Build documents for an application
    list        List all applications
    status      Show project status and statistics
    validate    Validate source materials
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLICATIONS_DIR = ROOT / "applications"
SOURCE_DIR = ROOT / "source_materials"
IDENTITY_JSON = SOURCE_DIR / "identity.json"
MASTER_EXP = SOURCE_DIR / "master_experience.md"

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def log(icon: str, msg: str, color: str = RESET):
    print(f"{color}{icon}{RESET} {msg}")


def cmd_new(args):
    """Create a new job application directory."""
    date = datetime.now().strftime("%Y-%m-%d")

    # Get company and role
    company = args.company or input("Company name: ").strip()
    role = args.role or input("Role title: ").strip()

    if not company or not role:
        log("✗", "Company and role are required", RED)
        return 1

    # Create slug
    slug = f"{company}-{role}".lower()
    slug = "-".join(slug.split())
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
    slug = "-".join(filter(None, slug.split("-")))

    folder_name = f"{date}-{slug}"
    app_dir = APPLICATIONS_DIR / folder_name

    if app_dir.exists():
        log("⚠", f"Application already exists: {folder_name}", YELLOW)
        return 1

    app_dir.mkdir(parents=True, exist_ok=True)

    # Create job_desc.md
    job_desc = app_dir / "job_desc.md"
    job_desc.write_text(
        f"""---
company: {company}
role: {role}
date: {date}
status: draft
---

# {company} - {role}

## Job Description

Paste the job description here.

## Key Requirements

- 

## Notes

- 
""",
        encoding="utf-8",
    )

    log("✓", f"Created: {app_dir.relative_to(ROOT)}", GREEN)
    log("ℹ", f"Next: Edit {job_desc.relative_to(ROOT)}", BLUE)

    return 0


def cmd_build(args):
    """Build documents using compile_all.py."""
    cmd = [sys.executable, str(ROOT / "scripts" / "compile_all.py")]

    if args.all:
        cmd.append("--all")
    if args.application:
        cmd.extend(["--application", args.application])
    if args.force:
        cmd.append("--force")
    if args.formats:
        cmd.extend(["--formats", args.formats])

    return subprocess.run(cmd, cwd=str(ROOT)).returncode


def cmd_list(args):
    """List applications using compile_all.py."""
    cmd = [sys.executable, str(ROOT / "scripts" / "compile_all.py"), "--list"]
    return subprocess.run(cmd, cwd=str(ROOT)).returncode


def cmd_status(args):
    """Show project status and statistics."""
    print(f"\n{BOLD}Career Architect Status{RESET}\n")

    # Check source materials
    print(f"{BOLD}Source Materials:{RESET}")

    if IDENTITY_JSON.exists():
        try:
            identity = json.loads(IDENTITY_JSON.read_text())
            name = identity.get("full_name", "Not set")
            if name == "Your Name":
                log("⚠", f"Identity: {name} (update required)", YELLOW)
            else:
                log("✓", f"Identity: {name}", GREEN)
        except json.JSONDecodeError:
            log("✗", "Identity: Invalid JSON", RED)
    else:
        log("✗", "Identity: Missing", RED)

    if MASTER_EXP.exists():
        content = MASTER_EXP.read_text()
        lines = len(content.splitlines())
        if lines > 50:
            log("✓", f"Master Experience: {lines} lines", GREEN)
        else:
            log("⚠", f"Master Experience: {lines} lines (needs more content)", YELLOW)
    else:
        log("✗", "Master Experience: Missing", RED)

    # Count applications
    print(f"\n{BOLD}Applications:{RESET}")

    if APPLICATIONS_DIR.exists():
        apps = [d for d in APPLICATIONS_DIR.iterdir() if d.is_dir()]
        total = len(apps)

        with_resume = sum(1 for a in apps if (a / "resume.md").exists())
        with_cover = sum(1 for a in apps if (a / "cover_letter.md").exists())
        with_pdf = sum(1 for a in apps if (a / "resume.pdf").exists())

        log("📁", f"Total: {total}", BLUE)
        log("📄", f"With resume.md: {with_resume}", BLUE)
        log("✉️", f"With cover_letter.md: {with_cover}", BLUE)
        log("📑", f"With PDF: {with_pdf}", BLUE)
    else:
        log("ℹ", "No applications yet", BLUE)

    print()
    return 0


def cmd_validate(args):
    """Validate source materials and configuration."""
    print(f"\n{BOLD}Validating Source Materials{RESET}\n")

    errors = 0
    warnings = 0

    # Check identity.json
    if not IDENTITY_JSON.exists():
        log("✗", "identity.json not found", RED)
        errors += 1
    else:
        try:
            identity = json.loads(IDENTITY_JSON.read_text())
            required = ["full_name", "email", "phone", "location"]
            for field in required:
                val = identity.get(field, "")
                if not val or val.startswith("Your") or val.startswith("your"):
                    log("⚠", f"identity.json: '{field}' needs to be set", YELLOW)
                    warnings += 1
                else:
                    log("✓", f"identity.json: '{field}' ✓", GREEN)
        except json.JSONDecodeError as e:
            log("✗", f"identity.json: Invalid JSON - {e}", RED)
            errors += 1

    # Check master_experience.md
    if not MASTER_EXP.exists():
        log("✗", "master_experience.md not found", RED)
        errors += 1
    else:
        content = MASTER_EXP.read_text()
        if "[Company Name]" in content:
            log("⚠", "master_experience.md: Contains template placeholders", YELLOW)
            warnings += 1
        else:
            log("✓", "master_experience.md: Exists", GREEN)

    # Check templates
    templates = ROOT / "templates"
    for tmpl in ["style.tex", "cover_letter_style.tex"]:
        if (templates / tmpl).exists():
            log("✓", f"templates/{tmpl}: Exists", GREEN)
        else:
            log("✗", f"templates/{tmpl}: Missing", RED)
            errors += 1

    # Summary
    print(f"\n{BOLD}Summary:{RESET}")
    if errors == 0 and warnings == 0:
        log("✓", "All checks passed!", GREEN)
    else:
        if errors:
            log("✗", f"{errors} error(s)", RED)
        if warnings:
            log("⚠", f"{warnings} warning(s)", YELLOW)

    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(
        prog="career",
        description="Career Architect - Job Application Pipeline CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # new command
    new_parser = subparsers.add_parser("new", help="Create new application")
    new_parser.add_argument("--company", "-c", help="Company name")
    new_parser.add_argument("--role", "-r", help="Role title")

    # build command
    build_parser = subparsers.add_parser("build", help="Build documents")
    build_parser.add_argument("--all", action="store_true", help="Build all")
    build_parser.add_argument("--application", "-a", help="Specific application")
    build_parser.add_argument(
        "--force", "-f", action="store_true", help="Force rebuild"
    )
    build_parser.add_argument(
        "--formats", default="pdf,docx,txt", help="Output formats"
    )

    # list command
    subparsers.add_parser("list", help="List applications")

    # status command
    subparsers.add_parser("status", help="Show project status")

    # validate command
    subparsers.add_parser("validate", help="Validate source materials")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "new": cmd_new,
        "build": cmd_build,
        "list": cmd_list,
        "status": cmd_status,
        "validate": cmd_validate,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
