# Career Architect 🏗️

> **Paste a job description. Let AI do the rest.**

An open-source, AI-powered job application pipeline that helps engineers create tailored resumes, cover letters, and application materials. Just paste the job description and your AI coding assistant handles everything.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## How It Works

```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   1. PASTE JOB DESCRIPTION  →  2. AI GENERATES  →  3. BUILD PDF       │
│                                                                        │
│   You provide the JD            AI creates:         One command:       │
│   to your AI assistant          • Tailored resume   python compile.py  │
│                                 • Cover letter                         │
│                                 • Interview prep                       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Quick Start (5 Minutes)

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/career-architect.git
cd career-architect
make install
make check  # Verify dependencies
```

### 2. Configure Your Profile (One-Time)

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

### 3. Apply to a Job

**Just paste the job description to your AI assistant and say:**

> "I want to apply for this job. Use the Career Architect pipeline."

That's it! The AI will:

1. ✅ Create an application folder
2. ✅ Analyze the job requirements against your experience
3. ✅ Generate a tailored resume with metrics
4. ✅ Write a matching cover letter
5. ✅ Prepare you for interviews

### 4. Build PDFs

```bash
python scripts/compile_all.py
```

## Features

- **🤖 AI-Native Workflow** - Designed for Claude, GPT-4, Copilot, and other AI assistants
- **📊 Modern Builder Framework** - Metrics-driven achievements using SAR (Situation-Action-Result)
- **🎯 Vertical Targeting** - Auto-adapts tone for Startups vs ScaleUps vs Big Tech
- **📄 Multi-Format Export** - PDF, DOCX, and TXT from single Markdown source
- **🔍 Gap Analysis** - Identifies skill gaps and suggests how to address them
- **🎤 Interview Prep** - Generates likely questions with model answers

## Prerequisites

- **Python 3.8+**
- **AI Assistant** (Claude, GPT-4, Cursor, Windsurf, etc.)
- **[Pandoc](https://pandoc.org/installing.html)** - Document conversion
- **LaTeX** - PDF generation
  - macOS: `brew install --cask mactex-no-gui`
  - Ubuntu: `sudo apt-get install texlive-full`
  - Windows: [MiKTeX](https://miktex.org/download)

## CLI Commands

```bash
# Create new application
python scripts/career.py new --company "Acme" --role "Senior Engineer"

# Build documents
python scripts/career.py build              # Most recent application
python scripts/career.py build --all        # All applications
python scripts/career.py build --force      # Force rebuild

# List applications
python scripts/career.py list

# Check setup
python scripts/career.py status
python scripts/career.py validate
```

Or use Make:

```bash
make build                    # Build most recent
make build-all               # Build all
make new COMPANY=Acme ROLE=Engineer
```

## Project Structure

```
career-architect/
├── .prompts/                    # AI instruction prompts
│   ├── main_orchestrator.md     # Pipeline controller
│   ├── setup.md                 # Experience extraction
│   ├── analyser.md              # Gap analysis
│   ├── tailor_resume.md         # Resume generation
│   ├── application_questions.md # Extra questions
│   ├── interview_prep.md        # Interview coaching
│   ├── gap_filler.md            # Fill experience gaps
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
│   ├── build_resume.py          # Document builder
│   └── compile_all.py           # Batch compiler
├── source_materials/
│   ├── identity.json            # Contact info & logistics
│   ├── master_experience.md     # Experience lake
│   ├── projects/                # Project case studies
│   └── resumes/                 # Historical resumes
├── templates/
│   ├── style.tex                # Resume LaTeX styling
│   └── cover_letter_style.tex   # Cover letter styling
├── requirements.txt
├── Makefile
└── README.md
```

## Prompts Overview

| Prompt                     | Purpose                                                |
| -------------------------- | ------------------------------------------------------ |
| `main_orchestrator.md`     | End-to-end pipeline controller                         |
| `setup.md`                 | Extract and structure experience into master file      |
| `analyser.md`              | Gap analysis between experience and job requirements   |
| `tailor_resume.md`         | Generate targeted resume with Modern Builder framework |
| `application_questions.md` | Answer application questions with SAR framework        |
| `interview_prep.md`        | Generate interview questions and model answers         |
| `gap_filler.md`            | Fill identified experience gaps                        |
| `pdf_generator.md`         | Prepare documents for PDF generation                   |
| `manifesto_logic.md`       | Modern Builder philosophy and language                 |
| `career_architect.md`      | Core operational directives                            |

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details.

---

**Built for engineers who treat job applications as a system to be optimized.** 🎯
