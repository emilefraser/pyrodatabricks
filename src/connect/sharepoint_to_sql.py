import os
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.sql import upload_to_sql
from utils.sharepoint import download_file_from_sharepoint

SITE_URL = os.getenv(
    'SHAREPOINT_SITE_URL')  # e.g. https://fqml.sharepoint.com/sites/MCM-COVIDTracking
FILE_URL = os.getenv(
    'SHAREPOINT_FILE_URL')  # e.g. /sites/MCM-COVIDTracking/Shared Documents/file.xlsx
SP_USERNAME = os.getenv('SP_USERNAME')
SP_PASSWORD = os.getenv('SP_PASSWORD')
SQL_USERNAME = os.getenv('SQL_USERNAME')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_HOST = os.getenv('SQL_HOST')
SQL_DB = os.getenv('SQL_DB')
SQL_PORT = os.getenv('SQL_PORT')

if __name__ == '__main__':
    ingested_file = download_file_from_sharepoint(SITE_URL, FILE_URL, SP_USERNAME, SP_PASSWORD)
    # READ IN DATA e.g. using pandas to read Excel. Should be changed per different file
    file_df = pd.read_excel(ingested_file)
    # DO TRANSFORMATIONS HERE/BELOW
    # UPLOAD TO SQL
    upload_to_sql(file_df, 'test_table', SQL_USERNAME, SQL_PASSWORD, SQL_HOST, SQL_DB, SQL_PORT)
