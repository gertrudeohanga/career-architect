# Career Architect 🏗️

> **Paste a job description. Let AI do the rest.**

An open-source, AI-powered job application pipeline that helps engineers create tailored resumes, cover letters, and application materials. Just paste the job description and your AI coding assistant handles everything.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## How It Works

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  1. PASTE JOB DESC  │───▶│   2. AI GENERATES   │───▶│    3. BUILD PDF     │
├─────────────────────┤    ├─────────────────────┤    ├─────────────────────┤
│ You provide the JD  │    │ • Tailored resume   │    │ One command:        │
│ to your AI assistant│    │ • Cover letter      │    │ make build          │
│                     │    │ • Interview prep    │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

## Quick Start (5 Minutes)

### 1. Clone & Setup

```bash
# HTTPS
git clone https://github.com/henryohanga/career-architect.git

# Or SSH (if you have keys configured)
git clone git@github.com:henryohanga/career-architect.git

cd career-architect
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Or use Make (auto-installs)
make install
```

### 3. Verify Setup

```bash
make check  # Verify all dependencies are installed
```

**Required external tools:**

- **Pandoc** - Document conversion ([install](https://pandoc.org/installing.html))
- **LaTeX** - PDF generation
  - macOS: `brew install --cask mactex-no-gui`
  - Ubuntu: `sudo apt-get install texlive-full`
  - Windows: [MiKTeX](https://miktex.org/download)

### 4. Configure Your Profile (One-Time)

**Step A: Edit your identity**

Update `source_materials/identity.json` with your contact info:

```json
{
  "full_name": "Your Name",
  "email": "your@email.com",
  "phone": "+1 234 567 8901",
  "location": "City, Country",
  "linkedin": "https://linkedin.com/in/you",
  "github": "https://github.com/you"
}
```

**Step B: Add your historical resumes**

Copy-paste your existing resumes into `source_materials/resumes/`:

```
source_materials/resumes/
├── 2024-google-resume.md      # Paste your Google application resume
├── 2023-startup-resume.md     # Paste your startup resume
└── general-resume.md          # Your most complete/recent resume
```

**Step C: Add your projects**

Document key projects in `source_materials/projects/`:

```
source_materials/projects/
├── saas-platform.md           # Your SaaS project details
├── open-source-contrib.md     # Open source contributions
└── side-project.md            # Notable side projects
```

**Step D: Build your experience lake**

Now tell your AI assistant:

> "Read `.prompts/setup.md` and analyze my resumes in `source_materials/resumes/` and projects in `source_materials/projects/` to build my master experience file."

The AI will extract and structure all your achievements into `source_materials/master_experience.md`.

### 5. Apply to a Job

**Just paste the job description to your AI assistant and say:**

> "I want to apply for this job. Use the Career Architect pipeline."

That's it! The AI will:

1. ✅ Create an application folder
2. ✅ Analyze the job requirements against your experience
3. ✅ Generate a tailored resume with metrics
4. ✅ Write a matching cover letter
5. ✅ Prepare you for interviews

### 6. Build PDFs

```bash
python scripts/compile_all.py
```

## Features

- **🤖 AI-Native Workflow** - Designed for Claude, GPT-4, Copilot, and other AI assistants
- **📊 Modern Builder Framework** - Metrics-driven achievements using SAR (Situation-Action-Result)
- **🎯 Vertical Targeting** - Auto-adapts tone for Startups vs ScaleUps vs Big Tech
- **📄 Multi-Format Export** - PDF, DOCX, TXT, and JSON Resume from single Markdown source
- **🔍 Gap Analysis** - Identifies skill gaps and suggests how to address them
- **🎤 Interview Prep** - Generates likely questions with mock interview coaching
- **📈 ATS Scoring** - Keyword analysis to optimize for Applicant Tracking Systems
- **🌍 Multi-Language** - Configurable for any language and resume style
- **🎨 Template Gallery** - 4 professional LaTeX templates (default, minimal, creative, executive)
- **🌐 Web Dashboard** - Visual management with Streamlit UI
- **🔗 Job Board Scraper** - Import jobs from LinkedIn, Indeed, Greenhouse, Lever
- **📦 Batch Processing** - Import multiple job descriptions at once
- **📝 Version Tracking** - Save, compare, and restore resume versions

## CLI Commands

```bash
# Create new application
python scripts/career.py new --company "Acme" --role "Senior Engineer"

# Build documents
python scripts/career.py build              # Most recent application
python scripts/career.py build --all        # All applications
python scripts/career.py build --force      # Force rebuild

# Build with specific template
python scripts/compile_all.py --template executive
python scripts/compile_all.py --template minimal --force

# List applications
python scripts/career.py list

# Check setup
python scripts/career.py status
python scripts/career.py validate

# ATS keyword scoring
python scripts/career.py ats                    # Score latest application

# Export to ATS-friendly formats
python scripts/career.py export                 # Export TXT + JSON Resume
python scripts/career.py export txt             # Plain text only
python scripts/career.py export json            # JSON Resume format

# Version tracking
python scripts/career.py version save -m "v1"   # Save version
python scripts/career.py version list           # List versions
python scripts/career.py version diff           # Compare versions

# Analytics
python scripts/career.py stats                  # Application statistics

# Batch processing
python scripts/career.py batch ./jd_folder      # Import multiple JDs
python scripts/career.py batch ./jd_folder -n   # Preview (dry run)

# Scrape from URL
python scripts/career.py scrape <url>           # Preview job details
python scripts/career.py scrape <url> --create  # Create application
```

## Web Dashboard

Launch the visual dashboard:

```bash
streamlit run app.py
```

Features:

- 📊 Dashboard overview of all applications
- 📝 Application management with status updates
- ➕ Create new applications with form
- 📈 Analytics and statistics
- ⚙️ Profile settings

Or use Make:

```bash
make build                    # Build most recent
make build-all               # Build all
make new COMPANY=Acme ROLE=Engineer
make ats                     # ATS keyword score
make test                    # Run tests
```

## Project Structure

```
career-architect/
├── .prompts/                    # AI instruction prompts
│   ├── main_orchestrator.md     # Pipeline controller
│   ├── setup.md                 # Experience extraction
│   ├── analyser.md              # Gap analysis + strategic match report
│   ├── tailor_resume.md         # Resume generation
│   ├── cover_letter.md          # Cover letter generation
│   ├── application_questions.md # Extra questions
│   ├── interview_prep.md        # Interview coaching + mock interviews
│   ├── gap_filler.md            # Fill experience gaps
│   ├── linkedin_optimizer.md    # LinkedIn profile optimization
│   ├── follow_up.md             # Professional follow-up emails
│   ├── style_guide.md           # Resume styles & language config
│   ├── pdf_generator.md         # Build preparation
│   ├── manifesto_logic.md       # Modern Builder philosophy
│   └── career_architect.md      # Core directives
├── applications/                # Generated job applications
│   └── YYYY-MM-DD-company-role/
│       ├── job_desc.md
│       ├── resume.md
│       ├── cover_letter.md
│       ├── extra_questions.md
│       └── *.pdf, *.docx
├── scripts/
│   ├── career.py                # Main CLI tool
│   ├── ats_score.py             # ATS keyword analyzer
│   ├── export_resume.py         # ATS format exporter (TXT, JSON Resume)
│   ├── version_tracker.py       # Resume version tracking
│   ├── batch_process.py         # Batch JD processing
│   ├── job_scraper.py           # Job board URL scraper
│   ├── build_resume.py          # Document builder
│   └── compile_all.py           # Batch compiler
├── tests/                       # Unit tests (40+ tests)
│   ├── test_career.py
│   ├── test_export.py
│   ├── test_version_tracker.py
│   └── test_batch.py
├── app.py                       # Streamlit web dashboard
├── source_materials/
│   ├── identity.json            # Contact info & logistics
│   ├── master_experience.md     # Experience lake
│   ├── projects/                # Project case studies
│   └── resumes/                 # Historical resumes
├── templates/
│   ├── style.tex                # Default resume style
│   ├── minimal.tex              # Clean, conservative style
│   ├── creative.tex             # Bold, colorful style
│   ├── executive.tex            # Sophisticated style
│   └── cover_letter_style.tex   # Cover letter styling
├── requirements.txt
├── Makefile
└── README.md
```

## Prompts Overview

| Prompt                     | Purpose                                                 |
| -------------------------- | ------------------------------------------------------- |
| `main_orchestrator.md`     | End-to-end pipeline controller                          |
| `setup.md`                 | Extract and structure experience into master file       |
| `analyser.md`              | Gap analysis + strategic match report                   |
| `tailor_resume.md`         | Generate targeted resume (style-configurable)           |
| `cover_letter.md`          | Generate compelling cover letters                       |
| `application_questions.md` | Answer application questions with SAR framework         |
| `interview_prep.md`        | Generate questions + mock interview coaching            |
| `gap_filler.md`            | Fill identified experience gaps                         |
| `linkedin_optimizer.md`    | Optimize LinkedIn profile for target roles              |
| `follow_up.md`             | Professional follow-up emails and thank you notes       |
| `style_guide.md`           | Resume styles (modern, traditional, academic, creative) |
| `pdf_generator.md`         | Prepare documents for PDF generation                    |
| `manifesto_logic.md`       | Modern Builder philosophy and language                  |
| `career_architect.md`      | Core operational directives                             |

## The Modern Builder Framework

This system uses the "Modern Builder" framework to present engineering experience:

### Five Core Capabilities

1. **Precise Problem Decomposition** - Breaking complex problems into solvable units
2. **Systems Thinking** - Understanding interconnections and dependencies
3. **AI Steering** - Effectively directing AI tools for development
4. **Technical Taste** - Making sound architectural decisions
5. **Ownership of Outcomes** - End-to-end responsibility for results

### Language Transformations

| Generic            | Modern Builder                            |
| ------------------ | ----------------------------------------- |
| Implemented X      | Locked architectural intent for X         |
| Increased velocity | Improved decision throughput              |
| Team lead          | System leadership & mentoring             |
| Built feature      | Constrained entropy, delivered durability |

## Vertical Targeting

The system adapts tone based on company type:

| Type                     | Focus                               | Tone                |
| ------------------------ | ----------------------------------- | ------------------- |
| **🚀 Startup** (<50)     | Force Multiplier, Zero-to-One wins  | Bold, High-energy   |
| **📈 ScaleUp** (50-1000) | Scaling the Chaos, Process maturity | Collaborative       |
| **🏢 Big Tech** (1000+)  | Deep Expertise at Scale             | Methodical, Precise |

## Customization

### Adding Custom Templates

Create new `.tex` files in `templates/` for different styling:

```tex
% templates/custom_style.tex
\usepackage{...}
% Your custom LaTeX configuration
```

### Extending the Pipeline

Add new prompts to `.prompts/` following the existing pattern:

```markdown
# Role: [Your Role Name]

## Objective

[Clear objective statement]

## Instructions

1. [Step 1]
2. [Step 2]

## Output Format

[Expected output structure]
```

## Configuration

### Resume Styles & Templates

Set your preferences in `source_materials/identity.json`:

```json
{
  "full_name": "Your Name",
  "email": "your@email.com",
  "preferences": {
    "language": "en",
    "resume_style": "modern_builder",
    "tone": "professional",
    "template": "executive"
  }
}
```

#### Content Styles (AI generation)

| Style            | Description                                      |
| ---------------- | ------------------------------------------------ |
| `modern_builder` | Metrics-driven, high-agency verbs, SAR framework |
| `traditional`    | Conservative, chronological, formal language     |
| `academic`       | Research-focused, publications, methodologies    |
| `creative`       | Personality-forward, storytelling approach       |

#### Visual Templates (PDF output)

| Template    | File            | Best For                                       |
| ----------- | --------------- | ---------------------------------------------- |
| `default`   | `style.tex`     | Modern professional (slate blue)               |
| `minimal`   | `minimal.tex`   | Conservative industries, traditional companies |
| `creative`  | `creative.tex`  | Startups, design roles, bold colors            |
| `executive` | `executive.tex` | Senior roles, management, navy/gold            |

**Override template via CLI:**

```bash
python scripts/compile_all.py --template executive
python scripts/build_resume.py resume.md --template minimal
```

### ATS Keyword Scoring

Analyze how well your resume matches the job description:

```bash
# Score most recent application
python scripts/career.py ats

# Score specific application
python scripts/ats_score.py applications/2025-01-09-company-role/

# Get JSON output
python scripts/ats_score.py applications/folder/ --json
```

The tool identifies:

- ✅ Matched keywords (what you have)
- ⚠️ Missing keywords (what to add)
- 📊 Match score (0-100%)
- 💡 Recommendations

## Development

### Running Tests

```bash
make test                    # Run all tests
python -m pytest tests/ -v   # Verbose output
```

### Linting

```bash
make lint                    # Check Python syntax
flake8 scripts/ --max-line-length=100
```

### CI/CD

The project uses GitHub Actions for:

- Python linting (flake8)
- Unit tests (pytest)
- Project structure validation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

1. Fork the repository
2. Create a feature branch
3. Run tests (`make test`)
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 📋 Applications Dashboard

### Current Applications (Status: In Progress)

| Date | Company | Position | Status | Match Score | Application Type |
|------|---------|----------|---------|-------------|------------------|
| 2026-02-21 | Kaziweza Limited | Branch Team Leader - Eldoret | 🔄 In Progress | 50/100 | Career Architect |
| 2026-02-21 | SimplePay Capital Limited | Business Development Officer | 🔄 In Progress | 40/100 | Career Architect |
| 2026-02-20 | SGS Brightsight | Business Development Executive | 🔄 In Progress | 70/100 | Career Architect |
| 2026-02-19 | InEvent | Business Development Representative | 🔄 In Progress | 80/100 | Career Architect |
| 2026-02-19 | Decathlon | Business Developer Wholesale | 🔄 In Progress | 70/100 | Career Architect |
| 2026-02-19 | Boresha Credit Services | Assistant Head of Operations | 🔄 In Progress | 50/100 | Career Architect |
| 2026-02-19 | Primano Global Limited | Business Development Officer | 🔄 In Progress | 70/100 | Career Architect |
| 2026-02-19 | TLC Worldwide | Business Development Manager | 🔄 In Progress | 75/100 | Career Architect |
| 2026-02-19 | Kaziweza Limited | Regional Manager - Fashion Retail | 🔄 In Progress | 60/100 | Career Architect |
| 2026-02-19 | Autocom Japan Kenya | Sales Representative | 🔄 In Progress | 80/100 | Career Architect |
| 2026-02-19 | Lubricants Company | Business Development Manager | 🔄 In Progress | 70/100 | Career Architect |
| 2026-02-15 | Moja EV Kenya LTD | Business Development Executive | 🔄 In Progress | 80/100 | Career Architect |
| 2026-02-02 | Sanara Program | Gender, Inclusion and Data Quality Audit | 🔄 In Progress | 80/100 | Career Architect |
| 2026-01-26 | Zeno | Head of Customer Success | 🔄 In Progress | TBD | Career Architect |
| 2026-01-26 | Oasis Outsourcing | Home Care Recruiter | 🔄 In Progress | TBD | Career Architect |
| 2026-01-26 | The Action Foundation | People & Culture Associate | 🔄 In Progress | 70/100 | Career Architect |
| 2026-01-26 | [Company] | SDR/BDR Sales Development | 🔄 In Progress | 85/100 | Career Architect |
| 2026-01-26 | Enduring Technologies | iPOS Field Sales Agent | 🔄 In Progress | 90/100 | Career Architect |
| 2026-01-26 | Finik Enterprises | Electric Bikes Salesperson | 🔄 In Progress | 85/100 | Career Architect |
| 2026-01-24 | EBRD | Assistant Banking | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | Jobgether | Business Capture Manager | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | Justmarkets | Partner Relationship Manager | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | LED Power Technologies | Business Development Officer | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | Ratehawk | Business Development Manager | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | Roamtech | Business Development Officer | 🔄 In Progress | TBD | Career Architect |
| 2026-01-24 | Snibe | Business Development Manager | 🔄 In Progress | TBD | Career Architect |

### Application Materials Generated

Each application includes:
- ✅ **Job Description Analysis** - Complete role requirements breakdown
- ✅ **Strategic Match Report** - Alignment analysis with match scores
- ✅ **Tailored Resume** - Role-specific highlighting and optimization
- ✅ **Cover Letter** - Professional application correspondence
- ✅ **Interview Preparation** - Comprehensive interview guide
- ✅ **Email Templates** - Application submission formats (where applicable)

### Rejected Applications

| Date | Company | Position | Rejection Date | Reason |
|------|---------|----------|----------------|--------|
| 2026-02-06 | Mastercard | Manager, Loyalty Specialist Sales | 2026-02-21 | Moving forward with other candidates |

### Interview Stage

| Date | Company | Position | Status | Next Step |
|------|---------|----------|--------|-----------|
| 2026-02-16 | Kenyan Alliance Insurance | Business Development Manager - Kericho | 📞 Interview Scheduled | Virtual interview next week |

### Application Status Legend
- 🔄 **In Progress** - Materials generated, ready for submission
- ✅ **Submitted** - Application sent to employer
- 📞 **Interview Scheduled** - Interview confirmed
- ⏳ **Under Review** - Application being reviewed
- 🎉 **Offer Received** - Job offer received
- ❌ **Rejected** - Application not successful

### Quick Actions
- **Apply Now**: Check individual application folders for submission instructions
- **Update Status**: Edit this README to track application progress
- **Build PDFs**: Run `python scripts/compile_all.py` to generate PDF versions

---

**Built for engineers who treat job applications as a system to be optimized.** 🎯
