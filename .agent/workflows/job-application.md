---
description: Workflow for processing job applications with git sync
---

# Job Application Workflow

Before starting a new job application, ALWAYS complete the following steps for the previous application:

## After Completing Each Application

// turbo-all

1. Stage all changes for the completed application:
```bash
git add applications/<application-folder>/
```

2. Commit the changes with a descriptive message:
```bash
git commit -m "Add application materials for <Company> - <Role>"
```

3. Push/sync to GitHub:
```bash
git push
```

4. Verify the push was successful before proceeding to the next application.

## Application Processing Order

For each job in the list:
1. Create application folder
2. Fetch job description
3. Create strategic match report
4. If match score < 5/10, ask user if they want to skip
5. If skipping, delete the folder and move to next
6. If proceeding, create all materials (resume, cover letter, interview prep, application email)
7. Generate PDFs using compile_all.py
8. **COMMIT AND PUSH** (see above)
9. Ask user for any extra questions from application portal
10. Move to next application

## Skipped Applications

When skipping an application where a folder was already created:
1. Delete the folder: `rm -rf applications/<folder>`
2. Update task.md to mark as skipped
3. No need to commit skipped applications (folder is deleted)
