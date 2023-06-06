# encoding: utf-8
import logging

# config
LOG_LEVEL = logging.INFO
LOG_NAME = 'root'
LOG_FILE_NAME = 'run.log'
LOG_ENCODING = 'utf-8'

# create logger
log = logging.getLogger(LOG_NAME)
log.setLevel(LOG_LEVEL)

# file handler
file_handler = logging.FileHandler(LOG_FILE_NAME, encoding=LOG_ENCODING)
file_handler.setLevel(LOG_LEVEL)

# console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add handler
log.addHandler(file_handler)
log.addHandler(console_handler)
