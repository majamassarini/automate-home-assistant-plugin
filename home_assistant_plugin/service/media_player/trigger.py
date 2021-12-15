import home
from home_assistant_plugin.service.trigger import Equals


class Factory:
    def __init__(self, setup_triggers):
        self._setup_triggers = setup_triggers

    def get_triggers_from(self, message):
        state = None
        triggers = list()

        try:
            state = message["event"]["data"]["new_state"]["state"]
        except (KeyError, TypeError):
            pass

        if state == "playing":
            triggers.append(Playing(message))

        if state == "paused":
            triggers.append(Paused(message))

        return triggers


class Playing(Equals):

    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "playing",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    DEFAULT_EVENTS = [home.appliance.sound.player.event.forced.Event.On]


class Paused(Equals):

    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {"entity_id": "none", "state": "paused", "attributes": {}},
            },
            "event_type": "state_changed",
        },
    }

    DEFAULT_EVENTS = [home.appliance.sound.player.event.forced.Event.Off]
