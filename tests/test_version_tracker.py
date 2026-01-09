"""Tests for version_tracker.py - Resume version tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from version_tracker import VersionTracker  # noqa: E402


class TestVersionTracker:
    """Tests for the VersionTracker class."""

    def test_init_sets_versions_dir(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()

        tracker = VersionTracker(app_dir)

        # Dir is created on first save, not on init
        assert tracker.version_dir == app_dir / ".versions"

    def test_save_version_creates_file(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        (app_dir / "resume.md").write_text("# My Resume\n\nContent")

        tracker = VersionTracker(app_dir)
        result = tracker.save_version("resume.md", "Initial version")

        assert result is not None
        assert result["id"] == "v1"
        assert result["message"] == "Initial version"

    def test_save_increments_version(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("# Version 1")

        tracker = VersionTracker(app_dir)
        v1 = tracker.save_version("resume.md", "First")

        resume.write_text("# Version 2")
        v2 = tracker.save_version("resume.md", "Second")

        assert v1["id"] == "v1"
        assert v2["id"] == "v2"

    def test_list_versions(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("Content 1")

        tracker = VersionTracker(app_dir)
        tracker.save_version("resume.md", "First")

        resume.write_text("Content 2")
        tracker.save_version("resume.md", "Second")

        versions = tracker.list_versions("resume.md")
        assert len(versions) == 2
        assert versions[0]["id"] == "v1"
        assert versions[1]["id"] == "v2"

    def test_get_version_content(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("Original content")

        tracker = VersionTracker(app_dir)
        tracker.save_version("resume.md", "Original")

        resume.write_text("Modified content")

        content = tracker.get_version("v1", "resume.md")
        assert content == "Original content"

    def test_restore_version(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("Version 1 content")

        tracker = VersionTracker(app_dir)
        tracker.save_version("resume.md", "v1")

        resume.write_text("Version 2 content")
        tracker.save_version("resume.md", "v2")

        result = tracker.restore_version("v1", "resume.md")

        assert result is True
        assert resume.read_text() == "Version 1 content"

    def test_no_duplicate_if_unchanged(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("Same content")

        tracker = VersionTracker(app_dir)
        v1 = tracker.save_version("resume.md", "First")
        v2 = tracker.save_version("resume.md", "Second")

        assert v1 is not None
        assert v2 is None  # No changes, should return None

    def test_diff_versions(self, tmp_path):
        app_dir = tmp_path / "test-app"
        app_dir.mkdir()
        resume = app_dir / "resume.md"
        resume.write_text("Line 1\nLine 2\nLine 3")

        tracker = VersionTracker(app_dir)
        tracker.save_version("resume.md", "v1")

        resume.write_text("Line 1\nModified Line\nLine 3\nLine 4")
        tracker.save_version("resume.md", "v2")

        diff = tracker.diff_versions("v1", "v2", "resume.md")

        assert diff is not None
        assert diff["added_count"] >= 1
        assert diff["removed_count"] >= 1
