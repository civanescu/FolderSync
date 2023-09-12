import hashlib
import logging
import os

logger = logging.getLogger("logger")


class SyncFile:
    def __init__(self, source_file: str, destination_file: str, chunk_size: int = 1024):
        """
        Class to take care of synchronizing two files, made as a class for extensions
        :param source_file: String with the source file
        :param destination_file: String with the destination
        :param chunk_size: Chunk size for very big file
        :param remove_source: Boolean to remove the source file after syncing, not required now but can be used for
                further development
        :return: None
        """
        self.source_file = source_file
        self.destination_file = destination_file
        self.filename = os.path.basename(self.source_file)
        self.chunk_size = chunk_size

    def _must_sync(self) -> bool:
        """
        Check if we need to sync files (different content, missing destination)
        :return: True if we need to sync, False if not
        """
        md5_source, md5_destination = hashlib.md5(), hashlib.md5()
        if not os.path.exists(self.destination_file):
            return True
        else:
            with open(self.destination_file, 'rb') as dest_file:
                while True:
                    content_chunk_size = dest_file.read(self.chunk_size)
                    if not content_chunk_size:
                        break
                    md5_destination.update(content_chunk_size)

        with open(self.source_file, 'rb') as src_file:
            while True:
                content_chunk_size = src_file.read(self.chunk_size)
                if not content_chunk_size:
                    break
                md5_source.update(content_chunk_size)

        if md5_source.hexdigest() != md5_destination.hexdigest():
            return True
        else:
            return False

    def copy(self) -> bool:
        """
        Check source & destionation to sync, in case of different file after sync I suppose that can be under
        continuous change the source file so returned error.
        :return:
        """
        if not self._must_sync():
            return True
        try:
            with open(self.source_file, 'rb') as src_file:
                with open(self.destination_file, 'wb') as dest_file:
                    while True:
                        content_chunk_size = src_file.read(self.chunk_size)
                        if not content_chunk_size:
                            break
                        dest_file.write(content_chunk_size)
            logger.info(f"File {self.filename} synced")

        except Exception as e:
            logger.error(f"Error while syncing file {self.source_file} to {self.destination_file}, {e}")
            return False

        if not self._must_sync():
            return True
        else:
            logger.error(f"Error file {self.filename} source/destination not identical after copying, try rollback")
            try:  # Try to remove the file
                os.remove(self.destination_file)
            except:
                pass
            return False
