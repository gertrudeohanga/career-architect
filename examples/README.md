# Examples

This folder contains examples to help you get started with Career Architect.

## Files

| File                         | Description                              |
| ---------------------------- | ---------------------------------------- |
| `example_job_description.md` | Sample JD to test the pipeline           |
| `sample_resume_output.md`    | What a generated resume looks like       |
| `sample_cover_letter.md`     | What a generated cover letter looks like |

## Quick Test

1. Make sure you've set up your `source_materials/identity.json`
2. Open `example_job_description.md`
3. Copy the job description section
4. Paste to your AI assistant and say:
   > "I want to apply for this job. Use the Career Architect pipeline."

## What Happens

The AI assistant will read the prompts in `.prompts/` and:

1. **Parse the JD** - Extract company, role, requirements
2. **Create application folder** - `applications/YYYY-MM-DD-company-role/`
3. **Run gap analysis** - Compare your experience to requirements
4. **Generate documents** - Resume, cover letter tailored to the role
5. **Save everything** - Ready for PDF generation

Then run:

```bash
python scripts/compile_all.py
```

## Tips

- **Better input = Better output**: The more detailed your `master_experience.md`, the better your tailored documents
- **Review before sending**: Always review AI-generated content before submitting
- **Iterate**: Ask the AI to refine specific sections if needed
