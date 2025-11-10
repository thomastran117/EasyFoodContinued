from config.celeryConfig import celery_app
from utilities.logger import logger
import time
import threading


class CeleryHealth:
    """Singleton health monitor for Celery broker + workers."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._last_check = 0
        self._cached_status = False
        self._cache_ttl = 10
        self._lock = threading.Lock()

    def check(self, force=False) -> bool:
        """Ping Celery (cached for a short TTL)."""
        with self._lock:
            now = time.time()
            if not force and (now - self._last_check) < self._cache_ttl:
                return self._cached_status

            try:
                ping = celery_app.control.ping(timeout=1.5)
                alive = bool(ping)
                self._cached_status = alive
                self._last_check = now
                if alive:
                    logger.debug("[Health] Celery workers online.")
                else:
                    logger.warning("[Health] No Celery workers responded.")
                return alive
            except Exception as e:
                logger.error(f"[Health] Celery broker unavailable: {e}")
                self._cached_status = False
                self._last_check = now
                return False
