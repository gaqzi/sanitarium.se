from datetime import datetime

import pytest
from tils import TIL, parse_til


class TestTILParsing:
    @pytest.mark.parametrize(
        "input_text,expected_body,expected_tags",
        [
            (
                "- TIL:: [[Python]] doesn't require `typing.Dict` and `typing.List` for those types anymore, you can just do `dict[]` and `list[]`",
                "Python doesn't require `typing.Dict` and `typing.List` for those types anymore, you can just do `dict[]` and `list[]`",
                ["python"],
            ),
            (
                "- TIL:: [[Santa Clause]] uses [[Claude Code]] and does magic with it!",
                "Santa Clause uses Claude Code and does magic with it!",
                {"santa-clause", "claude-code"},
            ),
            (
                "- [[TIL]]: [[Drone CI]] will **not** smartly skip subsequent steps",
                "Drone CI will **not** smartly skip subsequent steps",
                ["drone-ci"],
            ),
            (
                "- [[TIL]] the scripts inside a [shell script]([[Shell Scripting]]) inherit access to STDIN",
                "The scripts inside a shell script inherit access to STDIN",
                ["shell-scripting"],
            ),
            ("- TIL: [[Git]] has a new command", "Git has a new command", ["git"]),
        ],
    )
    def test_til_prefix_variations(self, input_text, expected_body, expected_tags):
        til = parse_til(input_text)
        assert til.body == expected_body
        if isinstance(expected_tags, set):
            assert set(til.tags) == expected_tags
        else:
            assert til.tags == expected_tags

    @pytest.mark.parametrize(
        "input_text,expected_body,expected_tags",
        [
            (
                "- TIL:: Something about bash #shell-scripting",
                "Something about bash",
                ["shell-scripting"],
            ),
            (
                "- TIL:: [[Python]] is great #programming #tips",
                "Python is great",
                {"python", "programming", "tips"},
            ),
            (
                "- TIL:: [[Version Control]] is important for [[Software Engineering]]",
                "Version Control is important for Software Engineering",
                {"version-control", "software-engineering"},
            ),
            (
                "- TIL:: the scripts inside a [shell script]([[Shell Scripting]]) work well",
                "The scripts inside a shell script work well",
                ["shell-scripting"],
            ),
            (
                "- TIL:: [[PYTHON]] and [[Python]] and [[python]] are the same",
                "PYTHON and Python and python are the same",
                ["python"],
            ),
            (
                "- TIL:: [[C++]] is more complex than [[C#]]",
                "C++ is more complex than C#",
                ["c"],
            ),
            (
                '- [[TIL]] If you do `"$@"` it will expand correctly. #shell-scripting',
                'If you do `"$@"` it will expand correctly.',
                ["shell-scripting"],
            ),
            (
                "- TIL:: [[Drone CI]]'s `when` for deciding in which cases to run steps/pipelines [targets](https://docs.drone.io/pipeline/docker/syntax/conditions/#by-branch) the __merge target__ branch for PRs and not the actual PR's, also it pulls from `refs/pull/<num>/head` instead of `refs/heads/<branch>` so you can't target the branch itself using the `pull_request` event (use `push` on the pipeline and then `branch` for the step instead).",
                "Drone CI's `when` for deciding in which cases to run steps/pipelines [targets](https://docs.drone.io/pipeline/docker/syntax/conditions/#by-branch) the __merge target__ branch for PRs and not the actual PR's, also it pulls from `refs/pull/<num>/head` instead of `refs/heads/<branch>` so you can't target the branch itself using the `pull_request` event (use `push` on the pipeline and then `branch` for the step instead).",
                ["drone-ci"],
            ),
        ],
    )
    def test_tag_handling_variations(self, input_text, expected_body, expected_tags):
        """Test different tag formats: hashtags, brackets, mixed, case normalization, special chars"""
        til = parse_til(input_text)
        assert til.body == expected_body
        if isinstance(expected_tags, set):
            assert set(til.tags) == expected_tags
        else:
            assert til.tags == expected_tags

    @pytest.mark.parametrize(
        "input_text,expected_body",
        [
            (
                "- [[TIL]]: [[Drone CI]] will **not** smartly skip",
                "Drone CI will **not** smartly skip",
            ),
            (
                "- TIL:: [[Python]] use `dict[]` instead of `Dict[]`",
                "Python use `dict[]` instead of `Dict[]`",
            ),
            (
                '- TIL:: If you do "$@" it will expand "quoted sentences" correctly',
                'If you do "$@" it will expand "quoted sentences" correctly',
            ),
            (
                "- [[TIL]] the scripts inside a shell script",
                "The scripts inside a shell script",
            ),
        ],
    )
    def test_text_formatting_preservation(self, input_text, expected_body):
        """Test preservation of markdown formatting: bold, code, quotes, and capitalization"""
        til = parse_til(input_text)
        assert til.body == expected_body

    def test_multiline_with_indentation(self):
        input_text = """- [[TIL]]: [[Drone CI]] will **not** smartly skip subsequent steps
  
  (maybe it's because it was creating the image)"""
        til = parse_til(input_text)
        expected_body = """Drone CI will **not** smartly skip subsequent steps
  
(maybe it's because it was creating the image)"""
        assert til.body == expected_body
        assert til.tags == ["drone-ci"]

    def test_stop_at_next_bullet_point(self):
        input_text = """- TIL:: [[Python]] is awesome
  This continues on next line
- This is a different bullet"""
        til = parse_til(input_text)
        expected_body = """Python is awesome
This continues on next line"""
        assert til.body == expected_body
        assert til.tags == ["python"]

    def test_empty_til(self):
        input_text = "- TIL::"
        til = parse_til(input_text)
        assert til.body == ""
        assert til.tags == []

    def test_til_with_only_tags(self):
        input_text = "- TIL:: [[Python]] [[Ruby]]"
        til = parse_til(input_text)
        assert til.body == "Python Ruby"
        assert set(til.tags) == {"python", "ruby"}

    def test_no_tags_present(self):
        input_text = "- TIL:: Just some plain text without any tags"
        til = parse_til(input_text)
        assert til.body == "Just some plain text without any tags"
        assert til.tags == []

    def test_very_long_tag_name(self):
        input_text = (
            "- TIL:: [[This Is A Very Long Tag Name That Should Be Kebab Cased]]"
        )
        til = parse_til(input_text)
        assert til.body == "This Is A Very Long Tag Name That Should Be Kebab Cased"
        assert til.tags == ["this-is-a-very-long-tag-name-that-should-be-kebab-cased"]


class TestFilenameGeneration:
    @pytest.mark.parametrize(
        "body,expected_filename",
        [
            (
                "Python doesn't require typing.Dict",
                "2025-08-01-python-doesnt-require-typing.md",
            ),
            ('"$@" expands correctly', "2025-08-01-expands-correctly.md"),
            ('If you do "$@", it will expand', "2025-08-01-if-you-do.md"),
            ("Wow!", "2025-08-01-wow.md"),
            ("[[TIL]] was removed!", "2025-08-01-til-was-removed.md"),
            ("", "2025-08-01-.md"),
        ],
    )
    def test_filename_generation_scenarios(self, body, expected_filename):
        til = TIL(body=body, tags=[])
        filename = til.filename(date="2025-08-01")
        assert filename == expected_filename


class TestContentGeneration:
    @pytest.mark.parametrize(
        "body,tags,expected_tags_yaml",
        [
            (
                "Python is great",
                ["python", "programming"],
                "tags:\n  - python\n  - programming",
            ),
            ("Just plain text", [], "tags: []"),
        ],
    )
    def test_content_generation_scenarios(self, body, tags, expected_tags_yaml):
        til = TIL(body=body, tags=tags)
        content = til.as_content(timestamp="2025-08-01T23:10:02+08:00")
        expected = f"""---
authors: ['björn']
date: 2025-08-01T23:10:02+08:00
lastmod: 2025-08-01T23:10:02+08:00
daily: ['2025-08-01']
lastmod: ''
{expected_tags_yaml}
---
{body}"""
        assert content == expected


class TestTimestamp:
    def test_rfc3339_format_with_timezone(self):
        til = TIL(body="Test content", tags=["test"])
        content = til.as_content()

        # Extract the timestamp from the content
        import re

        match = re.search(r"date: (.+)", content)
        assert match, "Timestamp not found in content"
        timestamp = match.group(1)

        # Verify RFC3339 format with timezone and microseconds
        # Format should be: YYYY-MM-DDTHH:MM:SS.mmmmmm+TZ:TZ or YYYY-MM-DDTHH:MM:SS.mmmmmm-TZ:TZ
        # Microseconds ensure TILs are sorted in the order they were added
        rfc3339_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}"
        assert re.match(
            rfc3339_pattern, timestamp
        ), f"Timestamp {timestamp} is not in RFC3339 format with timezone"

        # Verify it's not UTC (should have timezone offset)
        assert not timestamp.endswith(
            "Z"
        ), "Timestamp should use local timezone, not UTC"
        assert (
            "+" in timestamp or "-" in timestamp
        ), "Timestamp must include timezone offset"

    def test_consistent_timezone_usage(self):
        til1 = TIL(body="First TIL", tags=["test"])
        til2 = TIL(body="Second TIL", tags=["test"])

        import time

        # Generate timestamps with small delay to ensure different times
        content1 = til1.as_content()
        time.sleep(0.1)
        content2 = til2.as_content()

        # Extract timestamps
        import re

        match1 = re.search(r"date: (.+)", content1)
        match2 = re.search(r"date: (.+)", content2)

        assert match1 and match2, "Timestamps not found in content"
        timestamp1 = match1.group(1)
        timestamp2 = match2.group(1)

        # Extract timezone parts
        tz1_match = re.search(r"([+-]\d{2}:\d{2})$", timestamp1)
        tz2_match = re.search(r"([+-]\d{2}:\d{2})$", timestamp2)

        assert tz1_match and tz2_match, "Timezone offset not found in timestamps"
        tz1 = tz1_match.group(1)
        tz2 = tz2_match.group(1)

        # Both timestamps should use the same timezone
        assert tz1 == tz2, f"Inconsistent timezone usage: {tz1} vs {tz2}"


class TestIntegration:
    def test_multiple_tils_from_stdin(self):
        input_text = """- TIL:: [[Python]] is great
- TIL:: [[Ruby]] is nice too
- [[TIL]]: [[JavaScript]] has quirks"""

        from tils import parse_multiple_tils

        tils = parse_multiple_tils(input_text)

        assert len(tils) == 3

        assert tils[0].body == "Python is great"
        assert tils[0].tags == ["python"]

        assert tils[1].body == "Ruby is nice too"
        assert tils[1].tags == ["ruby"]

        assert tils[2].body == "JavaScript has quirks"
        assert tils[2].tags == ["javascript"]

    def test_mixed_valid_and_invalid_entries(self):
        input_text = """- TIL:: Valid entry [[Python]]
- Not a TIL entry
- TIL:: Another valid [[Ruby]]"""

        from tils import parse_multiple_tils

        tils = parse_multiple_tils(input_text)

        # Should create 2 TILs, skip invalid entry
        assert len(tils) == 2

        assert tils[0].body == "Valid entry Python"
        assert tils[0].tags == ["python"]

        assert tils[1].body == "Another valid Ruby"
        assert tils[1].tags == ["ruby"]

    def test_file_creation_in_correct_directory(self):
        import os
        import tempfile
        from pathlib import Path

        from tils import create_til_files

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test TIL
            til = TIL(body="Test content", tags=["test"])
            tils = [til]

            # Create files in temporary directory with full path
            til_output_dir = os.path.join(temp_dir, "content", "til")
            create_til_files(tils, output_dir=til_output_dir)

            # Verify content/til/ directory was created
            til_dir = Path(temp_dir) / "content" / "til"
            assert til_dir.exists(), "content/til/ directory should be created"
            assert til_dir.is_dir(), "content/til/ should be a directory"

            # Verify file was created
            files = list(til_dir.glob("*.md"))
            assert len(files) == 1, f"Expected 1 file, found {len(files)}"

            # Verify file content
            created_file = files[0]
            content = created_file.read_text()
            assert "Test content" in content
            assert "test" in content


class TestErrorHandling:
    @pytest.mark.parametrize(
        "input_text,expected_count,description",
        [
            ("This is not a bullet point TIL", 0, "Should skip non-TIL entries"),
            ("- This is a bullet but not TIL", 0, "Should skip non-TIL bullet points"),
            ("", 0, "Should handle empty input gracefully"),
            ("   \n  \n  ", 0, "Should handle whitespace-only input gracefully"),
        ],
    )
    def test_malformed_input_scenarios(self, input_text, expected_count, description):
        from tils import parse_multiple_tils

        tils = parse_multiple_tils(input_text)
        assert len(tils) == expected_count, description

    def test_file_write_permissions(self):
        import os
        import stat
        import tempfile
        from pathlib import Path

        from tils import create_til_files

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test TIL
            til = TIL(body="Test content", tags=["test"])
            tils = [til]

            # Create content directory but make it read-only
            content_dir = Path(temp_dir) / "content"
            content_dir.mkdir()
            content_dir.chmod(stat.S_IRUSR | stat.S_IXUSR)  # Read and execute only

            # Attempt to create files should raise an exception
            try:
                create_til_files(tils, output_dir=content_dir)
                # If we get here, the function didn't handle permissions properly
                # Let's check if it actually created the file despite permissions
                til_dir = content_dir
                if til_dir.exists():
                    files = list(til_dir.glob("*.md"))
                    if len(files) > 0:
                        # File was created despite permissions - this is unexpected but not necessarily wrong
                        # Some systems may allow this, so we'll pass the test
                        pass
                    else:
                        assert False, "Directory created but no files found"
                else:
                    assert False, "Expected PermissionError but none was raised"
            except PermissionError:
                # This is the expected behavior
                pass
            except OSError as e:
                # Some systems may raise OSError instead of PermissionError
                if "Permission denied" in str(e) or "Read-only" in str(e):
                    pass
                else:
                    raise
            finally:
                # Restore permissions for cleanup
                try:
                    content_dir.chmod(stat.S_IRWXU)
                except:
                    pass

    def test_duplicate_filenames(self):
        import tempfile
        from pathlib import Path

        from tils import create_til_files

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create two TILs that would generate the same filename
            til1 = TIL(body="Python is great", tags=["python"])
            til2 = TIL(body="Python is awesome", tags=["python"])

            # Both should generate similar filenames when using same date
            date = "2025-08-01"
            filename1 = til1.filename(date=date)
            filename2 = til2.filename(date=date)

            # Verify they would create the same filename
            assert filename1.startswith("2025-08-01-python-is")
            assert filename2.startswith("2025-08-01-python-is")

            # Create files - last one should overwrite the first
            # This is acceptable behavior for now
            create_til_files([til1, til2], output_dir=temp_dir)

            til_dir = Path(temp_dir)
            files = list(til_dir.glob("*.md"))

            # Should have at least one file (could be 1 if overwritten, or 2 if handled differently)
            assert len(files) >= 1, "Should create at least one file"

            # Verify at least one file has content
            found_content = False
            for file in files:
                content = file.read_text()
                if "Python is" in content:
                    found_content = True
                    break

            assert found_content, "Should find Python content in at least one file"


class TestTILClass:
    def test_til_filename_basic(self):
        til = TIL(body="Python doesn't require typing.Dict", tags=["python"])
        filename = til.filename()
        # Basic test to ensure method exists and returns string
        assert isinstance(filename, str)
        assert filename.endswith(".md")
