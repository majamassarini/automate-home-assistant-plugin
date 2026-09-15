import home
from typing import Union, ClassVar, Any
from home_assistant_plugin.message import Command as Parent


class TurnOn(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> off_state = home.appliance.socket.energy_guard.state.off.State()
    >>> on_state = off_state.next(home.appliance.socket.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.switch.command.TurnOn.make("a switch")
    >>> msg = cmd.make_msgs_from(off_state, on_state)
    >>> len(msg) and msg[0].service == 'turn_on'
    True
    >>> cmd.make_msgs_from(on_state, off_state)
    []
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "switch",
        "service": "turn_on",
        "service_data": {
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

    >>> off_state = home.appliance.socket.energy_guard.state.off.State()
    >>> on_state = off_state.next(home.appliance.socket.event.forced.Event.On)
    >>> cmd = home_assistant_plugin.service.switch.command.TurnOff.make("a switch")
    >>> cmd.make_msgs_from(off_state, on_state)
    []
    >>> msg = cmd.make_msgs_from(on_state, off_state)
    >>> len(msg) and msg[0].service == 'turn_off'
    True
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "switch",
        "service": "turn_off",
        "service_data": {
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
