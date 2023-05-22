import logging
import logging.config
import yaml
import os


def get_logger(name:str)->logging.Logger:
    """
            get_logger function
            Parameters:
                name: the name of the logger to get. If it's not defined in config it will be the root
                      use a name that allows the identification of the application that's logging.
            Returns:
                A logger with a specific name based on the configuration
    """

    directoryPath = os.getenv("LOGGINGDEMOHOME", "./")

    with open(f"{directoryPath}logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    return logging.getLogger(name)