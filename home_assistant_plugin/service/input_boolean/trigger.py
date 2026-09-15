from home_assistant_plugin.service.sensor import trigger as sensor_trigger


class On(sensor_trigger.On):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.input_boolean.trigger.On.make(
    ...     "input_boolean.movie_scene",
    ...     events=[home.event.presence.Event.On],
    ... )
    >>> [event.value for event in trigger.events]
    ['On']
    """


class Off(sensor_trigger.Off):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.input_boolean.trigger.Off.make(
    ...     "input_boolean.movie_scene",
    ...     events=[home.event.presence.Event.Off],
    ... )
    >>> [event.value for event in trigger.events]
    ['Off']
    """
