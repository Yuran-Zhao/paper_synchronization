import logging


def config_logger(log_level=logging.INFO, log_file=None):
    format = '%(asctime)s %(levalname)s %(name)s:%(lineno)d - %(message)s'
    if log_file is not None:
        logging.basicConfig(format=format, level=log_level, filename=log_file)
    else:
        logging.basicConfig(format=format, level=log_level)