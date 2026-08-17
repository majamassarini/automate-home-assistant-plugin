import home
from typing import Union, ClassVar, Any
from home_assistant_plugin.message import Command as Parent


class SetTemperature(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.thermostat.presence.state.off.State()
    >>> on_state = off_state.next(home.appliance.thermostat.presence.event.forced.Event.On)
    >>> new_setpoint_state = on_state.next(home.appliance.thermostat.presence.event.setpoint.Event(21.5))
    >>> cmd = home_assistant_plugin.service.climate.command.SetTemperature.make("a thermostat")
    >>> msg = cmd.make_msgs_from(on_state, new_setpoint_state)
    >>> msg[0].service
    'set_temperature'
    >>> msg[0].message["service_data"]["temperature"]
    21.5
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "climate",
        "service": "set_temperature",
        "service_data": {
            "entity_id": "none",
            "temperature": 0,
        },
    }

    def make_msgs_from(
        self,
        old_state: home.appliance.attribute.mixin.Setpoint,
        new_state: home.appliance.attribute.mixin.Setpoint,
    ):
        self.message["service_data"]["temperature"] = new_state.setpoint
        result = self.execute()
        return result


class SetHvacMode(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.thermostat.presence.state.off.State()
    >>> on_state = off_state.next(home.appliance.thermostat.presence.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.climate.command.SetHvacMode.make("a thermostat")
    >>> msg = cmd.make_msgs_from(off_state, on_state)
    >>> len(msg) and msg[0].service == 'set_hvac_mode'
    True
    >>> msg[0].message["service_data"]["hvac_mode"]
    'heat'
    >>> msg = cmd.make_msgs_from(on_state, off_state)
    >>> msg[0].message["service_data"]["hvac_mode"]
    'off'
    >>> cmd.make_msgs_from(on_state, on_state)
    []
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "climate",
        "service": "set_hvac_mode",
        "service_data": {
            "entity_id": "none",
            "hvac_mode": "off",
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
        if old_state.is_on != new_state.is_on:
            self.message["service_data"]["hvac_mode"] = (
                "heat" if new_state.is_on else "off"
            )
            result = self.execute()
        return result
