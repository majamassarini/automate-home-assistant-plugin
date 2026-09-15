from typing import ClassVar, Any

import home
from home_assistant_plugin.message import Description
from home_assistant_plugin.service.trigger import ChangedState


class Factory:
    def __init__(self, setup_triggers):
        self._setup_triggers = setup_triggers

    def get_triggers_from(self, message):
        triggers = list()

        for klass in (On, Off):
            if klass.check(message):
                triggers.append(klass(message))

        return triggers


class On(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.switch.trigger.On.make("switch.plug")
    >>> [event.value for event in trigger.events]
    ['On']
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "on",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "on"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.socket.event.forced.Event.On]


class Off(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.switch.trigger.Off.make("switch.plug")
    >>> [event.value for event in trigger.events]
    ['Off']
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "off",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "off"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.socket.event.forced.Event.Off]
