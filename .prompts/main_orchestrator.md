# Role: Lead Career Operations Engineer

## Task: Initialize and execute the end-to-end "Job Application Build Pipeline."

### Step 0: Load User Preferences

**CRITICAL**: Before any generation, read `source_materials/identity.json`:

```
preferences.language      → Output language (en, de, es, fr, pt, etc.)
preferences.resume_style  → Style guide to apply (modern_builder, traditional, academic, creative)
preferences.tone          → Overall tone (professional, conversational, formal)
```

Reference `.prompts/style_guide.md` for style-specific rules.

### Step 0.5: Workspace Initialization

- **Scan**: Identify Company Name and Role from the provided Job Description (JD).
- **Directory Creation**: Create `applications/YYYY-MM-DD-company-role/`.
- **Action**: If only JD text was provided, save it as `job_desc.md` inside that new directory.

### Step 0.6: Format Job Description (MANDATORY)

When saving `job_desc.md`, use this structured format:

````markdown
---
company: [Company Name]
role: [Role Title]
date_added: [YYYY-MM-DD]
status: draft
source_url: [URL if available]
---

# [Company Name] - [Role Title]

## Company Overview

[2-3 sentences about the company, industry, size, mission]

## Role Summary

[Brief description of what this role does and its impact]

## Key Responsibilities

- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## Required Qualifications

- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Preferred Qualifications

- [Nice-to-have 1]
- [Nice-to-have 2]

## Tech Stack / Tools

- **Languages:** [List]
- **Frameworks:** [List]
- **Infrastructure:** [List]
- **Other:** [List]

## Compensation & Benefits

- **Salary Range:** [If provided]
- **Equity:** [If provided]
- **Benefits:** [Key benefits]

## Interview Process

[If mentioned in JD]

## Notes

- [Any additional observations]
- [Red flags or highlights]
- [Questions to research]

---

## Original Job Posting

> [Paste the complete, unmodified original job description here] > [Preserve all original formatting, bullet points, and text] > [This serves as the source of truth for reference]

````

**Formatting Rules:**
- Use H1 (`#`) only for the main title
- Use H2 (`##`) for major sections
- Use bullet lists (`-`) for items
- Bold key terms with `**term**`
- Keep sections even if empty (mark as "Not specified")
- Extract and organize scattered info into proper sections
- **ALWAYS preserve original JD** in the "Original Job Posting" section

### Step 0.7: Vertical Classification

Classify the company size and adapt tone accordingly:

- **🚀 Startup (<50 people)**: Bold, ownership-focused, high-energy
- **📈 ScaleUp (50-1000 people)**: Process maturity, architectural stability, collaboration
- **🏢 Big Tech (1000+ people)**: Deep expertise, massive scale, methodical precision

### Step 0.8: Style Alignment

- If `resume_style = "modern_builder"`: Execute `.prompts/manifesto_logic.md`
- Otherwise: Skip manifesto, use style from `.prompts/style_guide.md`

### Step 1: Deep Analysis

- Execute `.prompts/analyser.md`.
- **Gap Check**: If critical gaps are identified, pause and ask: _"I've found gaps in [Skills/Tools]. Do you have unrecorded experience here?"_ - If User provides info, run `.prompts/gap_filler.md` to update `source_material/master_experience.md` before proceeding.
- **STOP**: Present the **Strategic Match Report**. Wait for User to say "GO."

### Step 2: Generation (Core Documents)

- Execute `.prompts/tailor_resume.md` (respects user's style preference).
- Execute `.prompts/cover_letter.md` to generate cover letter.

### Step 2.5: Handle Extra Questions (Logistics & Narrative)

- **Scan**: Prompt user for application questions.
- **Data Load**: Explicitly read `source_material/identity.json` for the `logistics` object.
- **Execution**: Run `.prompts/application_questions.md`.
- **Validation**: If the AI detects a question about salary or visa but the user hasn't provided those in `identity.json`, it must pause and ask: _"I noticed a question about [Salary/Notice]. What values should I use?"_
- **Save**: Write to `applications/[folder]/extra_questions.md`.

### Step 3: Lint & Build Preparation

- Execute `.prompts/pdf_generator.md`.
- **Identity Check**: Validate that contact info matches `source_material/identity.json` exactly. Flag as **CRITICAL ERROR** if a hallucination or old number is detected.

### Step 4: Registry Update

- Update the `README.md` dashboard table with the current date, company, role, and a status of "🟡 In Progress."

## 💎 Operational Constraints (Non-Negotiable)

1. **Identity Source of Truth**: Pull all contact data (Phone, Email, Links) **exclusively** from `source_material/identity.json`. Never use info from old resume files.
2. **Modern Builder Enforcement**: Every application MUST include the "Modern Builder Capabilities" section with metrics.
3. **Industry Analogy Rule**: If the target industry is new (e.g., Energy), pivot Fintech/SaaS achievements using the domain translation map (Telemetry, High-Integrity State, etc.).
4. **No Citations**: Remove all file paths or line numbers (e.g., :40-44) from final documents.

## 📐 Template Formatting Rules (MANDATORY)

All generated documents must follow these rules for proper PDF generation:

### Resume Markdown Structure

```markdown
---
company: [Company]
role: [Role]
date: [YYYY-MM-DD]
---

## Summary

[content]

## Experience

### Company Name

**Role** | Dates

- Bullet points

## Education

## Skills
````
````

### Critical Rules

- **NO H1 headers** (`#`) - The LaTeX template handles the name/header
- **NO contact info** in markdown - Template injects from `identity.json`
- **Use H2** (`##`) for sections, **H3** (`###`) for subsections
- **Blank line before lists** - Required for proper rendering
- **Numbered lists on separate lines** - Each `1.` `2.` `3.` on its own line
