from motion_validator.reader import read_log_file


def test_read_log_file(tmp_path):
    file = tmp_path / "test.log"
    file.write_text("line1\nline2\nline3")

    lines = read_log_file(file)

    assert len(lines) == 3
    assert lines[0].line_number == 1
    assert lines[0].raw_text == "line1"
    assert lines[2].line_number == 3