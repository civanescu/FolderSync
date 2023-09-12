import os

import pytest

from src.sync_file import SyncFile


def test__must_sync():
    mock_file = "source_folder/mock_file.txt"
    dest_file = "replica_folder/mock_file.txt"
    sync_file = SyncFile(mock_file, dest_file)

    try:  # clear the replica
        os.remove(dest_file)
    except:
        pass

    assert sync_file._must_sync() is True

    # Manually copy the destination file content to make them identical
    with open(dest_file, 'wb') as d_file:
        with open(mock_file, 'rb') as m_file:
            d_file.write(m_file.read())

    assert sync_file._must_sync() is False
    os.remove(dest_file)


@pytest.mark.parametrize("mock_file, dest_file, result", [
    ("source_folder/mock_file.txt", "replica_folder/mock_file.txt", True),
    ("source_folder/missing_file.txt", "replica_folder/mock_file.txt", False),
    ("source_folder/mock_file.txt", "wrong_folder/mock_file.txt", False)])
def test_copy(mock_file, dest_file, result):
    try:  # clear the replica
        os.remove(dest_file)
    except:
        pass
    sync_file = SyncFile(mock_file, dest_file)
    assert sync_file.copy() is result

    if result:  # in case we have correct parameters
        # Change content
        with open(dest_file, 'wb') as file:
            file.write(b"Modified Content")

        assert sync_file.copy() is True
        assert sync_file._must_sync() is False

        os.remove(dest_file)
