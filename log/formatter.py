import logging


def set_formatter(logger):
    logger.handlers[0].setFormatter(LogFormatter())


class LogFormatter(logging.Formatter):
    info = "\033[92m"
    warning = '\033[93m'
    error = "\033[91m"
    critical = "\033[91;1m"
    endc = "\033[0m"
    format = "[%(asctime)s] - %(module)s - {}%(levelname)s{}: %(message)s"

    FORMATS = {
        logging.DEBUG: format.format('', ''),
        logging.INFO: format.format(info, endc),
        logging.WARNING: format.format(warning, endc),
        logging.ERROR: format.format(error, endc),
        logging.CRITICAL: format.format(critical, endc)
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
