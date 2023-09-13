import logging
import os
from unittest.mock import patch

import pytest

from main import logging_setup, main, remove_files


@pytest.fixture
def fix_time():
    with patch("time.sleep") as mock_sleep:
        yield mock_sleep


@pytest.mark.parametrize(
    "source_folder, destination_folder, sleep_time, expected_exception",
    [
        ("source_folder", "replica_folder", 0, False),
        ("source_folder", "replica_folder", "wrong_time", True),
        ("wrong_source_folder", "wrong_destination_folder", 0, True),
        ("source_folder", "wrong_destination_folder", 0, True),
        ("wrong_source_folder", "destination_folder", 0, True),
    ],
)
def test_main(
    fix_time, caplog, source_folder, destination_folder, sleep_time, expected_exception
):
    with caplog.at_level(logging.INFO):
        main(source_folder, destination_folder, sleep_time)

    if expected_exception is False:
        assert "INFO" in caplog.text
    if expected_exception is True:
        assert "ERROR" in caplog.text


@pytest.mark.parametrize(
    "log_file, expected_exception",
    [
        ("logs/right.log", None),  # No Fail
        ("wrong_path/wrong_path.log", "Logs file directory does not exists"),
    ],
)
def test_logging_file_setup(log_file, expected_exception):
    if expected_exception is not None:
        with pytest.raises(SystemExit) as exception:
            logger = logging_setup(log_file)
            logger.removeHandler(logger.handlers[0])
            os.remove(log_file)
        assert str(exception.value) == expected_exception


def test_logging_setup(tmp_path):
    log_file = tmp_path / "logs.log"
    logger = logging_setup(str(log_file))

    # config
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.FileHandler)
    assert isinstance(logger.handlers[1], logging.StreamHandler)
    assert logger.level == logging.INFO
    assert logger.handlers[0].formatter._fmt == "%(asctime)s %(levelname)s %(message)s"

    # output
    logger.info("Mock message")

    # check content (reconfigured to remove the time/level)
    with open(log_file, "r") as file_log:
        message = file_log.read().split("INFO ", 1)[1]
        assert message == f"Mock message\n"

    # clear content
    logger.removeHandler(logger.handlers[0])
    os.remove(log_file)


def test_remove_files(tmp_path, caplog):
    file_1 = tmp_path / "file_1"
    file_2 = tmp_path / "file_2"
    file_1.touch()
    file_2.touch()

    with caplog.at_level(logging.INFO):
        remove_files(str(tmp_path), {"file_1", "file_2", "mocked"})

    assert not file_1.exists()
    assert not file_2.exists()
    assert "file_1 removed" in caplog.text
    assert "File mocked could not be removed" in caplog.text


if __name__ == "__main__":
    # define the logger you want to use
    logger = logging.getLogger("logger")
