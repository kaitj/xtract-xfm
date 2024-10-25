"""Helper utility functions."""

import logging


def setup_logger(
    level: int | None = None,
    debug: bool = False,
) -> logging.Logger:
    """Setup logging function."""
    logger = logging.getLogger(__package__)

    if debug:
        level = logging.DEBUG
    else:
        match level:
            case 0:
                level = logging.CRITICAL
            case 1:
                level = logging.ERROR
            case 2:
                level = logging.WARNING
            case _:
                level = logging.INFO

    if not logger.hasHandlers():
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("[%(levelname).1s] %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
