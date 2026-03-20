from motion_validator.engine import ValidationEngine


def test_engine_pass(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "\n".join(
            [
                "12:00:00 DBG_MSG > servo Z-Axis       to be moved, pos(inc):     100 | vel(rpm):       10",
                "12:00:01 DBG_MSG > >>>--->target reached: Z-Axis, position: 100",
                "12:00:02 DBG_MSG > servo Z-Axis standby timestamp: 123456",
                "12:00:03 DBG_MSG > drive status|error: 0000|0000",
            ]
        )
    )

    engine = ValidationEngine()
    report = engine.run(str(log_file))

    assert report.overall_pass is True


def test_engine_fail(tmp_path):
    log_file = tmp_path / "test_fail.log"

    log_file.write_text(
        "\n".join(
            [
                "12:00:00 DBG_MSG > servo Z-Axis       to be moved, pos(inc):     100 | vel(rpm):       10",
                "12:00:03 DBG_MSG > drive status|error: 1234|0000",
            ]
        )
    )

    engine = ValidationEngine()
    report = engine.run(str(log_file))

    assert report.overall_pass is False