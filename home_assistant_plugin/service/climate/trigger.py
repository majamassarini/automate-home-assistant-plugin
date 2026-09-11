from typing import ClassVar, Any

import home
from home_assistant_plugin.message import Description
from home_assistant_plugin.service.trigger import (
    ChangedState,
    ChangedAttribute,
)


class Factory:
    def __init__(self, setup_triggers):
        self._setup_triggers = setup_triggers

    def get_triggers_from(self, message):
        triggers = list()

        for klass in (Heating, Idle, Setpoint):
            if klass.check(message):
                triggers.append(klass(message))

        return triggers


class Heating(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.climate.trigger.Heating.make("climate.living_room")
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
                    "attributes": {"hvac_action": "heating"},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            attributes = message["event"]["data"]["new_state"]["attributes"]
            return attributes.get("hvac_action") == "heating"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.thermostat.presence.event.forced.Event.On]


class Idle(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.climate.trigger.Idle.make("climate.living_room")
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
                    "attributes": {"hvac_action": "idle"},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            attributes = message["event"]["data"]["new_state"]["attributes"]
            return attributes.get("hvac_action") == "idle"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [
        home.appliance.thermostat.presence.event.forced.Event.Off
    ]


class Setpoint(ChangedAttribute):
    """
    >>> import home_assistant_plugin
    >>> import json

    >>> message = '''
    ... {"id": 1,
    ...   "type": "event",
    ...   "event": {
    ...     "event_type": "state_changed",
    ...     "data": {"entity_id": "climate.living_room",
    ...       "new_state": {"entity_id": "climate.living_room",
    ...         "state": "heat", "attributes": {"temperature": 21.5}},
    ...       "old_state": {"entity_id": "climate.living_room",
    ...         "state": "heat", "attributes": {"temperature": 20.0}}
    ...     }
    ...   }
    ... }
    ... '''
    >>> trigger = home_assistant_plugin.service.climate.trigger.Setpoint(json.loads(message))
    >>> trigger.attributes["temperature"]
    21.5
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"temperature": 0},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            if (
                "temperature"
                in message["event"]["data"]["new_state"]["attributes"]
            ):
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self,
        another_description: Description,
        old_state: home.appliance.attribute.mixin.Setpoint,
    ) -> home.appliance.State:
        new_state = super(Setpoint, self).make_new_state_from(
            another_description, old_state
        )
        new_state.setpoint = another_description.message["event"]["data"][
            "new_state"
        ]["attributes"]["temperature"]
        return new_state
