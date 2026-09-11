import home
from typing import Union, ClassVar, Any
from home_assistant_plugin.message import Command as Parent


class OpenCover(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> closed_state = home.appliance.curtain.indoor.blackout.state.closed.State()
    >>> open_state = closed_state.next(home.appliance.curtain.event.forced.Event.Opened)
    >>> cmd = home_assistant_plugin.service.cover.command.OpenCover.make("a cover")
    >>> msg = cmd.make_msgs_from(closed_state, open_state)
    >>> len(msg) and msg[0].service == 'open_cover'
    True
    >>> cmd.make_msgs_from(open_state, closed_state)
    []
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "cover",
        "service": "open_cover",
        "service_data": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOpened,
            home.appliance.attribute.mixin.IsClosed,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOpened,
            home.appliance.attribute.mixin.IsClosed,
        ],
    ):
        result = []
        if (
            old_state.is_opened != new_state.is_opened
        ) and new_state.is_opened:
            result = self.execute()
        return result


class CloseCover(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> closed_state = home.appliance.curtain.indoor.blackout.state.closed.State()
    >>> open_state = closed_state.next(home.appliance.curtain.event.forced.Event.Opened)
    >>> cmd = home_assistant_plugin.service.cover.command.CloseCover.make("a cover")
    >>> cmd.make_msgs_from(closed_state, open_state)
    []
    >>> msg = cmd.make_msgs_from(open_state, closed_state)
    >>> len(msg) and msg[0].service == 'close_cover'
    True
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "cover",
        "service": "close_cover",
        "service_data": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: Union[
            home.appliance.attribute.mixin.IsOpened,
            home.appliance.attribute.mixin.IsClosed,
        ],
        new_state: Union[
            home.appliance.attribute.mixin.IsOpened,
            home.appliance.attribute.mixin.IsClosed,
        ],
    ):
        result = []
        if (
            old_state.is_opened != new_state.is_opened
        ) and not new_state.is_opened:
            result = self.execute()
        return result


class SetPosition(Parent):
    """
    No automate-home curtain state mixes in
    ``home.appliance.attribute.mixin.Position`` yet, so this doctest stands
    a minimal state in for one to demonstrate the round trip.

    >>> import home
    >>> import home_assistant_plugin

    >>> class FakeCoverState(home.appliance.attribute.mixin.Position):
    ...     def __init__(self, position):
    ...         self._position = position
    ...     @property
    ...     def position(self):
    ...         return self._position

    >>> cmd = home_assistant_plugin.service.cover.command.SetPosition.make("a cover")
    >>> msg = cmd.make_msgs_from(FakeCoverState(10), FakeCoverState(42))
    >>> len(msg) and msg[0].service == 'set_cover_position'
    True
    >>> msg[0].message["service_data"]["position"]
    42
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "cover",
        "service": "set_cover_position",
        "service_data": {
            "entity_id": "none",
            "position": 0,  # int [0,100]
        },
    }

    def make_msgs_from(
        self,
        old_state: home.appliance.attribute.mixin.Position,
        new_state: home.appliance.attribute.mixin.Position,
    ):
        self.message["service_data"]["position"] = new_state.position
        result = self.execute()
        return result


class StopCover(Parent):
    """
    No automate-home curtain state mixes in
    ``home.appliance.attribute.mixin.IsStopped`` yet, so this doctest stands
    a minimal state in for one to demonstrate the round trip.

    >>> import home
    >>> import home_assistant_plugin

    >>> class FakeMovingState(home.appliance.attribute.mixin.IsNotStopped):
    ...     pass
    >>> class FakeStoppedState(home.appliance.attribute.mixin.IsStopped):
    ...     pass

    >>> cmd = home_assistant_plugin.service.cover.command.StopCover.make("a cover")
    >>> msg = cmd.make_msgs_from(FakeMovingState(), FakeStoppedState())
    >>> len(msg) and msg[0].service == 'stop_cover'
    True
    >>> cmd.make_msgs_from(FakeStoppedState(), FakeMovingState())
    []
    """

    Message: ClassVar[dict[str, Any]] = {
        "type": "call_service",
        "domain": "cover",
        "service": "stop_cover",
        "service_data": {
            "entity_id": "none",
        },
    }

    def make_msgs_from(
        self,
        old_state: home.appliance.attribute.mixin.IsStopped,
        new_state: home.appliance.attribute.mixin.IsStopped,
    ):
        result = []
        if new_state.is_stopped:
            result = self.execute()
        return result
