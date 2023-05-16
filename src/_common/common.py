import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def delete_file(filename: str):
    """
    Delete file written to local to store data for transportation.

    :param filename: Name of file to delete
    :return:
    """
    if os.path.exists(filename):
        os.remove(filename)
    else:
        logger.info("The file does not exist")