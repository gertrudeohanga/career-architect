# Career Architect 🏗️

An AI-powered job application pipeline that helps engineers create tailored resumes, cover letters, and application materials using a structured prompt system.

## Features

- **AI-Guided Workflow**: Structured prompts for consistent, high-quality outputs
- **Modern Builder Framework**: Emphasizes metrics-driven achievements and system leadership
- **Multi-Format Export**: Generate PDF, DOCX, and TXT from Markdown sources
- **Vertical Targeting**: Customized tone for Startups, ScaleUps, and Big Tech
- **Gap Analysis**: Identifies skill gaps and suggests strategic pivots
- **Interview Prep**: Generate predictive questions based on your application

## Quick Start

### Prerequisites

- Python 3.8+
- [Pandoc](https://pandoc.org/installing.html)
- LaTeX distribution (for PDF generation):
  - macOS: `brew install --cask mactex-no-gui`
  - Ubuntu: `sudo apt-get install texlive-full`
  - Windows: [MiKTeX](https://miktex.org/download)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd learning

# Install Python dependencies
pip install -r requirements.txt

# Verify Pandoc installation
pandoc --version
```

### Setup Your Profile

1. **Edit your identity** in `source_materials/identity.json`:

```json
{
  "full_name": "Your Name",
  "email": "your@email.com",
  "phone": "+1 234 567 8901",
  "location": "City, Country",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",
  "portfolio": "https://yoursite.com"
}
```

2. **Build your experience lake** in `source_materials/master_experience.md` using the setup prompt

3. **Add projects** to `source_materials/projects/`

## Usage

### The Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Job Description → 2. Analysis → 3. Generation → 4. Build   │
└─────────────────────────────────────────────────────────────────┘
```

#### Step 1: Start a New Application

Provide a job description to your AI assistant with the main orchestrator prompt (`.prompts/main_orchestrator.md`). The system will:

- Extract company and role information
- Create `applications/YYYY-MM-DD-company-role/`
- Save the job description as `job_desc.md`

#### Step 2: Build Documents

```bash
# Build a specific resume
python scripts/build_resume.py applications/2025-01-06-acme-senior-engineer/resume.md

# Build with specific formats
python scripts/build_resume.py resume.md --formats pdf,docx

# Build most recent application
python scripts/compile_all.py

# Build all applications
python scripts/compile_all.py --all

# Build specific application
python scripts/compile_all.py --application "2025-01-06-acme-senior-engineer"
```

### CLI Reference

```bash
# Build resume/cover letter
python scripts/build_resume.py <input.md> [options]
  --company    Company name override
  --role       Role name override
  --formats    Output formats: pdf,docx,txt (default: pdf,docx,txt)

# Compile applications
python scripts/compile_all.py [options]
  --all           Build all applications
  --application   Build specific application by folder name
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
