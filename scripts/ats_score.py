#!/usr/bin/env python3
"""ATS (Applicant Tracking System) Keyword Scoring Tool.

Analyzes resume against job description to calculate keyword match score
and identify missing keywords for ATS optimization.

Usage:
    python scripts/ats_score.py <job_desc.md> <resume.md>
    python scripts/ats_score.py applications/2025-01-01-company-role/
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Common stop words to exclude from analysis
STOP_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "as",
    "is",
    "was",
    "are",
    "were",
    "been",
    "be",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "must",
    "shall",
    "can",
    "need",
    "we",
    "you",
    "your",
    "our",
    "their",
    "this",
    "that",
    "these",
    "those",
    "it",
    "its",
    "they",
    "them",
    "he",
    "she",
    "his",
    "her",
    "who",
    "which",
    "what",
    "when",
    "where",
    "why",
    "how",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "just",
    "about",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "between",
    "under",
    "over",
    "out",
    "up",
    "down",
    "off",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "any",
    "also",
    "well",
    "work",
    "working",
    "worked",
    "experience",
    "years",
    "year",
    "team",
    "including",
    "using",
    "used",
    "use",
    "new",
    "help",
    "strong",
    "able",
}

# Technical keywords with higher weight
TECH_KEYWORDS = {
    # Languages
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "golang",
    "rust",
    "c++",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "scala",
    "r",
    "sql",
    # Frontend
    "react",
    "vue",
    "angular",
    "svelte",
    "nextjs",
    "next.js",
    "nuxt",
    "html",
    "css",
    "sass",
    "tailwind",
    "webpack",
    "vite",
    # Backend
    "node",
    "nodejs",
    "express",
    "fastapi",
    "django",
    "flask",
    "rails",
    "spring",
    "graphql",
    "rest",
    "api",
    "microservices",
    # Data
    "postgresql",
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "kafka",
    "rabbitmq",
    "dynamodb",
    "cassandra",
    # Cloud/DevOps
    "aws",
    "gcp",
    "azure",
    "docker",
    "kubernetes",
    "k8s",
    "terraform",
    "jenkins",
    "github",
    "gitlab",
    "ci/cd",
    "cicd",
    # AI/ML
    "machine learning",
    "ml",
    "ai",
    "llm",
    "nlp",
    "tensorflow",
    "pytorch",
    "openai",
    "langchain",
    "vector",
    "embeddings",
}


def extract_keywords(text: str) -> Counter:
    """Extract and count keywords from text."""
    # Normalize text
    text = text.lower()
    # Remove markdown formatting
    text = re.sub(r"[#*_`\[\](){}|>~]", " ", text)
    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    # Extract words (including hyphenated)
    words = re.findall(r"\b[a-z][a-z0-9+#.-]*\b", text)
    # Filter stop words and short words
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return Counter(keywords)


def extract_phrases(text: str) -> set:
    """Extract common multi-word phrases."""
    text = text.lower()
    phrases = set()

    # Common technical phrases to look for
    phrase_patterns = [
        r"full[- ]?stack",
        r"front[- ]?end",
        r"back[- ]?end",
        r"machine learning",
        r"deep learning",
        r"data science",
        r"software engineer",
        r"senior engineer",
        r"tech lead",
        r"team lead",
        r"product manager",
        r"project manager",
        r"ci/cd",
        r"test[- ]?driven",
        r"object[- ]?oriented",
        r"event[- ]?driven",
        r"real[- ]?time",
        r"open[- ]?source",
    ]

    for pattern in phrase_patterns:
        if re.search(pattern, text):
            # Normalize the match
            match = re.search(pattern, text).group()
            phrases.add(match.replace(" ", "-"))

    return phrases


def calculate_score(jd_keywords: Counter, resume_keywords: Counter) -> dict:
    """Calculate ATS match score."""
    # Get unique keywords from JD
    jd_unique = set(jd_keywords.keys())
    resume_unique = set(resume_keywords.keys())

    # Find matches
    matched = jd_unique & resume_unique
    missing = jd_unique - resume_unique

    # Calculate weighted score (tech keywords worth more)
    total_weight = 0
    matched_weight = 0

    for keyword in jd_unique:
        weight = 2 if keyword in TECH_KEYWORDS else 1
        weight *= jd_keywords[keyword]  # Frequency matters
        total_weight += weight

        if keyword in matched:
            matched_weight += weight

    score = (matched_weight / total_weight * 100) if total_weight > 0 else 0

    # Prioritize missing keywords by frequency and importance
    missing_ranked = []
    for keyword in missing:
        weight = 2 if keyword in TECH_KEYWORDS else 1
        weight *= jd_keywords[keyword]
        missing_ranked.append((keyword, weight, jd_keywords[keyword]))

    missing_ranked.sort(key=lambda x: x[1], reverse=True)

    return {
        "score": round(score, 1),
        "matched": len(matched),
        "total_jd": len(jd_unique),
        "missing": missing_ranked[:20],  # Top 20 missing
        "matched_keywords": sorted(matched),
    }


def print_report(result: dict, jd_path: str, resume_path: str):
    """Print the ATS score report."""
    score = result["score"]

    # Score color
    if score >= 70:
        score_color = Colors.GREEN
        verdict = "Strong Match"
    elif score >= 50:
        score_color = Colors.YELLOW
        verdict = "Moderate Match"
    else:
        score_color = Colors.RED
        verdict = "Needs Improvement"

    print(f"\n{Colors.BOLD}ATS Keyword Analysis{Colors.RESET}")
    print("=" * 50)
    print(f"Job Description: {jd_path}")
    print(f"Resume: {resume_path}")
    print()

    # Score
    print(f"{Colors.BOLD}Match Score:{Colors.RESET} ", end="")
    print(f"{score_color}{score}%{Colors.RESET} - {verdict}")
    print(f"Keywords Matched: {result['matched']}/{result['total_jd']}")
    print()

    # Missing keywords
    if result["missing"]:
        print(f"{Colors.BOLD}Top Missing Keywords:{Colors.RESET}")
        print(f"{Colors.YELLOW}(Consider adding these to your resume){Colors.RESET}")
        print()
        for keyword, weight, freq in result["missing"][:15]:
            indicator = "⚡" if keyword in TECH_KEYWORDS else "•"
            print(f"  {indicator} {keyword} (appears {freq}x in JD)")
        print()

    # Matched keywords (abbreviated)
    if result["matched_keywords"]:
        print(f"{Colors.BOLD}Matched Keywords:{Colors.RESET}")
        matched_display = ", ".join(result["matched_keywords"][:30])
        if len(result["matched_keywords"]) > 30:
            matched_display += f" ... (+{len(result['matched_keywords']) - 30} more)"
        print(f"  {Colors.GREEN}{matched_display}{Colors.RESET}")
        print()

    # Recommendations
    print(f"{Colors.BOLD}Recommendations:{Colors.RESET}")
    if score < 50:
        print("  1. Add more technical keywords from the job description")
        print("  2. Mirror the exact terminology used in the JD")
        print("  3. Include specific tools and technologies mentioned")
    elif score < 70:
        print("  1. Good foundation - add a few more key terms")
        print("  2. Ensure skills section matches JD requirements")
    else:
        print("  ✓ Strong keyword match! Focus on tailoring bullet points.")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="ATS Keyword Scoring - Analyze resume against job description"
    )
    parser.add_argument(
        "path",
        help="Path to application folder or job_desc.md file",
    )
    parser.add_argument(
        "resume",
        nargs="?",
        help="Path to resume.md (optional if path is a folder)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    path = Path(args.path)

    # Determine file paths
    if path.is_dir():
        jd_path = path / "job_desc.md"
        resume_path = path / "resume.md"
    elif args.resume:
        jd_path = path
        resume_path = Path(args.resume)
    else:
        print(
            f"{Colors.RED}Error: Provide either a folder or both JD and resume paths{Colors.RESET}"
        )
        return 1

    # Check files exist
    if not jd_path.exists():
        print(f"{Colors.RED}Error: Job description not found: {jd_path}{Colors.RESET}")
        return 1

    if not resume_path.exists():
        print(f"{Colors.RED}Error: Resume not found: {resume_path}{Colors.RESET}")
        return 1

    # Read files
    jd_text = jd_path.read_text(encoding="utf-8")
    resume_text = resume_path.read_text(encoding="utf-8")

    # Extract keywords
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    # Add phrase matching
    jd_phrases = extract_phrases(jd_text)
    resume_phrases = extract_phrases(resume_text)
    for phrase in jd_phrases:
        jd_keywords[phrase] += 2  # Phrases are important
    for phrase in resume_phrases:
        resume_keywords[phrase] += 2

    # Calculate score
    result = calculate_score(jd_keywords, resume_keywords)

    # Output
    if args.json:
        import json

        print(json.dumps(result, indent=2))
    else:
        print_report(result, str(jd_path), str(resume_path))

    # Return code based on score
    return 0 if result["score"] >= 50 else 1


if __name__ == "__main__":
    sys.exit(main())
