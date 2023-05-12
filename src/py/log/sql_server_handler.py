import logging
from logging import LogRecord
import pyodbc 


class SqlServerHandler(logging.Handler):

    def __init__(self, connection_string:str, sql:str, log_record_delimiter:str=","):
        """
        SqlServerHandler class constructor
        Parameters:
            self: instance of the class
            connection_string: pyodbc connection string to connect to db
            sql: parameterised sql statement
            log_record_delimiter: delimiter to split the formatted message into sql parameter values default=,
        Returns:
            None
        """

        super().__init__()
        self._connection_string = connection_string
        self._sql = sql
        self._log_record_delimiter = log_record_delimiter


    def emit(self, record: LogRecord) -> None:
        """
            Save the log record to SQL Server
            Parameters:
                self: instance of the class
                record: log record to be saved
            Returns:
                None
        """

        # Use configured formatter, sql is all driven of the config.
        values = [s.strip().replace(".<module>", "") 
            for s in self.format(record).split(self._log_record_delimiter)]

        conn = pyodbc.connect(self._connection_string)
        cursor = conn.cursor()

        count = cursor.execute(self._sql, values).rowcount
        conn.commit()
