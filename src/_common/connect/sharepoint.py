import logging
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def download_file_from_sharepoint(site_url: str, file_url: str, username: str, password: str):
    """
    Function to download file from Sharepoint.

    :param site_url: Sharepoint Site URL
    :param file_url: Sharepoint File URL
    :param username: Username to use to Authenticate Sharepoint Site
    :param password: Password for above username

    :return Path to File which was ingested.
    """
    user_credentials = UserCredential(username, password)
    ctx = ClientContext(site_url).with_credentials(user_credentials)
    download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
    with open(download_path, "wb") as local_file:
        ctx.web.get_file_by_server_relative_path(file_url).download(
            local_file).execute_query()
    logger.info(f"[Ok] file has been downloaded into: {download_path}.")
    return download_path
