from pydantic import BaseModel, ConfigDict, Field


class ClientFields:
    EMAIL = "email"
    ENABLE = "enable"
    PASSWORD = "password"
    ID = "id"
    INBOUND_ID = "inboundId"
    UP = "up"
    DOWN = "down"
    EXPIRY_TIME = "expiryTime"
    TOTAL = "total"
    RESET = "reset"
    FLOW = "flow"
    METHOD = "method"
    LIMIT_IP = "limitIp"
    SUB_ID = "subId"
    COMMENT = "comment"
    TG_ID = "tgId"
    TOTAL_GB = "totalGB"
    UUID = "uuid"
    AUTH = "auth"
    SECURITY = "security"
    GROUP = "group"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    REVERSE = "reverse"
    INBOUND_IDS = "inboundIds"
    USED_TRAFFIC = "usedTraffic"
    LAST_ONLINE = "lastOnline"
    PRIVATE_KEY = "privateKey"
    PUBLIC_KEY = "publicKey"
    ALLOWED_IPS = "allowedIPs"
    PRE_SHARED_KEY = "preSharedKey"
    KEEP_ALIVE = "keepAlive"
    EXTERNAL_LINKS = "externalLinks"
    START_AFTER_FIRST_USE = "startAfterFirstUse"


class Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    def __str__(self):
        return self.model_dump_json(indent=4, ensure_ascii=True, exclude_none=True)

class Traffic(Base):
    id: int
    upload: int = Field(default=0, alias=ClientFields.UP)
    download: int = Field(default=0, alias=ClientFields.DOWN)
    total: int
    last_online: int = Field(default=None, alias=ClientFields.LAST_ONLINE)
    
class Client(Base):
    email: str | None = None
    enable: bool = True
    uuid: str | None = None
    sub_id: str | None = Field(default=None, alias=ClientFields.SUB_ID)
    traffic_limit: int = Field(default=0, alias=ClientFields.TOTAL_GB)
    time_limit: int = Field(default=0, alias=ClientFields.EXPIRY_TIME)
    ip_limit: int = Field(default=0, alias=ClientFields.LIMIT_IP)
    telegram_id: int = Field(default=None, alias=ClientFields.TG_ID)
    comment: str | None = None
    group: str | None = None
    start_after_first_use: bool = Field(
        default=False, alias=ClientFields.START_AFTER_FIRST_USE
    )


class ClientOutput(Base):
    id: int
    email: str
    sub_id: str | None = Field(default=None, alias=ClientFields.SUB_ID)
    uuid: str | None = None
    password: str
    auth: str
    flow: str
    security: str
    private_key: str = Field(default=None, alias=ClientFields.PRIVATE_KEY)
    public_key: str = Field(default=None, alias=ClientFields.PUBLIC_KEY)
    allowed_ips: str = Field(default=None, alias=ClientFields.ALLOWED_IPS)
    pre_shared_key: str = Field(default=None, alias=ClientFields.PRE_SHARED_KEY)
    keep_alive: int = Field(default=None, alias=ClientFields.KEEP_ALIVE)
    ip_limit: int = Field(default=None, alias=ClientFields.LIMIT_IP)
    traffic_limit: int = Field(default=None, alias=ClientFields.TOTAL_GB)
    time_limit: int = Field(default=None, alias=ClientFields.EXPIRY_TIME)
    enable: bool
    telegram_id: int = Field(default=None, alias=ClientFields.TG_ID)
    group: str
    comment: str
    reset: int
    created_at: int = Field(default=None, alias=ClientFields.CREATED_AT)
    updated_at: int = Field(default=None, alias=ClientFields.UPDATED_AT)
    reverse: dict | None = None
    external_links: list = Field(default=None, alias=ClientFields.EXTERNAL_LINKS)
    inbound_ids: list[int] | None = Field(default=None, alias=ClientFields.INBOUND_IDS)
    used_traffic: int = Field(default=0, alias=ClientFields.USED_TRAFFIC)
    traffic: Traffic | None = None