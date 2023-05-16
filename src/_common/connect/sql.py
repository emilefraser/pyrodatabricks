import sqlalchemy
import logging
import pandas as pd
from datetime import datetime
from urllib.parse import quote

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_engine(username: str, password: str, server: str, db: str, port: str = None,
                  dialect: str = 'mssql+pymssql'):
    """
    Create SQLAlchemy engine to allow for DB manipulations.

    :param username: SQL server username
    :param password: SQL Server Password
    :param server: SQL Server host
    :param db: Database to be used
    :param port: DB Port if needed
    :param dialect: system SQLAlchemy uses to communicate with various types of DBAPI
                    implementations and databases e.g. mssql+pymssql for MSSQL Server
                    https://docs.sqlalchemy.org/en/14/dialects/
    :return:
    """
    engine_str = f'{dialect}://{username}:%s@{server}:{port}/{db}' if port else \
        f'{dialect}://{username}:%s@{server}/{db}'
    engine_str = engine_str % quote(str(password))
    logger.info(f"{datetime.now()}: Creating SQL Engine for Server: {server}.")
    engine = sqlalchemy.create_engine(engine_str, pool_pre_ping=True)
    return engine


def upload_to_sql(df: pd.DataFrame, table_name: str, username: str, password: str, server: str,
                  db: str, port: str = None):
    """
    Upload data from Pandas Dataframe to SQL Server.

    :param df: CSV File Path
    :param table_name: SQL Table name to write data to
    :param username: SQL server username
    :param password: SQL Server Password
    :param server: SQL Server host
    :param db: Database to be used
    :param port: DB Port if needed
    """
    engine = create_engine(username, password, server, db, port)
    logger.info(f"{datetime.now()}: Writing Data to SQL Server Table: {table_name}.")
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=3000)


def ingest_data_from_sql(sql_query: str, username: str, password: str, server: str, db: str,
                         port: str = None):
    """
    Ingest Data from Microsoft SQL Server DB using SQL Query into Pandas DataFrame.

    :param sql_query: SQL Query as String
    :param username: DB Username
    :param password: DB Password
    :param server: SQL Server hostname/IP
    :param db: Database name
    :param port: Port Number
    :return: Dataframe with ingested data
    """
    engine = create_engine(username, password, server, db, port)
    return pd.read_sql(sql_query, engine)
