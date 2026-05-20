import copy
import asyncio
import logging
import aiohttp
import json

import home
from home_assistant_plugin.message import Description, Command
from home_assistant_plugin.service.notify.command import Command as Notifier
from home_assistant_plugin import factory


class Gateway(home.protocol.Gateway):

    PROTOCOL = Description.PROTOCOL

    def __init__(self, long_live_token, address="0.0.0.0", port=8123):
        self._session = None
        self._websocket = None
        self._long_live_token = long_live_token
        self._address = address
        self._port = port
        self._setup_triggers = set()
        self._triggers = set()
        self._commands = set()
        self._id = 5

        self.logger = logging.getLogger(__name__)

    def associate_commands(self, descriptions):
        pass

    def associate_triggers(self, descriptions):
        for trigger in descriptions:
            self._setup_triggers.add(trigger)
            self._triggers.add(trigger.entity_id)

    async def run(self, other_tasks):
        wrapped_tasks = self._wrap_tasks(other_tasks)
        trigger_factory = factory.trigger.Factory(self._setup_triggers)
        async with aiohttp.ClientSession() as self._session:
            while True:
                uri = "ws://{}:{}/api/websocket".format(
                    self._address, self._port
                )
                try:
                    async with self._session.ws_connect(
                        uri
                    ) as self._websocket:
                        async for msg in self._websocket:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                self.logger.debug("received: {}".format(data))
                                if data["type"] == "auth_required":
                                    await self._websocket.send_str(
                                        json.dumps(
                                            {
                                                "type": "auth",
                                                "access_token": self._long_live_token,
                                            }
                                        )
                                    )
                                elif data["type"] == "auth_ok":
                                    await self._websocket.send_str(
                                        json.dumps(
                                            {
                                                "id": 1,
                                                "type": "subscribe_events",
                                            }
                                        )
                                    )
                                    await self._websocket.send_str(
                                        json.dumps(
                                            {
                                                "id": 2,
                                                "type": "get_services",
                                            }
                                        )
                                    )
                                elif data["type"] == "result":
                                    if not data["success"]:
                                        self.logger.error(
                                            "received: {}".format(
                                                json.dumps(
                                                    data,
                                                    indent=4,
                                                    sort_keys=True,
                                                )
                                            )
                                        )
                                else:
                                    for task in wrapped_tasks:
                                        triggers = (
                                            trigger_factory.get_triggers_from(
                                                data
                                            )
                                        )
                                        for trigger in triggers:
                                            if (
                                                trigger
                                                and trigger.entity_id
                                                in self._triggers
                                            ):
                                                asyncio.create_task(
                                                    task(trigger),
                                                    name="Home assistant trigger received {}".format(
                                                        str(trigger)
                                                    ),
                                                )
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                self.logger.error(
                                    "received: {}".format(
                                        json.dumps(
                                            data, indent=4, sort_keys=True
                                        )
                                    )
                                )
                except Exception as e:
                    self._websocket = None
                    self.logger.warning(
                        "HA connection failed: %s — retrying in 60 s", e
                    )
                await asyncio.sleep(60)

    async def disconnect(self):
        if self._session:
            await self._session.close()

    async def writer(self, msgs, *args):
        if not self._websocket:
            self.logger.warning(
                "HA writer: not connected, skipping %d msg(s)", len(msgs)
            )
            return
        for msg in msgs:
            if isinstance(msg, Command) or isinstance(msg, Notifier):
                msg_with_id = copy.deepcopy(msg.message)
                msg_with_id["id"] = self._id + 1
                self._id += 1
                await self._websocket.send_str(json.dumps(msg_with_id))
                self.logger.info("written {}".format(msg_with_id))

    @staticmethod
    def make_trigger(trigger):
        return trigger
