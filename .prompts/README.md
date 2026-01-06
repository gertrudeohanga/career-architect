# Prompts Index

This directory contains AI instruction prompts for the Career Architect pipeline. Use these prompts with your AI assistant (Claude, GPT-4, etc.) to generate tailored job application materials.

## First-Time Setup (Do This Once)

Before using any prompts, you must add your source materials:

```
1. Edit identity.json          → Your contact info
2. Add resumes to resumes/     → Copy-paste your existing resumes as .md files
3. Add projects to projects/   → Document your key projects
4. Run setup.md                → AI builds your master_experience.md
```

Then for each job application, just paste the job description!

## Quick Reference

| Prompt                     | When to Use                              | Output                         |
| -------------------------- | ---------------------------------------- | ------------------------------ |
| `setup.md`                 | **First!** After adding resumes/projects | `master_experience.md`         |
| `main_orchestrator.md`     | For each new job application             | Full pipeline                  |
| `analyser.md`              | Gap analysis before tailoring            | Strategic Match Report         |
| `tailor_resume.md`         | Generate targeted resume                 | `resume.md`                    |
| `application_questions.md` | Answer extra questions                   | `extra_questions.md`           |
| `interview_prep.md`        | Prepare for interviews                   | Q&A coaching                   |
| `gap_filler.md`            | Fill experience gaps                     | Updated `master_experience.md` |
| `pdf_generator.md`         | Prepare for PDF build                    | Validated Markdown             |

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAREER ARCHITECT PIPELINE                         │
└─────────────────────────────────────────────────────────────────────────┘

SETUP PHASE (One-Time):
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Add Resumes  │────▶│ Add Projects │────▶│  setup.md    │
│ (resumes/)   │     │ (projects/)  │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
                                         ┌──────────────┐
                                         │master_exp.md │
                                         │  (Generated) │
                                         └──────────────┘

APPLICATION PHASE (Per Job):
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Job Desc    │────▶│ analyser.md  │────▶│ Match Report │
│  (Paste it!) │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                           ┌──────────────────────┤
                           │                      │
                           ▼                      ▼
                    ┌──────────────┐     ┌──────────────┐
                    │gap_filler.md │     │tailor_resume │
                    │ (If needed)  │     │     .md      │
                    └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
                                         ┌──────────────┐
                                         │pdf_generator │
                                         │     .md      │
                                         └──────────────┘
                                                  │
                                                  ▼
                                         ┌──────────────┐
                                         │   resume.pdf │
                                         │cover_letter  │
                                         └──────────────┘
```

## Prompt Descriptions

### 🎯 main_orchestrator.md

**The Master Controller** - Orchestrates the entire pipeline from job description to final PDF. Use this when you want the AI to run the complete workflow automatically.

**Usage**: Provide a job description and say "Run the main orchestrator"

### 📊 setup.md

**Experience Extraction** - Analyzes your existing resumes and creates a comprehensive `master_experience.md` file. Run this once at the start, then update periodically.

**Usage**: "Analyze my resumes in source_materials/resumes/ and create master_experience.md"

### 🔍 analyser.md

**Gap Analysis** - Compares your experience against job requirements. Outputs a Strategic Match Report with scores and recommendations.

**Usage**: "Analyze the gap between my experience and this job description"

### ✍️ tailor_resume.md

**Resume Generation** - Creates a targeted resume using the Modern Builder framework. Every bullet includes metrics.

**Usage**: "Create a tailored resume for this position"

### 📝 application_questions.md

**Extra Questions** - Handles both narrative questions (using SAR framework) and logistics questions (from identity.json).

**Usage**: "Answer these application questions: [paste questions]"

### 🎤 interview_prep.md

**Interview Coaching** - Generates likely interview questions and provides model answers based on your experience.

**Usage**: "Help me prepare for the interview at [Company]"

### 🔧 gap_filler.md

**Experience Updates** - Converts informal experience descriptions into structured entries for master_experience.md.

**Usage**: "I have this experience that's not in my master file: [describe]"

### 📄 pdf_generator.md

**Build Preparation** - Validates and sanitizes Markdown for PDF generation. Checks contact info against identity.json.

**Usage**: "Prepare resume.md for PDF generation"

### 💡 manifesto_logic.md

**Philosophy Guide** - Defines the "Modern Builder" language transformations. Referenced by other prompts automatically.

### 🏗️ career_architect.md

**Core Directives** - Establishes fundamental rules like SAR framework and no-hallucination policy.

## Best Practices

1. **Start with setup.md** to build your experience lake
2. **Keep identity.json updated** with current contact info
3. **Run analyser.md first** before generating documents
4. **Review AI output** - verify all metrics and claims
5. **Use gap_filler.md** when analysis finds missing experience

## Customization

To add new prompts:

1. Create a new `.md` file in this directory
2. Follow the structure:

   ```markdown
   # Role: [Role Name]

   ## Objective

   [Clear goal]

   ## Inputs

   [What files/data are needed]

   ## Instructions

   [Step-by-step process]

   ## Output Format

   [Expected structure]
   ```

3. Update this README with the new prompt
