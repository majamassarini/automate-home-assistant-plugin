from typing import Union

import home
from home_assistant_plugin.message import Description
from home_assistant_plugin.service.trigger import ChangedState, ChangedAttribute


class Factory:
    def __init__(self, setup_triggers):
        self._setup_triggers = setup_triggers

    def get_triggers_from(self, message):
        state = None
        triggers = list()

        for klass in (On, Off, Brightness, Temperature, HueSaturation):
            if klass.check(message):
                triggers.append(klass(message))

        return triggers


class On(ChangedState):
    Message = {
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

    def check(message: Description):
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "on"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.light.indoor.dimmerable.event.forced.Event.On]


class Off(ChangedState):
    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {"entity_id": "none", "state": "off", "attributes": {}},
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):
        try:
            state = message["event"]["data"]["new_state"]["state"]
            return state == "off"
        except (KeyError, TypeError):
            pass
        return False

    DEFAULT_EVENTS = [home.appliance.light.indoor.dimmerable.event.forced.Event.Off]


class Brightness(ChangedAttribute):
    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"brightness": "0"},
                },
            },
            "event_type": "state_changed",
        },
    }
    
    def check(message: Description):
        try:
            if "brightness" in message["event"]["data"]["new_state"]["attributes"]:
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self, another_description: Description, old_state: home.appliance.attribute.mixin.Brightness
    ) -> home.appliance.State:
        new_state = super(Brightness, self).make_new_state_from(
            another_description, old_state
        )
        new_state.brightness = another_description.message["event"]["data"]["new_state"]["attributes"]["brightness"]
        return new_state


class Brightness(ChangedAttribute):
    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"brightness": "0"},
                },
            },
            "event_type": "state_changed",
        },
    }
    
    def check(message: Description):
        try:
            if "brightness" in message["event"]["data"]["new_state"]["attributes"]:
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self, another_description: Description, old_state: home.appliance.attribute.mixin.Brightness
    ) -> home.appliance.State:
        new_state = super(Brightness, self).make_new_state_from(
            another_description, old_state
        )
        new_state.brightness = int(another_description.message["event"]["data"]["new_state"]["attributes"]["brightness"] * (100 / 255))
        return new_state


class Temperature(ChangedAttribute):
    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"color_temp": 1,},
                },
            },
            "event_type": "state_changed",
        },
    }
    
    def check(message: Description):
        try:
            if "color_temp" in message["event"]["data"]["new_state"]["attributes"]:
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self, another_description: Description, old_state: home.appliance.attribute.mixin.Temperature
    ) -> home.appliance.State:
        new_state = super(Temperature, self).make_new_state_from(
            another_description, old_state
        )
        new_state.temperature = another_description.message["event"]["data"]["new_state"]["attributes"]["color_temp"] * 10000
        return new_state


class HueSaturation(ChangedAttribute):
    Message = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "none",
                "new_state": {
                    "entity_id": "none",
                    "attributes": {"hs_color": (1, 1),},
                },
            },
            "event_type": "state_changed",
        },
    }
    
    def check(message: Description):
        try:
            if "hs_color" in message["event"]["data"]["new_state"]["attributes"]:
                return True
        except (KeyError, TypeError):
            pass
        return False

    def make_new_state_from(
        self, another_description: Description, old_state: Union[home.appliance.attribute.mixin.Hue, home.appliance.attribute.mixin.Saturation]
    ) -> home.appliance.State:
        new_state = super(HueSaturation, self).make_new_state_from(
            another_description, old_state
        )
        new_state.hue = another_description.message["event"]["data"]["new_state"]["attributes"]["hs_color"][0]
        new_state.saturation = another_description.message["event"]["data"]["new_state"]["attributes"]["hs_color"][1]
        return new_state









