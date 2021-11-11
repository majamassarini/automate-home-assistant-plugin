import copy
from home_assistant_plugin.message import Command as Parent


class Play(Parent):

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "media_play",
        "service_data": {
            "entity_id": "none"
        }
    }

    def make_msgs_from(self, old_state, new_state):
        result = []
        if (old_state.is_on != new_state.is_on) and new_state.is_on:
            result = self.execute()
        return result


class Pause(Parent):

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "media_pause",
        "service_data": {
            "entity_id": "none"
        }
    }

    def make_msgs_from(self, old_state, new_state):
        result = []
        if (old_state.is_on != new_state.is_on) and not new_state.is_on:
            result = self.execute()
        return result


class VolumeSet(Parent):

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "volume_set",
        "service_data": {
            "entity_id": "none",
            "volume_level": 0.1  # float between [0,1]
        }
    }

    def make_msgs_from(self, old_state, new_state):
        result = self.execute()
        return result


class ShuffleSet(Parent):

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "shuffle_set",
        "service_data": {
            "entity_id": "none",
            "shuffle": True
        }
    }

    def make_msgs_from(self, old_state, new_state):
        result = self.execute()
        return result


class SelectSource(Parent):

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "select_source",
        "service_data": {
            "entity_id": "none",
            "source": "none"  # a name in the sonos queue
        }
    }

    def make_msgs_from(self, old_state, new_state):
        result = self.execute()
        return result

    @classmethod
    def make(cls, entity_id, source):
        message = copy.deepcopy(cls.Message)
        message["service_data"]["entity_id"] = entity_id
        message["service_data"]["source"] = source
        return cls(message)
