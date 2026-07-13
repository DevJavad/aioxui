import logging
from typing import Literal, Any

from aiohttp import ClientSession, TCPConnector, ClientTimeout, ClientError

from .errors import XUIAuthError, XUINotFoundError, XUIRequestError

logger = logging.getLogger(__name__)


class Session:
    def __init__(
        self,
        base_url: str,
        token: str,
        verify_ssl: bool = True,
        timeout: float = 10.0,
    ):
        self.base_url = base_url.rstrip("/") + "/"
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout

        self.session: ClientSession | None = None

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    @property
    def is_connected(self) -> bool:
        return self.session is not None and not self.session.closed

    async def create_session(self) -> None:
        if self.is_connected:
            return

        connector = TCPConnector(ssl=self.verify_ssl)
        timeout = ClientTimeout(total=self.timeout)

        self.session = ClientSession(
            base_url=self.base_url,
            headers=self.headers,
            connector=connector,
            timeout=timeout,
        )

    async def close_session(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self) -> "Session":
        await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close_session()

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
        retry: int = 1,
    ) -> dict[str, Any]:

        await self.create_session()

        url = endpoint.lstrip("/")
        logger.debug("HTTP %s %s", method, url)

        last_error: Exception | None = None

        for attempt in range(retry + 1):
            try:
                async with self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                ) as response:

                    if response.status == 401:
                        raise XUIAuthError("Invalid XUI token")

                    if response.status == 404:
                        raise XUINotFoundError(f"Endpoint not found: {endpoint}")

                    if response.status >= 400:
                        text = await response.text()
                        raise XUIRequestError(f"HTTP {response.status}: {text}")

                    try:
                        result = await response.json()
                    except Exception:
                        text = await response.text()
                        raise XUIRequestError(f"Invalid JSON response: {text}")

                    logger.debug("Response: %s", result)

                    if isinstance(result, dict) and not result.get("success", True):
                        raise XUIRequestError(result.get("msg", "Unknown API error"))

                    return result

            except ClientError as e:
                last_error = e
                if attempt < retry:
                    continue
                raise XUIRequestError(f"Client error: {e}") from e

            except TimeoutError as e:
                last_error = e
                if attempt < retry:
                    continue
                raise XUIRequestError("Request timed out") from e

        raise XUIRequestError(f"Request failed: {last_error}")