# AioxUI

A lightweight async Python SDK for interacting with XUI panel APIs.

## Features
- Async client based on aiohttp
- Typed models using Pydantic
- Client management (create, update, delete)
- Traffic management utilities
- Inbound attach/detach support

## Installation

```bash
pip install aioxui
```

```bash
git clone https://github.com/DevJavad/aioxui.git
cd aioxui
pip install -e .
```

## Quick Start
```python
import asyncio

from aioxui import XUI

async def main():
    async with XUI(
        base_url="https://your-panel.com/",
        token="YOUR_TOKEN"
    ) as xui:

        client = await xui.client.get("Javad")
        print(client)

        clients = await xui.client.all()
        print(len(clients))

asyncio.run(main())
```

## Example: Create Client
```python
import asyncio
import os

from aioxui import XUI
from aioxui.models import Client
from aioxui.enums import UnitType
from aioxui.utils import DateTime, Storage
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("URL")
token: str = os.getenv("TOKEN")

async def main():
    async with XUI(base_url=url, token=token) as xui:
        client = Client(
            totalGB=Storage.from_unit(10, UnitType.GB),
            expiryTime=DateTime.after(days=30),
            limitIp=3,
            tgId=12345678,  # Telegram user_id
        )

        add = await xui.client.add(inbound_id=[2, 3], client=client)
        print(add.email)
        print(add.sub_id)


asyncio.run(main())
```