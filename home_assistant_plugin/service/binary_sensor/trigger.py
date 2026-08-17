from home_assistant_plugin.service.sensor import trigger as sensor_trigger


class On(sensor_trigger.On):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.binary_sensor.trigger.On.make(
    ...     "binary_sensor.motion",
    ...     events=[home.event.presence.Event.On],
    ... )
    >>> [event.value for event in trigger.events]
    ['On']
    """


class Off(sensor_trigger.Off):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> trigger = home_assistant_plugin.service.binary_sensor.trigger.Off.make(
    ...     "binary_sensor.motion",
    ...     events=[home.event.presence.Event.Off],
    ... )
    >>> [event.value for event in trigger.events]
    ['Off']
    """
