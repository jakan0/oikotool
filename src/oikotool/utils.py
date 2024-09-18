# SPDX-License-Identifier: MIT

from typing import Any, Callable, Optional

import requests
from tenacity import WrappedFn, retry, stop_after_attempt, wait_exponential_jitter


class HttpUtils:
    @staticmethod
    def _create_retry_decorator() -> Callable[[WrappedFn], WrappedFn]:
        return retry(
            reraise=True,
            wait=wait_exponential_jitter(initial=3, jitter=2),
            stop=stop_after_attempt(5),
        )

    @staticmethod
    def _send_http_request(method: str, url: str, **kwargs: Any) -> requests.Response:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    @_create_retry_decorator()
    def get_with_retry(
        url: str,
        headers: Optional[dict[str, str]] = None,
        timeout: int = 30,
        stream: bool = False,
        **kwargs: Any,
    ) -> requests.Response:
        return HttpUtils._send_http_request(
            "GET", url, headers=headers, timeout=timeout, stream=stream, **kwargs
        )

    @staticmethod
    @_create_retry_decorator()
    def post_with_retry(
        url: str,
        data: Any,
        headers: Optional[dict[str, str]] = None,
        timeout: int = 30,
        **kwargs: Any,
    ) -> requests.Response:
        return HttpUtils._send_http_request(
            "POST", url, data=data, headers=headers, timeout=timeout, **kwargs
        )
