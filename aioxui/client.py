import logging
from uuid import uuid4

from .models import ClientOutput, Client, Traffic
from .session import Session

logger = logging.getLogger(__name__)


class ClientAPI:
    def __init__(self, session: Session):
        self.session = session

    async def get(self, email: str) -> ClientOutput:
        response = await self.session.request("GET", f"panel/api/clients/get/{email}")
        obj: dict = response["obj"]

        client = ClientOutput.model_validate(obj["client"])
        client.inbound_ids = obj.get("inboundIds", [])
        client.used_traffic = obj.get("usedTraffic", 0)
        client.external_links = obj.get("externalLinks", [])

        return client

    async def all(self) -> list[ClientOutput]:
        response = await self.session.request("GET", "panel/api/clients/list")
        clients: list = []

        for user in response.get("obj", []):
            traffic = Traffic.model_validate(user.get("traffic", {}))

            client = ClientOutput.model_validate(user)
            client.traffic = traffic

            clients.append(client)

        return clients

    async def add(self, inbound_id: int | list[int], client: Client) -> ClientOutput:
        if client.email is None:
            client.email = uuid4().hex[:8]
        if client.uuid is None:
            client.uuid = str(uuid4())
        if client.sub_id is None:
            client.sub_id = uuid4().hex[:16]

        data = {
            "client": client.model_dump(by_alias=True, exclude_none=True),
            "inboundIds": inbound_id if isinstance(inbound_id, list) else [inbound_id],
        }
        email = client.email

        await self.session.request("POST", "panel/api/clients/add", data=data)
        logger.info("Client added successfully: %s", email)
        return await self.get(email)

    async def update(self, client: Client) -> ClientOutput:
        email = client.email
        await self.session.request(
            "POST",
            f"panel/api/clients/update/{email}",
            client.model_dump(by_alias=True, exclude_none=True),
        )
        logger.info("Client updated successfully: %s", email)

        return await self.get(email)

    async def delete(self, email: str, keep_traffic: bool = False) -> None:
        endpoint = f"panel/api/clients/del/{email}"
        if keep_traffic:
            endpoint += "?keepTraffic=1"

        await self.session.request("POST", endpoint)
        logger.info("Client deleted successfully: %s", email)

    async def get_traffic(self, email: str) -> Traffic:
        response = await self.session.request(
            "GET", f"panel/api/clients/traffic/{email}"
        )
        return Traffic.model_validate(response.get("obj", {}))

    async def reset_traffic(self, email: str) -> None:
        await self.session.request("POST", f"panel/api/clients/resetTraffic/{email}")
        logger.info("Successfully reset traffic for client: %s", email)

    async def reset_all_traffics(self) -> None:
        await self.session.request("POST", "panel/api/clients/resetAllTraffics")
        logger.info("Successfully reset traffic for all clients")

    async def update_traffic(self, email: str, upload: int, download: int) -> Traffic:
        await self.session.request(
            "POST",
            f"panel/api/clients/updateTraffic/{email}",
            {"up": upload, "down": download},
        )
        logger.info("Successfully update traffic for client: %s", email)
        return await self.get_traffic(email)

    async def get_configs(self, email: str) -> list[str] | None:
        response = await self.session.request("GET", f"panel/api/clients/links/{email}")
        return response.get("obj", [])

    async def get_ips(self, email: str) -> list[str]:
        response = await self.session.request("POST", f"panel/api/clients/ips/{email}")
        return response.get("obj", [])

    async def clear_ips(self, email: str) -> None:
        await self.session.request("POST", f"panel/api/clients/clearIps/{email}")

    async def get_onlines(self) -> list[str]:
        response = await self.session.request("POST", "panel/api/clients/onlines")
        return response.get("obj", [])

    async def get_onlines_by_guid(self) -> dict:
        response = await self.session.request("POST", "panel/api/clients/onlinesByGuid")
        return response.get("obj", {})

    async def get_last_online(self) -> dict[str, int]:
        response = await self.session.request("POST", "panel/api/clients/lastOnline")
        return response.get("obj", {})

    async def get_active_inbounds(self) -> dict:
        response = await self.session.request(
            "POST", "panel/api/clients/activeInbounds"
        )
        return response.get("obj", {})

    async def attach(self, email: str, inbound_ids: list[int]) -> None:
        await self.session.request(
            "POST", f"panel/api/clients/{email}/attach", {"inboundIds": inbound_ids}
        )
        logger.info("Attached client email=%s to inbound_ids=%s", email, inbound_ids)

    async def delete_depleted(self) -> None:
        await self.session.request("POST", "panel/api/clients/delDepleted")
        logger.info("Deleted all depleted clients")

    async def detach(self, email: str, inbound_ids: list[int]) -> None:
        await self.session.request(
            "POST", f"panel/api/clients/{email}/detach", {"inboundIds": inbound_ids}
        )
        logger.info("Detached client email=%s from inbound_ids=%s", email, inbound_ids)