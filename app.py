#!/usr/bin/env python3
"""Career Architect - Streamlit Web Dashboard.

A visual interface for managing job applications.

Run with: streamlit run app.py
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

# Paths
ROOT = Path(__file__).resolve().parent
APPLICATIONS_DIR = ROOT / "applications"
SOURCE_DIR = ROOT / "source_materials"
IDENTITY_JSON = SOURCE_DIR / "identity.json"
MASTER_EXP = SOURCE_DIR / "master_experience.md"

# Page config
st.set_page_config(
    page_title="Career Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_identity() -> dict:
    """Load identity.json."""
    if IDENTITY_JSON.exists():
        return json.loads(IDENTITY_JSON.read_text())
    return {}


def get_applications() -> list:
    """Get all application folders with metadata."""
    if not APPLICATIONS_DIR.exists():
        return []

    apps = []
    for d in sorted(APPLICATIONS_DIR.iterdir(), reverse=True):
        if not d.is_dir() or d.name.startswith("."):
            continue

        app = {
            "path": d,
            "name": d.name,
            "company": "",
            "role": "",
            "status": "draft",
            "date": "",
            "has_resume": (d / "resume.md").exists(),
            "has_cover": (d / "cover_letter.md").exists(),
            "has_pdf": any(d.glob("*.pdf")),
        }

        # Parse job_desc.md for metadata
        job_desc = d / "job_desc.md"
        if job_desc.exists():
            content = job_desc.read_text()
            for line in content.split("\n"):
                if line.startswith("company:"):
                    app["company"] = line.split(":", 1)[1].strip()
                elif line.startswith("role:"):
                    app["role"] = line.split(":", 1)[1].strip()
                elif line.startswith("status:"):
                    app["status"] = line.split(":", 1)[1].strip()
                elif line.startswith("date_added:"):
                    app["date"] = line.split(":", 1)[1].strip()

        # Extract date from folder name if not in frontmatter
        if not app["date"] and len(d.name) >= 10:
            app["date"] = d.name[:10]

        apps.append(app)

    return apps


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("🏗️ Career Architect")
        st.markdown("---")

        # Navigation
        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "📝 Applications",
                "➕ New Application",
                "📈 Analytics",
                "⚙️ Settings",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Quick stats
        apps = get_applications()
        st.metric("Total Applications", len(apps))

        by_status = {}
        for app in apps:
            status = app["status"]
            by_status[status] = by_status.get(status, 0) + 1

        if by_status:
            cols = st.columns(2)
            for i, (status, count) in enumerate(by_status.items()):
                cols[i % 2].metric(status.title(), count)

        return page


def render_dashboard():
    """Render the main dashboard view."""
    st.header("📊 Dashboard")

    apps = get_applications()

    if not apps:
        st.info("No applications yet. Create your first one!")
        return

    # Recent applications
    st.subheader("Recent Applications")

    for app in apps[:5]:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

            with col1:
                st.markdown(f"**{app['company']}** - {app['role']}")

            with col2:
                status_colors = {
                    "draft": "🟡",
                    "applied": "🟢",
                    "interview": "🔵",
                    "rejected": "🔴",
                    "offer": "⭐",
                }
                emoji = status_colors.get(app["status"], "⚪")
                st.markdown(f"{emoji} {app['status'].title()}")

            with col3:
                docs = []
                if app["has_resume"]:
                    docs.append("📄")
                if app["has_cover"]:
                    docs.append("✉️")
                if app["has_pdf"]:
                    docs.append("📑")
                st.markdown(" ".join(docs) if docs else "—")

            with col4:
                st.markdown(f"`{app['date']}`")

            st.markdown("---")


def render_applications():
    """Render the applications list view."""
    st.header("📝 Applications")

    apps = get_applications()

    if not apps:
        st.info("No applications found.")
        return

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "draft", "applied", "interview", "rejected", "offer"],
        )
    with col2:
        search = st.text_input("Search", placeholder="Company or role...")

    # Filter applications
    filtered = apps
    if status_filter != "All":
        filtered = [a for a in filtered if a["status"] == status_filter]
    if search:
        search_lower = search.lower()
        filtered = [
            a
            for a in filtered
            if search_lower in a["company"].lower() or search_lower in a["role"].lower()
        ]

    st.markdown(f"Showing {len(filtered)} of {len(apps)} applications")
    st.markdown("---")

    # Application cards
    for app in filtered:
        with st.expander(f"**{app['company']}** - {app['role']} ({app['status']})"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Date:** {app['date']}")
                st.markdown(f"**Status:** {app['status']}")

                # Status update
                new_status = st.selectbox(
                    "Update status",
                    ["draft", "applied", "interview", "rejected", "offer"],
                    index=["draft", "applied", "interview", "rejected", "offer"].index(
                        app["status"]
                    ),
                    key=f"status_{app['name']}",
                )

                if new_status != app["status"]:
                    if st.button("Save", key=f"save_{app['name']}"):
                        update_status(app["path"], new_status)
                        st.rerun()

            with col2:
                st.markdown("**Documents:**")
                st.markdown(f"- Resume: {'✅' if app['has_resume'] else '❌'}")
                st.markdown(f"- Cover Letter: {'✅' if app['has_cover'] else '❌'}")
                st.markdown(f"- PDF: {'✅' if app['has_pdf'] else '❌'}")

            # View/Edit buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📂 Open Folder", key=f"open_{app['name']}"):
                    subprocess.run(["open", str(app["path"])])
            with col2:
                if app["has_resume"]:
                    resume_content = (app["path"] / "resume.md").read_text()
                    st.download_button(
                        "📄 Download Resume",
                        resume_content,
                        file_name="resume.md",
                        key=f"dl_{app['name']}",
                    )


def update_status(app_path: Path, new_status: str):
    """Update the status in job_desc.md."""
    job_desc = app_path / "job_desc.md"
    if not job_desc.exists():
        return

    content = job_desc.read_text()
    lines = content.split("\n")
    updated = []

    for line in lines:
        if line.startswith("status:"):
            updated.append(f"status: {new_status}")
        else:
            updated.append(line)

    job_desc.write_text("\n".join(updated))


def render_new_application():
    """Render the new application form."""
    st.header("➕ New Application")

    with st.form("new_application"):
        company = st.text_input("Company Name*")
        role = st.text_input("Role/Position*")

        st.markdown("### Job Description")
        job_desc = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Copy and paste the full job description...",
        )

        submitted = st.form_submit_button("Create Application")

        if submitted:
            if not company or not role:
                st.error("Company and role are required!")
            else:
                result = create_application(company, role, job_desc)
                if result:
                    st.success(f"Created: {result}")
                    st.balloons()
                else:
                    st.error("Failed to create application")


def create_application(company: str, role: str, job_desc: str) -> str:
    """Create a new application folder."""
    import re

    date = datetime.now().strftime("%Y-%m-%d")

    # Slugify
    def slugify(text):
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text.strip("-")

    slug = f"{date}-{slugify(company)}-{slugify(role)}"
    app_dir = APPLICATIONS_DIR / slug

    if app_dir.exists():
        return None

    app_dir.mkdir(parents=True, exist_ok=True)

    # Create job_desc.md
    frontmatter = f"""---
company: {company}
role: {role}
date_added: {date}
status: draft
---

# {company} - {role}

## Job Description

{job_desc if job_desc else "Paste the job description here."}

## Key Requirements

-

## Notes

-
"""
    (app_dir / "job_desc.md").write_text(frontmatter)
    return slug


def render_analytics():
    """Render the analytics view."""
    st.header("📈 Analytics")

    apps = get_applications()

    if not apps:
        st.info("No data to display yet.")
        return

    # Status breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("By Status")
        by_status = {}
        for app in apps:
            status = app["status"]
            by_status[status] = by_status.get(status, 0) + 1

        for status, count in sorted(by_status.items()):
            st.progress(count / len(apps), text=f"{status}: {count}")

    with col2:
        st.subheader("Document Completion")
        has_resume = sum(1 for a in apps if a["has_resume"])
        has_cover = sum(1 for a in apps if a["has_cover"])
        has_pdf = sum(1 for a in apps if a["has_pdf"])

        st.metric("With Resume", f"{has_resume}/{len(apps)}")
        st.metric("With Cover Letter", f"{has_cover}/{len(apps)}")
        st.metric("With PDF", f"{has_pdf}/{len(apps)}")

    # Timeline
    st.subheader("Applications Over Time")
    by_month = {}
    for app in apps:
        if app["date"] and len(app["date"]) >= 7:
            month = app["date"][:7]
            by_month[month] = by_month.get(month, 0) + 1

    if by_month:
        months = sorted(by_month.keys())
        counts = [by_month[m] for m in months]
        st.bar_chart(dict(zip(months, counts)))


def render_settings():
    """Render the settings view."""
    st.header("⚙️ Settings")

    # Identity
    st.subheader("Profile")
    identity = load_identity()

    with st.form("identity_form"):
        name = st.text_input("Full Name", value=identity.get("full_name", ""))
        email = st.text_input("Email", value=identity.get("email", ""))
        phone = st.text_input("Phone", value=identity.get("phone", ""))
        location = st.text_input("Location", value=identity.get("location", ""))
        linkedin = st.text_input("LinkedIn", value=identity.get("linkedin", ""))
        github = st.text_input("GitHub", value=identity.get("github", ""))

        if st.form_submit_button("Save Profile"):
            identity.update(
                {
                    "full_name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                }
            )
            IDENTITY_JSON.write_text(json.dumps(identity, indent=2, ensure_ascii=False))
            st.success("Profile saved!")

    # Tools
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Validate Setup"):
            result = subprocess.run(
                [sys.executable, "scripts/career.py", "validate"],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            st.code(result.stdout)

    with col2:
        if st.button("📊 Run ATS Score"):
            result = subprocess.run(
                [sys.executable, "scripts/career.py", "ats"],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            st.code(result.stdout or result.stderr)

    with col3:
        if st.button("🔨 Build All"):
            result = subprocess.run(
                [sys.executable, "scripts/career.py", "build", "--all"],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            st.code(result.stdout or result.stderr)


def main():
    """Main application entry point."""
    page = render_sidebar()

    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "📝 Applications":
        render_applications()
    elif page == "➕ New Application":
        render_new_application()
    elif page == "📈 Analytics":
        render_analytics()
    elif page == "⚙️ Settings":
        render_settings()


if __name__ == "__main__":
    main()
