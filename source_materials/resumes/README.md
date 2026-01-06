# How to Add Your Resumes

> **Do this BEFORE running the setup prompt!**

## Instructions

1. **Create a new `.md` file** for each resume you have
2. **Copy-paste the entire resume content** (plain text is fine)
3. **Name files descriptively**: `YYYY-company-role.md`

## Example Files to Create

```
source_materials/resumes/
├── 2024-current-company.md     # Your most recent resume
├── 2023-previous-job.md        # Previous role
├── 2022-startup-resume.md      # Startup application
└── general-master-resume.md    # Your longest/most complete version
```

## What to Include

Just paste the raw resume text. The AI will extract:

- Job titles and dates
- Company names
- Achievements with metrics
- Technical skills
- Education

## Example Format

Create a file like `2024-techcorp-senior-engineer.md`:

```markdown
JOHN DOE
San Francisco, CA | john@email.com | linkedin.com/in/johndoe

EXPERIENCE

Senior Software Engineer | TechCorp Inc | 2022 - Present

- Designed payment system handling 50K daily transactions
- Led team of 4 engineers, improving velocity by 35%
- Reduced API latency from 800ms to 120ms

Software Engineer | StartupXYZ | 2020 - 2022

- Built core billing system processing $2M ARR
- Implemented CI/CD pipeline reducing deploy time by 80%

EDUCATION
B.S. Computer Science | University Name | 2020

SKILLS
Python, Go, PostgreSQL, AWS, Kubernetes
```

---

**Next step**: After adding your resumes, add your projects in `source_materials/projects/`
