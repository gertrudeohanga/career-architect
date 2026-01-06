import os
import subprocess
import argparse
from pathlib import Path


def get_resume_paths(base_dir: Path, application: str = None, all_apps: bool = False):
    """Get resume paths to process based on options."""
    if application:
        # Process specific application
        app_dir = base_dir / application
        resume_path = app_dir / "resume.md"
        if resume_path.exists():
            return [resume_path]
        else:
            print(f"Application '{application}' not found or has no resume.md")
            return []

    if not all_apps:
        # Default: process only the most recently modified application
        app_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
        if not app_dirs:
            return []

        # Sort by modification time, most recent first
        app_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
        most_recent = app_dirs[0]
        resume_path = most_recent / "resume.md"
        if resume_path.exists():
            print(f"🎯 Processing most recent application: {most_recent.name}")
            return [resume_path]
        else:
            print(f"Most recent application '{most_recent.name}' has no resume.md")
            return []

    # Process all applications
    return list(base_dir.glob("**/resume.md"))


def auto_build(application: str = None, all_apps: bool = False):
    base_dir = Path("applications")
    resume_paths = get_resume_paths(base_dir, application, all_apps)

    for resume_path in resume_paths:
        pdf_path = resume_path.with_name("final_resume.pdf")

        # Only build if PDF is missing or Markdown is newer
        if (
            not pdf_path.exists()
            or resume_path.stat().st_mtime > pdf_path.stat().st_mtime
        ):
            print(f"🔨 Building: {pdf_path}")
            subprocess.run(["python", "scripts/build_resume.py", str(resume_path)])
        else:
            print(f"⏭️  Skipping {pdf_path} (already up to date)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build resume PDFs for job applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compile_all.py                    # Build only the most recent application (default)
  python compile_all.py --all             # Build all applications that need updating
  python compile_all.py --application "2025-12-29-eterno-full-stack-engineer-healthtech-senior-lead"
                                         # Build specific application
        """,
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all applications that need updating (instead of just the most recent)",
    )
    parser.add_argument(
        "--application", type=str, help="Build a specific application directory name"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.all and args.application:
        parser.error("--all and --application cannot be used together")

    auto_build(application=args.application, all_apps=args.all)
