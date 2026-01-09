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

### Core Pipeline

| Prompt                     | When to Use                              | Output                 |
| -------------------------- | ---------------------------------------- | ---------------------- |
| `setup.md`                 | **First!** After adding resumes/projects | `master_experience.md` |
| `main_orchestrator.md`     | For each new job application             | Full pipeline          |
| `analyser.md`              | Gap analysis before tailoring            | Strategic Match Report |
| `tailor_resume.md`         | Generate targeted resume                 | `resume.md`            |
| `cover_letter.md`          | Generate cover letter                    | `cover_letter.md`      |
| `application_questions.md` | Answer extra questions                   | `extra_questions.md`   |
| `pdf_generator.md`         | Prepare for PDF build                    | Validated Markdown     |

### Supporting Prompts

| Prompt                  | When to Use                        | Output                         |
| ----------------------- | ---------------------------------- | ------------------------------ |
| `style_guide.md`        | Reference for resume styles        | Style configuration            |
| `interview_prep.md`     | Prepare for interviews             | Q&A coaching                   |
| `mock_interview.md`     | Practice interview responses       | Feedback & coaching            |
| `salary_negotiation.md` | Negotiate offers                   | Negotiation playbook           |
| `linkedin_optimizer.md` | Optimize LinkedIn profile          | Profile content                |
| `follow_up.md`          | Post-application communications    | Email templates                |
| `gap_filler.md`         | Fill experience gaps               | Updated `master_experience.md` |
| `manifesto_logic.md`    | Modern Builder language (optional) | Language patterns              |

### Configuration

Set your preferences in `source_materials/identity.json`:

```json
"preferences": {
  "language": "en",              // en, de, es, fr, pt, etc.
  "resume_style": "traditional", // modern_builder, traditional, academic, creative
  "tone": "professional"         // professional, conversational, formal
}
```

## Workflow Diagram

### Setup Phase (One-Time)

```
+--------------+     +--------------+     +--------------+
|   Resumes    | --> |   Projects   | --> |  setup.md    |
|  resumes/    |     |  projects/   |     |              |
+--------------+     +--------------+     +------+-------+
                                                 |
                                                 v
                                         +---------------+
                                         |   master_     |
                                         | experience.md |
                                         +---------------+
```

### Application Phase (Per Job)

```
+--------------+     +--------------+     +--------------+
|   Job Desc   | --> | analyser.md  | --> | Match Report |
|  (Paste it!) |     |              |     |   (Review)   |
+--------------+     +--------------+     +------+-------+
                                                 |
                     +---------------------------+---------------------------+
                     |                           |                           |
                     v                           v                           v
              +--------------+           +--------------+           +--------------+
              | gap_filler   |           | tailor_resume|           | cover_letter |
              | (if needed)  |           |     .md      |           |     .md      |
              +--------------+           +------+-------+           +------+-------+
                                                |                          |
                                                +------------+-------------+
                                                             |
                                                             v
                                                     +--------------+
                                                     | pdf_generator|
                                                     |     .md      |
                                                     +------+-------+
                                                            |
                                                            v
                                                     +--------------+
                                                     |    OUTPUT    |
                                                     |  resume.pdf  |
                                                     |  cover.pdf   |
                                                     +--------------+
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

**Resume Generation** - Creates a targeted resume respecting your style preferences. Every bullet includes metrics. Saves to `applications/[folder]/resume.md`.

**Usage**: "Create a tailored resume for this position"

### 💌 cover_letter.md

**Cover Letter Generation** - Creates a compelling cover letter that complements (not duplicates) your resume. Saves to `applications/[folder]/cover_letter.md`.

**Usage**: "Write a cover letter for this application"

### 📝 application_questions.md

**Extra Questions** - Handles both narrative questions (using SAR framework) and logistics questions (from identity.json).

**Usage**: "Answer these application questions: [paste questions]"

### 🎤 interview_prep.md

**Interview Coaching** - Generates technical, behavioral, and role-specific questions with model answers. Includes mock interview mode. Saves to `applications/[folder]/interview_prep.md`.

**Usage**: "Help me prepare for the interview at [Company]"

### 🔧 gap_filler.md

**Experience Updates** - Converts informal experience descriptions into structured entries. Asks clarifying questions to extract metrics, then updates `source_materials/master_experience.md`.

**Usage**: "I have this experience that's not in my master file: [describe]"

### 📄 pdf_generator.md

**Build Preparation** - Validates and sanitizes Markdown for PDF generation. Checks contact info against identity.json.

**Usage**: "Prepare resume.md for PDF generation"

### 🔗 linkedin_optimizer.md

**LinkedIn Optimization** - Generates optimized headline, about section, and experience bullets for LinkedIn profile.

**Usage**: "Optimize my LinkedIn profile for [target role]"

### 📧 follow_up.md

**Professional Communications** - Generates follow-up emails, thank you notes, rejection responses, and networking outreach.

**Usage**: "Write a thank you email after my interview with [Company]"

### 🎨 style_guide.md

**Style Configuration** - Defines resume styles (modern_builder, traditional, academic, creative) and language localization.

**Usage**: Referenced by other prompts based on `identity.json -> preferences.resume_style`

### 💡 manifesto_logic.md

**Philosophy Guide** - Defines the "Modern Builder" language transformations. Referenced when `resume_style = "modern_builder"`.

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
