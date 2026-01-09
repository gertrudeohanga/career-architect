#!/usr/bin/env python3
"""Job Scraper - Extract job descriptions from URLs.

Supports:
- LinkedIn job postings
- Indeed job listings
- Greenhouse job boards
- Lever job boards
- Generic job pages

Usage:
    python scripts/job_scraper.py <url>
    python scripts/job_scraper.py <url> --create
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup

    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

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
    return text.strip("-")[:50]


def extract_linkedin(soup: BeautifulSoup, url: str) -> dict:
    """Extract job details from LinkedIn."""
    data = {"company": "", "role": "", "description": "", "source": url}

    # Title
    title_elem = soup.find("h1", class_="top-card-layout__title")
    if title_elem:
        data["role"] = title_elem.get_text(strip=True)

    # Company
    company_elem = soup.find("a", class_="topcard__org-name-link")
    if company_elem:
        data["company"] = company_elem.get_text(strip=True)

    # Description
    desc_elem = soup.find("div", class_="description__text")
    if desc_elem:
        data["description"] = desc_elem.get_text(separator="\n", strip=True)

    return data


def extract_indeed(soup: BeautifulSoup, url: str) -> dict:
    """Extract job details from Indeed."""
    data = {"company": "", "role": "", "description": "", "source": url}

    # Title
    title_elem = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
    if title_elem:
        data["role"] = title_elem.get_text(strip=True)

    # Company
    company_elem = soup.find("div", {"data-testid": "inlineHeader-companyName"})
    if company_elem:
        data["company"] = company_elem.get_text(strip=True)

    # Description
    desc_elem = soup.find("div", id="jobDescriptionText")
    if desc_elem:
        data["description"] = desc_elem.get_text(separator="\n", strip=True)

    return data


def extract_greenhouse(soup: BeautifulSoup, url: str) -> dict:
    """Extract job details from Greenhouse boards."""
    data = {"company": "", "role": "", "description": "", "source": url}

    # Title
    title_elem = soup.find("h1", class_="app-title")
    if title_elem:
        data["role"] = title_elem.get_text(strip=True)

    # Company from URL or page
    company_elem = soup.find("span", class_="company-name")
    if company_elem:
        data["company"] = company_elem.get_text(strip=True)
    else:
        # Try to get from URL
        parsed = urlparse(url)
        if "boards.greenhouse.io" in parsed.netloc:
            path_parts = parsed.path.strip("/").split("/")
            if path_parts:
                data["company"] = path_parts[0].replace("-", " ").title()

    # Description
    desc_elem = soup.find("div", id="content")
    if desc_elem:
        data["description"] = desc_elem.get_text(separator="\n", strip=True)

    return data


def extract_lever(soup: BeautifulSoup, url: str) -> dict:
    """Extract job details from Lever boards."""
    data = {"company": "", "role": "", "description": "", "source": url}

    # Title
    title_elem = soup.find("h2")
    if title_elem:
        data["role"] = title_elem.get_text(strip=True)

    # Company from URL
    parsed = urlparse(url)
    if "jobs.lever.co" in parsed.netloc:
        path_parts = parsed.path.strip("/").split("/")
        if path_parts:
            data["company"] = path_parts[0].replace("-", " ").title()

    # Description
    desc_elem = soup.find("div", class_="section-wrapper")
    if desc_elem:
        data["description"] = desc_elem.get_text(separator="\n", strip=True)

    return data


def extract_generic(soup: BeautifulSoup, url: str) -> dict:
    """Generic extraction for unknown job boards."""
    data = {"company": "", "role": "", "description": "", "source": url}

    # Try to find title from h1 or title tag
    h1 = soup.find("h1")
    if h1:
        data["role"] = h1.get_text(strip=True)
    elif soup.title:
        data["role"] = soup.title.get_text(strip=True).split("|")[0].strip()

    # Try to extract company from meta or URL
    parsed = urlparse(url)
    domain_parts = parsed.netloc.split(".")
    if len(domain_parts) >= 2:
        data["company"] = domain_parts[-2].title()

    # Get main content
    # Try common content containers
    for selector in [
        "main",
        "article",
        ".job-description",
        "#job-description",
        ".content",
        "#content",
    ]:
        elem = soup.select_one(selector)
        if elem:
            data["description"] = elem.get_text(separator="\n", strip=True)
            break

    # Fallback to body
    if not data["description"]:
        body = soup.find("body")
        if body:
            # Remove script and style
            for tag in body(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            data["description"] = body.get_text(separator="\n", strip=True)

    return data


def fetch_job(url: str) -> dict:
    """Fetch and parse a job posting URL."""
    if not HAS_DEPS:
        log("✗", "Missing dependencies. Run: pip install requests beautifulsoup4", RED)
        return None

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        log("ℹ", f"Fetching: {url}", BLUE)
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        log("✗", f"Failed to fetch URL: {e}", RED)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    parsed = urlparse(url)

    # Route to appropriate extractor
    if "linkedin.com" in parsed.netloc:
        data = extract_linkedin(soup, url)
    elif "indeed.com" in parsed.netloc:
        data = extract_indeed(soup, url)
    elif "greenhouse.io" in parsed.netloc:
        data = extract_greenhouse(soup, url)
    elif "lever.co" in parsed.netloc:
        data = extract_lever(soup, url)
    else:
        data = extract_generic(soup, url)

    return data


def create_application(data: dict) -> Path:
    """Create application folder from scraped data."""
    if not data.get("company") or not data.get("role"):
        log("⚠", "Could not extract company/role. Please provide manually.", YELLOW)
        data["company"] = data.get("company") or input("Company name: ").strip()
        data["role"] = data.get("role") or input("Role title: ").strip()

    date = datetime.now().strftime("%Y-%m-%d")
    slug = f"{date}-{slugify(data['company'])}-{slugify(data['role'])}"
    app_dir = APPLICATIONS_DIR / slug

    if app_dir.exists():
        log("⚠", f"Application already exists: {slug}", YELLOW)
        return app_dir

    app_dir.mkdir(parents=True, exist_ok=True)

    # Create job_desc.md
    content = f"""---
company: {data['company']}
role: {data['role']}
date_added: {date}
status: draft
source_url: {data.get('source', '')}
---

# {data['company']} - {data['role']}

## Job Description

{data.get('description', 'No description extracted.')}

## Key Requirements

-

## Notes

- Imported from: {data.get('source', 'URL')}
"""

    (app_dir / "job_desc.md").write_text(content, encoding="utf-8")
    return app_dir


def main():
    parser = argparse.ArgumentParser(description="Scrape job descriptions from URLs")
    parser.add_argument("url", help="Job posting URL")
    parser.add_argument(
        "--create", "-c", action="store_true", help="Create application folder"
    )
    parser.add_argument("--output", "-o", help="Output file (default: print to stdout)")

    args = parser.parse_args()

    print(f"\n{BOLD}Job Scraper{RESET}\n")

    data = fetch_job(args.url)

    if not data:
        return 1

    log("✓", f"Company: {data.get('company', 'Unknown')}", GREEN)
    log("✓", f"Role: {data.get('role', 'Unknown')}", GREEN)

    desc_preview = data.get("description", "")[:200]
    if desc_preview:
        log("ℹ", f"Description: {desc_preview}...", BLUE)

    if args.create:
        app_dir = create_application(data)
        if app_dir:
            log("✓", f"Created: {app_dir.name}", GREEN)
            log("ℹ", f"Edit: {app_dir / 'job_desc.md'}", BLUE)
    elif args.output:
        Path(args.output).write_text(data.get("description", ""), encoding="utf-8")
        log("✓", f"Saved to: {args.output}", GREEN)
    else:
        print(f"\n{BOLD}Full Description:{RESET}\n")
        print(data.get("description", "No description found."))

    return 0


if __name__ == "__main__":
    sys.exit(main())
