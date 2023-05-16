from exchangelib import Account, Configuration, Credentials, DELEGATE, FileAttachment, Message
import tempfile
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERNAME = 'FQML\<some-username>'
PASSWORD = ''
ACC_USERNAME = '<your-email>'


def write_local(attachment_, file_location_):
    """
    Write Email Attachments to Local Files in Temp Directory

    :param attachment_: Email FileAttachment Object
    :param file_location_: Local File Location
    :return:
    """
    content = attachment_.content
    content_write = content.decode()
    logger.info(f"Writing attachment data to local file {file_location_}")
    with open(file_location_, 'wb') as file:
        file.write(content_write.encode('utf-8'))


if __name__ == '__main__':

    try:
        credentials = Credentials(USERNAME, PASSWORD)
        config = Configuration(server='owa.fqml.com', credentials=credentials)
        account = Account(ACC_USERNAME, autodiscover=False, config=config, access_type=DELEGATE)
        dirpath = Path(tempfile.mkdtemp())  # Set to whatever directory you want to write to
        for email in account.inbox.all().filter(is_read=False).order_by('-datetime_received'):
            if isinstance(email, Message):
                for attachment in email.attachments:
                    if isinstance(attachment, FileAttachment):
                        file_location = dirpath / attachment.name
                        write_local(attachment, file_location)
                        logger.info(f"Successfully Downloaded File: {file_location}.")
                        email.is_read = True
                        email.save()
        logger.info("Done.")
    except Exception as e:
        logger.error(f"Caught Exception: {e}.")
        raise e
