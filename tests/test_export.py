"""Tests for export_resume.py - ATS format exports."""

import json
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from export_resume import (  # noqa: E402
    strip_markdown,
    export_txt,
    export_json_resume,
    parse_resume_sections,
)


class TestStripMarkdown:
    """Tests for markdown stripping."""

    def test_removes_headers(self):
        text = "# Header\n## Subheader\nContent"
        result = strip_markdown(text)
        assert "# " not in result
        assert "Header" in result

    def test_removes_bold(self):
        text = "This is **bold** text"
        result = strip_markdown(text)
        assert "**" not in result
        assert "bold" in result

    def test_removes_links(self):
        text = "Check [this link](https://example.com)"
        result = strip_markdown(text)
        assert "[" not in result
        assert "this link" in result

    def test_removes_code_blocks(self):
        text = "Code: `inline` and ```block```"
        result = strip_markdown(text)
        assert "`" not in result


class TestExportTxt:
    """Tests for TXT export."""

    def test_creates_txt_file(self, tmp_path):
        resume = tmp_path / "resume.md"
        resume.write_text("# John Doe\n\n## Experience\n\n- Did stuff")

        output = tmp_path / "resume.txt"

        with mock.patch("export_resume.load_identity", return_value={}):
            result = export_txt(resume, output)

        assert result is True
        assert output.exists()
        content = output.read_text()
        assert "John Doe" in content
        assert "Experience" in content

    def test_adds_identity_header(self, tmp_path):
        resume = tmp_path / "resume.md"
        resume.write_text("# Resume\n\nContent here")

        output = tmp_path / "resume.txt"

        identity = {
            "full_name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "555-1234",
        }
        with mock.patch("export_resume.load_identity", return_value=identity):
            export_txt(resume, output)

        content = output.read_text()
        assert "JANE SMITH" in content
        assert "jane@example.com" in content

    def test_returns_false_if_missing(self, tmp_path):
        resume = tmp_path / "nonexistent.md"
        output = tmp_path / "resume.txt"

        result = export_txt(resume, output)
        assert result is False


class TestExportJsonResume:
    """Tests for JSON Resume export."""

    def test_creates_json_file(self, tmp_path):
        resume = tmp_path / "resume.md"
        resume.write_text(
            """# Resume

## Summary

Experienced engineer.

## Experience

### Acme Corp

**Senior Engineer** (2020 - Present)

- Built systems
- Led team
"""
        )
        output = tmp_path / "resume.json"

        with mock.patch(
            "export_resume.load_identity",
            return_value={"full_name": "Test User", "email": "test@example.com"},
        ):
            result = export_json_resume(resume, output)

        assert result is True
        assert output.exists()

        data = json.loads(output.read_text())
        assert data["basics"]["name"] == "Test User"
        assert "$schema" in data

    def test_parses_experience(self, tmp_path):
        resume = tmp_path / "resume.md"
        resume.write_text(
            """## Experience

### Google

**Software Engineer** (2018 - 2022)

- Developed features
- Improved performance
"""
        )
        output = tmp_path / "resume.json"

        with mock.patch("export_resume.load_identity", return_value={}):
            export_json_resume(resume, output)

        data = json.loads(output.read_text())
        assert len(data["work"]) >= 1
        assert data["work"][0]["company"] == "Google"


class TestParseResumeSections:
    """Tests for resume section parsing."""

    def test_extracts_summary(self):
        content = """## Summary

Experienced software engineer with 10 years.

## Experience
"""
        sections = parse_resume_sections(content)
        assert "experienced" in sections["summary"].lower()

    def test_handles_empty_content(self):
        sections = parse_resume_sections("")
        assert sections["summary"] == ""
        assert sections["experience"] == []
