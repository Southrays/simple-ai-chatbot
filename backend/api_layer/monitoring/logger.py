import logging


def setup_logger(name = "SimpleChatbot") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] [%(message)s]")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()