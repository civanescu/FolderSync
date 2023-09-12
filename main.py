import logging
import os
import sys
import time
from typing import Union

from src.sync_file import SyncFile

logger = logging.getLogger("logger")


def logging_setup(log_file: str) -> logging.Logger:
    """
    Setup the logging system for the application
    :param log_file:
    :return:
    """
    directory = os.path.dirname(log_file)
    if not os.path.exists(directory):
        exit("Logs file directory does not exists")

    logger.setLevel(logging.INFO)
    log_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    file_handler = logging.FileHandler(log_file, mode="a", encoding=None, delay=False)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    logger.addHandler(stream_handler)

    return logger


def remove_files(destination_folder: str, removal_files: set):
    """
    Try to remove files from the destination folder
    :param destination_folder:
    :param removal_files:
    :return:
    """
    for file in removal_files:
        try:
            os.remove(os.path.join(destination_folder, file))
            logger.info(f"File {file} removed")
        except Exception as e:
            logger.error(f"File {file} could not be removed, {e}")


def main(source_folder: str, destination_folder: str, sleep_time: Union[str, int]):
    """
    Main function that reads the content of source and set the destination folder, and also the time to sleep in seconds.
    If we set time to sleep to 0 it will only run one time
    :param source_folder:
    :param destination_folder:
    :param sleep_time:
    :return:
    """
    try:
        sleep_time = int(sleep_time)
    except Exception as e:
        logger.error(f"Application was accessed with wrong type of sleep parameter {sys.argv}, {e}")
        return

    while True:
        if os.path.exists(source_folder) and os.path.exists(destination_folder):
            logger.info(f"Syncing files between {source_folder} and {destination_folder}")
            source_files = set(os.listdir(source_folder))
            dest_files = set(os.listdir(destination_folder))
            removal_files = dest_files - source_files
            remove_files(destination_folder, removal_files)

            for file in source_files:
                file_handler = SyncFile(os.path.join(source_folder, file), os.path.join(destination_folder, file))
                file_handler.copy()
        else:
            logger.error(f"Source or destination folder does not exist {source_folder} | {destination_folder}")
            return

        if sleep_time == 0:
            return
        time.sleep(sleep_time)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python main.py <source_folder> <destination_folder> <log_file> <sleep_time_in_seconds: int>")
        exit(sys.argv)

    logger = logging_setup(sys.argv[3])
    main(sys.argv[1], sys.argv[2], sys.argv[4])
