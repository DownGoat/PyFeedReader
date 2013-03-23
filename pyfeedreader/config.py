__author__ = 'sis13'

import logging
from datetime import date

version = "0.01"

#Config for FeedServer database, this is so it can support using multiple databases. If you are only using one use
#same configuration for both DB configs.
feedserver_db = {
    "db_user": "root",
    "db_pass": "123qwe",
    "db_host": "localhost",
    "db_name": "gripper",
    "db_type": "mysql",
    "db_port": "3306",
    }

config = {
    # DB config
    "db_user": "root",
    "db_pass": "123qwe",
    "db_host": "localhost",
    "db_name": "gripper",
    "db_type": "mysql",
    "db_port": "3306",

    "version":      version,
    "User-agent":   "pyfeedreader-v{0}".format(version),

    "log_app":      "pyfeedreader",
    "log_file":     "pyfeedreader_{0}.log".format(date.today().isoformat()),
    "log_level":    logging.DEBUG,
    #"log_level":    logging.INFO,

    # Number of ReaderThread to start.
    "reader_threads":   10,

    # How often to look for updates in minutes
    "update_frequency": 1,
    }

config["db_connector"] = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    config.get("db_type"),
    config.get("db_user"),
    config.get("db_pass"),
    config.get("db_host"),
    config.get("db_port"),
    config.get("db_name")
)

feedserver_db["db_connector"] = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    config.get("db_type"),
    config.get("db_user"),
    config.get("db_pass"),
    config.get("db_host"),
    config.get("db_port"),
    config.get("db_name")
)

logger = logging.getLogger(config.get("log_app"))
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(config.get("log_file", "unkown"))
fh.setLevel(config.get("log_level"))
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)