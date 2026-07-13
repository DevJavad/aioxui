import logging

from .client import ClientAPI
from .session import Session

logger = logging.getLogger(__name__)


class XUI:
    def __init__(
        self,
        base_url: str,
        token: str,
        verify_ssl: bool = False,
        timeout: float = 10.0,
    ):
        self.base_url = base_url
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout

        self.session: Session | None = None

        self.client: ClientAPI | None = None

    async def start(self) -> None:
        self.session = Session(self.base_url, self.token, self.verify_ssl, self.timeout)
        await self.session.create_session()

        if self.client is None:
            self.client = ClientAPI(self.session)

        logger.info("Start XUI service")

    async def stop(self) -> None:
        await self.session.close_session()
        logger.info("Stop XUI service")

    async def __aenter__(self) -> "XUI":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()