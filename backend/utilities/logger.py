import logging
import os
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

init(autoreset=True)

logging.raiseExceptions = False
os.makedirs("logs", exist_ok=True)


class ColorFormatter(logging.Formatter):
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


class SafeRotatingFileHandler(RotatingFileHandler):
    """Fail-safe file handler that never crashes the app."""

    def emit(self, record):
        try:
            super().emit(record)
        except Exception:
            self.acquire()
            try:
                self.close()
                self.disabled = True
            finally:
                self.release()


def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        try:
            file_handler = SafeRotatingFileHandler(
                "logs/app.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",
                delay=True,  # important
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] %(message)s",
                    "%Y-%m-%d %H:%M:%S",
                )
            )
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
        except Exception:
            pass

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

    return logger


logger = get_logger("app")
