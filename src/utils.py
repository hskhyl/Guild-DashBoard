# src/utils.py
import datetime
import threading
import time
from functools import wraps


def get_previous_date():
    """어제 날짜를 YYYY-MM-DD 형식으로 반환"""
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


class GlobalRateLimiter:
    """
    전역 레이트 리미터 클래스: 전체 API 호출 횟수를 초당 max_per_second 이하로 제한.
    """

    def __init__(self, max_per_second):
        self.max_per_second = max_per_second
        self.min_interval = 1.0 / max_per_second
        self.last_call_time = 0.0
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call_time
            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                time.sleep(wait_time)
            self.last_call_time = time.time()


# 전역 레이트 리미터 인스턴스 (초당 5건 제한)
global_rate_limiter = GlobalRateLimiter(4)


def global_rate_limit(func):
    """
    데코레이터: 함수 호출 전에 global_rate_limiter.wait()를 호출하여 전체 호출 속도를 제한함.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        global_rate_limiter.wait()
        return func(*args, **kwargs)

    return wrapper
