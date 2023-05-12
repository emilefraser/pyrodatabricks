from .logging_config import get_logger


# get the root logger
# we don't have a logger defined in the config called Logging demo - so this is the root
root_logger = get_logger("Logging demo")


# call directly from the module so we can see how it logs with out a function name
root_logger.debug(f"Root logger called 'Logging demo' being called from module {__name__}")


# call from within a function so we can see how it grabs the function name
def my_function():
    root_logger.debug(f"Root logger called 'Logging demo' being called from a {__name__}.my_function")
my_function()


# now get a config defined logger that's not the root.
# note how it logs to console twice because it will fall through the root logger also
# and they both have a console logger, root also has a SQL Server logger it will be captured there also
# but only once since only the root logger has a sql server handler.
dev_logger = get_logger("additional_logger")
dev_logger.info("This will log in console twice since it automatically fall from the 'additional_logger' to the root.")