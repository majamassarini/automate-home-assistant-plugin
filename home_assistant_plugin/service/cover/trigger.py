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

        for klass in (Open, Closed, Position):
            if klass.check(message):
                triggers.append(klass(message))

        return triggers


class Open(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.cover.trigger.Open.make("cover.blind")
    >>> [event.value for event in trigger.events]
    ['Opened']
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "open",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "open"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.curtain.event.forced.Event.Opened]


class Closed(ChangedState):
    """
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.cover.trigger.Closed.make("cover.blind")
    >>> [event.value for event in trigger.events]
    ['Closed']
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "closed",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "closed"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.curtain.event.forced.Event.Closed]


class Position(ChangedAttribute):
    """
    >>> import home_assistant_plugin
    >>> import json

    >>> message = '''
    ... {"id": 1,
    ...   "type": "event",
    ...   "event": {
    ...     "event_type": "state_changed",
    ...     "data": {"entity_id": "cover.blind",
    ...       "new_state": {"entity_id": "cover.blind",
    ...         "state": "open", "attributes": {"current_position": 42}},
    ...       "old_state": {"entity_id": "cover.blind",
    ...         "state": "open", "attributes": {"current_position": 10}}
    ...     }
    ...   }
    ... }
    ... '''
    >>> trigger = home_assistant_plugin.service.cover.trigger.Position(json.loads(message))
    >>> trigger.attributes["current_position"]
    42
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"current_position": 0},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            if (
                "current_position"
                in message["event"]["data"]["new_state"]["attributes"]
            ):
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self,
        another_description: Description,
        old_state: home.appliance.attribute.mixin.Position,
    ) -> home.appliance.State:
        new_state = super(Position, self).make_new_state_from(
            another_description, old_state
        )
        new_state.position = another_description.message["event"]["data"][
            "new_state"
        ]["attributes"]["current_position"]
        return new_state
