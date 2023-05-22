from typing import Union
import logging
import pandas as pd
from azure.storage.blob import BlobServiceClient


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def upload_data_to_blob(data: Union[str, bytes], account_url: str, account_key: str, container: str, blob: str):
    """
    Upload string or bytes data to Blob int Azure Data Lake (ADLS Gen2).

    :param data: Data to upload, which can be of type string or bytes
    :param account_url: Account URL for ADLS Gen2 storage account
    :param account_key: Account Key for ADLS Gen2 storage account
    :param container: Storage Account container to write data to
    :param blob: Blob name for data contents to be written to
    :return:
    """
    blob_service = BlobServiceClient(account_url=account_url, credential=account_key, timeout=90,
                                     max_single_put_size=4 * 1024 * 1024)
    blob_client = blob_service.get_blob_client(container, blob, snapshot=None)
    logger.info(f"Uploading Data for File: {blob} to container: {container}.")
    blob_client.upload_blob(data, overwrite=True)


def upload_df_as_csv_to_blob(df: pd. DataFrame, account_url: str, account_key: str, container: str, blob: str):
    """
    Upload Site specific Pandas Dataframe as Blob to Azure Data Lake (ADLS Gen2) as a CSV.

    :param df: Pandas Dataframe to Upload Data for.
    :param account_url: Account URL for ADLS Gen2 storage account
    :param account_key: Account Key for ADLS Gen2 storage account
    :param container: Storage Account container to write data to
    :param blob: Blob name for data contents to be written to
    :return:
    """
    data = df.to_csv(encoding='utf-8', index=False)
    upload_data_to_blob(data=data, account_url=account_url, account_key=account_key, container=container, blob=blob)


def upload_df_as_parquet_to_blob(df: pd. DataFrame, account_url: str, account_key: str, container: str, blob: str):
    """
    Upload Site specific Pandas Dataframe as Blob to Azure Data Lake (ADLS Gen2) as a CSV.

    :param df: Pandas Dataframe to Upload Data for.
    :param account_url: Account URL for ADLS Gen2 storage account
    :param account_key: Account Key for ADLS Gen2 storage account
    :param container: Storage Account container to write data to
    :param blob: Blob name for data contents to be written to
    :return:
    """
    data = df.to_parquet()
    upload_data_to_blob(data=data, account_url=account_url, account_key=account_key, container=container, blob=blob)
