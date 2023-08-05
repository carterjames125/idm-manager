#/usr/bin/python3
import logging.config
import logging
import yaml
import pathlib
CONFIG = 'logging.yml'
def idm_logger(name:str) -> logging.getLogger:
    """
    idm_logger

    _extended_summary_

    Args:
        name (str): Logger name

    Returns:
        logging.getLogger: Logging object
    """

    with open(CONFIG, 'r') as stream:
        log_config = yaml.safe_load(stream.read())
        logging.config.dictConfig(config=log_config)

    logger = logging.getLogger(name)
    return logger
