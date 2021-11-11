from home_assistant_plugin.service.trigger import Equals


class Factory:

    def __init__(self, setup_triggers):
        self._entity_id_klass = {}
        for trigger in setup_triggers:
            if trigger.entity_id not in self._entity_id_klass:
                self._entity_id_klass[trigger.entity_id] = list()
            self._entity_id_klass[trigger.entity_id].append(trigger.__class__)

    def get_triggers_from(self, message):
        entity_id = None
        triggers = list()

        try:
            entity_id = message["event"]["data"]["entity_id"]
        except (KeyError, TypeError):
            pass

        if entity_id in self._entity_id_klass:
            for klass in self._entity_id_klass[entity_id]:
                triggers.append(klass(message))

        return triggers


class IntMixin:

    @property
    def state(self):
        return int(self._state)


class FloatMixin:

    @property
    def state(self):
        return float(self._state)


class On(Equals):

    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "on",
                    "attributes": {}
                }
            },
            "event_type": "state_changed"
        }
    }


class Off(Equals):

    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "state": "off",
                    "attributes": {}
                }
            },
            "event_type": "state_changed"
        }
    }

