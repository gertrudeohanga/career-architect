"""Tests for batch_process.py - Batch JD processing."""

import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from batch_process import (  # noqa: E402
    slugify,
    extract_metadata,
    create_application,
    process_folder,
)


class TestSlugify:
    """Tests for slug generation."""

    def test_lowercase(self):
        assert slugify("Hello World") == "hello-world"

    def test_removes_special_chars(self):
        assert slugify("Acme & Co.") == "acme-co"

    def test_handles_multiple_spaces(self):
        assert slugify("Multiple   Spaces") == "multiple-spaces"


class TestExtractMetadata:
    """Tests for JD metadata extraction."""

    def test_extracts_company_role(self):
        content = """Company: Acme Corp
Role: Software Engineer

Job description here..."""

        metadata = extract_metadata(content)
        assert metadata["company"] == "Acme Corp"
        assert metadata["role"] == "Software Engineer"

    def test_extracts_from_header(self):
        content = """# Google - Senior Engineer

We are looking for..."""

        metadata = extract_metadata(content)
        assert metadata["company"] == "Google"
        assert metadata["role"] == "Senior Engineer"

    def test_handles_empty_content(self):
        metadata = extract_metadata("")
        assert metadata["company"] == ""
        assert metadata["role"] == ""


class TestCreateApplication:
    """Tests for application creation."""

    def test_creates_folder(self, tmp_path):
        with mock.patch("batch_process.APPLICATIONS_DIR", tmp_path):
            content = "Job description content"
            result = create_application(content, "TestCorp", "Engineer")

            assert result is not None
            assert result.exists()
            assert "testcorp" in result.name
            assert (result / "job_desc.md").exists()

    def test_includes_frontmatter(self, tmp_path):
        with mock.patch("batch_process.APPLICATIONS_DIR", tmp_path):
            create_application("JD content", "Acme", "Developer")

            dirs = list(tmp_path.iterdir())
            job_desc = (dirs[0] / "job_desc.md").read_text()

            assert "company: Acme" in job_desc
            assert "role: Developer" in job_desc
            assert "source: batch_import" in job_desc

    def test_skips_duplicate(self, tmp_path):
        with mock.patch("batch_process.APPLICATIONS_DIR", tmp_path):
            result1 = create_application("Content", "Dupe", "Role")
            result2 = create_application("Content", "Dupe", "Role")

            assert result1 is not None
            assert result2 is None


class TestProcessFolder:
    """Tests for folder processing."""

    def test_processes_md_files(self, tmp_path):
        input_dir = tmp_path / "jds"
        input_dir.mkdir()

        (input_dir / "google-swe.md").write_text(
            "Company: Google\nRole: SWE\n\nDescription"
        )
        (input_dir / "meta-pm.md").write_text("Company: Meta\nRole: PM\n\nDescription")

        output_dir = tmp_path / "apps"
        output_dir.mkdir()

        with mock.patch("batch_process.APPLICATIONS_DIR", output_dir):
            results = process_folder(input_dir, dry_run=False)

        assert len(results["processed"]) == 2
        assert len(results["errors"]) == 0

    def test_dry_run_no_create(self, tmp_path):
        input_dir = tmp_path / "jds"
        input_dir.mkdir()
        (input_dir / "test.md").write_text("Company: Test\nRole: Dev")

        output_dir = tmp_path / "apps"
        output_dir.mkdir()

        with mock.patch("batch_process.APPLICATIONS_DIR", output_dir):
            results = process_folder(input_dir, dry_run=True)

        assert len(results["processed"]) == 1
        assert len(list(output_dir.iterdir())) == 0  # No folders created

    def test_handles_txt_files(self, tmp_path):
        input_dir = tmp_path / "jds"
        input_dir.mkdir()
        (input_dir / "job.txt").write_text("Company: Acme\nRole: Eng")

        output_dir = tmp_path / "apps"
        output_dir.mkdir()

        with mock.patch("batch_process.APPLICATIONS_DIR", output_dir):
            results = process_folder(input_dir, dry_run=False)

        assert len(results["processed"]) == 1
