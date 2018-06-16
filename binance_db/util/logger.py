import logging

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def __init__(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()

        log_format = "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s"
        time_format = "%Y-%m-%d %H:%M:%S %z"
        formatter = logging.Formatter(log_format, time_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

    # TODO: telegram messages
    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warn(msg)
    
    def error(self, msg):
        self.logger.error(msg)
