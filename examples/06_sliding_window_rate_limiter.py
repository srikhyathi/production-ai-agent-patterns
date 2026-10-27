# -*- coding: utf-8 -*-
"""
Production AI Agent Pattern: Sliding Window Rate Limiter.
Prevents webhook flooding and model denial-of-service in autonomous agent endpoints.
"""

import time
from collections import defaultdict, deque
from typing import Dict, Deque, Optional


class SlidingWindowRateLimiter:
    """
    High-precision sliding window timestamp tracker for API gateways and microservice agents.
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, Deque[float]] = defaultdict(deque)

    def is_allowed(self, client_id: str, now: Optional[float] = None) -> bool:
        current_time = now if now is not None else time.time()
        cutoff = current_time - self.window_seconds
        timestamps = self._history[client_id]

        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)
            return True

        return False

    def remaining_quota(self, client_id: str, now: Optional[float] = None) -> int:
        current_time = now if now is not None else time.time()
        cutoff = current_time - self.window_seconds
        timestamps = self._history[client_id]

        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()

        return max(0, self.max_requests - len(timestamps))

    def reset(self, client_id: Optional[str] = None):
        if client_id:
            self._history.pop(client_id, None)
        else:
            self._history.clear()


if __name__ == "__main__":
    limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=10)
    for i in range(7):
        allowed = limiter.is_allowed("agent-client-1")
        print(f"Request {i+1}: Allowed={allowed}, Remaining={limiter.remaining_quota('agent-client-1')}")
