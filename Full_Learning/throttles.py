from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled
import time

VISIT_RECORD = {}
BLOCKED_IPS = {}

class MillisecondThrottle(BaseThrottle):
    def allow_request(self, request, view):
        ip = self.get_ident(request)
        now = time.time()

        unblock_time = BLOCKED_IPS.get(ip)
        if unblock_time and now < unblock_time:
            raise Throttled(detail="Request blocked due to too many requests. Try again later.",
                            wait=unblock_time - now)

        request_times = VISIT_RECORD.get(ip, [])
        request_times = [t for t in request_times if now - t < 0.04]

        if len(request_times) >= 1:
            BLOCKED_IPS[ip] = now + 10
            VISIT_RECORD[ip] = []
            raise Throttled(detail="Too many requests in a short time. Blocked for 10 seconds.",
                            wait=10)

        request_times.append(now)
        VISIT_RECORD[ip] = request_times

        return True

    def wait(self):
        # Default wait time if needed
        return 10
