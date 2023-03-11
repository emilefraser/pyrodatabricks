import os
import sys

import pandas as pd
from dotenv import load_dotenv

if 'utils' not in os.listdir():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    if 'utils' not in os.listdir():
        raise ImportError("The 'utils' module can not be found")

import utils.azure as az_utils

load_dotenv()

ADLS_GEN2_ACCOUNT_URL = os.getenv('ADLS_GEN2_ACCOUNT_URL')
ADLS_GEN2_ACCOUNT_KEY = os.getenv('ADLS_GEN2_ACCOUNT_KEY')


if __name__ == '__main__':

    # Test DataFrame
    df_test = pd.DataFrame([{'a': 1, 'b': 11},
                            {'a': 2, 'b': 22},
                            {'a': 3, 'b': 33}])

    # Upload DataFrame as CSV to a blob in a Data Lake
    az_utils.upload_df_as_csv_to_blob(df=df_test,
                                      account_url=ADLS_GEN2_ACCOUNT_URL,
                                      account_key=ADLS_GEN2_ACCOUNT_KEY,
                                      container=ADLS_GEN2_CONTAINER,
                                      blob='test.csv')

    # Upload DataFrame as parquet to a blob in a Data Lake
    az_utils.upload_df_as_parquet_to_blob(df=df_test,
                                          account_url=ADLS_GEN2_ACCOUNT_URL,
                                          account_key=ADLS_GEN2_ACCOUNT_KEY,
                                          container='test',
                                          blob='test.parquet')
