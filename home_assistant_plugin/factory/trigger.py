from home_assistant_plugin import service


class Factory:
    """
    A factory which builds Triggers from Home Assistant messages received through the websocket API
    """

    def __init__(self, setup_triggers):
        """
        :param static_triggers: Triggers built at startup (decided by the configuration),
        which helps to evaluate new bus messages and map them in triggers
        """
        self._setup_triggers = setup_triggers
        self._factories = list()
        self._factories.append(service.media_player.trigger.Factory(setup_triggers))
        self._factories.append(service.sensor.trigger.Factory(setup_triggers))

    def get_triggers_from(self, message):
        triggers = list()
        for factory in self._factories:
            triggers.extend(factory.get_triggers_from(message))
        return triggers
