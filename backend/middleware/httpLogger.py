import logging
import time
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from colorama import Fore, Style

logger = logging.getLogger("http_logger")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_time = datetime.utcnow().isoformat()

        response = await call_next(request)
        duration = (time.time() - start_time) * 1000

        method_color = f"{Fore.CYAN}{request.method}{Style.RESET_ALL}"
        path_color = f"{Fore.YELLOW}{request.url.path}{Style.RESET_ALL}"
        status_color = (
            Fore.GREEN
            if response.status_code < 300
            else Fore.YELLOW if response.status_code < 400 else Fore.RED
        )
        status_text = f"{status_color}{response.status_code}{Style.RESET_ALL}"

        log_line = (
            f"[{request_time}] {method_color} {path_color} "
            f"-> {status_text} ({duration:.2f}ms)"
        )

        print(log_line)

        return response
