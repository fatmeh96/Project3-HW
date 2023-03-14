import inspect
import logging
class BaseClass():
    def getLogger(self):
        logger_name = inspect.stack()[1][3]
        logger=logging.getLogger(logger_name)
        if not logger.handlers:
            fileHandler = logging.FileHandler('logs_report.log',mode='a')
            formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
            logger.setLevel(logging.DEBUG)
        return logger
