from typing import ClassVar, Any

from home_assistant_plugin.message import Description
from home_assistant_plugin.service.trigger import ChangedState


class Factory:
    def __init__(self, setup_triggers):
        self._setup_triggers = setup_triggers

    def get_triggers_from(self, message):
        triggers = list()

        if Pressed.check(message):
            triggers.append(Pressed(message))

        return triggers


class Pressed(ChangedState):
    """
    HA bumps an ``input_button``'s state to the press timestamp on every
    press, so there's no fixed ``state`` value to match against (unlike
    ``on``/``off``); any state change counts as a press.

    >>> import home
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.input_button.trigger.Pressed.make(
    ...     "input_button.scene",
    ...     events=[home.event.presence.Event.On],
    ... )
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
                    "state": "none",
                    "attributes": {},
                },
            },
            "event_type": "state_changed",
        },
    }

    def check(message: Description):  # type: ignore[misc]
        try:
            return (
                message["event"]["event_type"] == "state_changed"
                and message["event"]["data"]["new_state"]["state"] is not None
            )
        except (KeyError, TypeError):
            pass
        return False

    def __eq__(self, other):
        return super(ChangedState, self).__eq__(other)

    def __hash__(self):
        return super(ChangedState, self).__hash__()

    def __str__(self, *args, **kwargs):
        return "Triggered entity {} pressed".format(self.entity_id)

    def is_triggered(self, another_description):
        if super(ChangedState, self).is_triggered(another_description):
            other = self.__class__(another_description.message)
            if self.entity_id == other.entity_id:
                if other.state != other._old_state:
                    self._logger.info(
                        "triggered {}".format(another_description)
                    )
                    return True
        return False
