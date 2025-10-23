import logging
from logging.handlers import RotatingFileHandler
import os
from colorama import Fore, Style, init

init(autoreset=True)

os.makedirs("logs", exist_ok=True)


class ColorFormatter(logging.Formatter):
    """Formatter with colored log levels and uniform [time] [LEVEL] message output."""

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        log_fmt = f"[%(asctime)s] [{color}%(levelname)s{reset}] %(message)s"
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger(name: str = "app") -> logging.Logger:
    """Creates a logger with rotating file and colored console output."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    console_handler.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = get_logger("app")
