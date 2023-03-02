import home
from typing import Union
from home_assistant_plugin.message import LightCommand as Parent


class TurnOn(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.light.command.TurnOn.make("a light")
    >>> msg = cmd.make_msgs_from(off_state, on_state)
    >>> len(msg) and msg[0].service == 'turn_on'
    True
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_on",
        "service_data": {},
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
    ):
        result = []
        if (old_state.is_on != new_state.is_on) and new_state.is_on:
            result = self.execute()
        return result


class TurnOff(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.light.command.TurnOff.make("a light")
    >>> cmd.make_msgs_from(off_state, on_state)
    []
    >>> msg = cmd.make_msgs_from(on_state, off_state)
    >>> len(msg) and msg[0].service == 'turn_off'
    True
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_off",
        "service_data": {},
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
    ):
        result = []
        if (old_state.is_on != new_state.is_on) and not new_state.is_on:
            result = self.execute()
        return result


class Brightness(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.dimmerable.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> new_brightness_state = on_state.next(home.appliance.light.event.brightness.Event(51))
    >>> cmd = home_assistant_plugin.service.light.command.Brightness.make("a light")
    >>> msg = cmd.make_msgs_from(off_state, new_brightness_state)
    >>> len(msg) and msg[0].service == 'turn_on'
    True
    >>> msg[0].message["service_data"]["brightness"] == 130
    True
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_on",
        "service_data": {
            "brightness": 127,  # int [1,255]
        },
        "target": {
            "entity_id": "none",
        }
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Brightness,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Brightness,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["brightness"] = int(
                new_state.brightness * (255 / 100)
            )
            result = self.execute()
        return result


class OffBrightness(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.dimmerable.state.off.State()
    >>> brightness_state = off_state.next(home.appliance.light.event.brightness.Event(51))
    >>> cmd = home_assistant_plugin.service.light.command.OffBrightness.make("a light")
    >>> msg = cmd.make_msgs_from(off_state, brightness_state)
    >>> len(msg) and msg[0].service == 'turn_off'
    True
    >>> msg[0].message["service_data"]["brightness"] == 130
    True
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_off",
        "service_data": {
            "brightness": 127,  # int [1,255]
        },
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Brightness,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Brightness,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["brightness"] = int(
                new_state.brightness * (255 / 100)
            )
            result = self.execute()
        return result


class Temperature(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.hue.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> new_temperature_state = on_state.next(home.appliance.light.event.temperature.Event(3200))
    >>> cmd = home_assistant_plugin.service.light.command.Temperature.make("a light")
    >>> msg = cmd.make_msgs_from(off_state, new_temperature_state)
    >>> len(msg) and msg[0].service == 'turn_on'
    True
    >>> msg[0].message["service_data"]["color_temp"]
    3
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_on",
        "service_data": {
            "color_temp": 1,
        },
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Temperature,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Temperature,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["color_temp"] = int(
                10000 / new_state.temperature
            )
            result = self.execute()
        return result


class OffTemperature(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.hue.state.off.State()
    >>> new_temperature_state = off_state.next(home.appliance.light.event.temperature.Event(3200))
    >>> on_state = off_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.light.command.OffTemperature.make("a light")
    >>> msg = cmd.make_msgs_from(on_state, new_temperature_state)
    >>> len(msg) and msg[0].service == 'turn_off'
    True
    >>> msg[0].message["service_data"]["color_mode"]
    'ColorMode.COLOR_TEMP'
    >>> msg[0].message["service_data"]["color_temp"]
    3
    >>> cmd.make_msgs_from(off_state, on_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_off",
        "service_data": {
            "color_mode": "ColorMode.COLOR_TEMP",
            "color_temp": 1,
        },
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Temperature,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Temperature,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["color_temp"] = int(
                10000 / new_state.temperature
            )
            result = self.execute()
        return result


class HueSaturation(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.hue.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> new_hue_state = on_state.next(home.appliance.light.event.hue.Event(320))
    >>> new_saturation_state = new_hue_state.next(home.appliance.light.event.saturation.Event(80))
    >>> cmd = home_assistant_plugin.service.light.command.HueSaturation.make("a light")
    >>> msg = cmd.make_msgs_from(off_state, new_saturation_state)
    >>> len(msg) and msg[0].service == 'turn_on'
    True
    >>> msg[0].message["service_data"]["hs_color"]
    (320, 80)
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_on",
        "service_data": {"hs_color": (1, 1)},
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Hue,
            home.appliance.attribute.mixin.Saturation,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Hue,
            home.appliance.attribute.mixin.Saturation,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["hs_color"] = (
                new_state.hue,
                new_state.saturation,
            )
            result = self.execute()
        return result


class OffHueSaturation(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.light.indoor.hue.state.off.State()
    >>> on_state = off_state.next(home.appliance.light.indoor.dimmerable.event.forced.Event.On)
    >>> new_hue_state = off_state.next(home.appliance.light.event.hue.Event(320))
    >>> new_saturation_state = new_hue_state.next(home.appliance.light.event.saturation.Event(80))
    >>> cmd = home_assistant_plugin.service.light.command.OffHueSaturation.make("a light")
    >>> msg = cmd.make_msgs_from(on_state, new_saturation_state)
    >>> len(msg) and msg[0].service == 'turn_off'
    True
    >>> msg[0].message["service_data"]["color_mode"]
    'ColorMode.HS'
    >>> msg[0].message["service_data"]["hs_color"]
    (320, 80)
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message = {
        "type": "call_service",
        "domain": "light",
        "service": "turn_off",
        "service_data": {"color_mode": "ColorMode.HS", "hs_color": (1, 1)},
        "target": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Hue,
            home.appliance.attribute.mixin.Saturation,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
            home.appliance.attribute.mixin.Hue,
            home.appliance.attribute.mixin.Saturation,
        ],
    ):
        result = []
        if new_state.is_on:
            self.message["service_data"]["hs_color"] = (
                new_state.hue,
                new_state.saturation,
            )
            result = self.execute()
        return result
