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
