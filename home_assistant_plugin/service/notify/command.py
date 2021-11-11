import copy

import home
from home_assistant_plugin.message import Description


class Command(Description, home.protocol.Command):
    """
    >>> import json
    >>> command_data = '''
    ... {
    ...   "type": "call_service",
    ...   "domain": "notify",
    ...   "service": "notify",
    ...   "service_data": {
    ...     "message": "socket has been detached"
    ...   }
    ... }
    ... '''
    >>> command_data = json.loads(command_data)
    >>> command = Command(command_data)
    >>> command.execute()
    [Command: domain 'notify', service 'notify', message 'socket has been detached', title '', target [], other data {}]
    """

    Message = {"type": "call_service",
               "domain": "none",
               "service": "none",
               "service_data": {
                   "message": "none",
                   "title": "none",
                   "target": [],
                   "data": {}
               }
               }

    def __init__(self, message):
        super(Command, self).__init__(message)
        if message["type"] == self.Message["type"]:
            self._domain = message["domain"]
            self._service = message["service"]
            self._notify_message = message["service_data"]["message"]
            if "title" in message["service_data"]:
                self._title = message["service_data"]["title"]
            else:
                self._title = ""
            if "target" in message["service_data"]:
                self._target = message["service_data"]["target"]
            else:
                self._target = []
            if "data" in message["service_data"]:
                self._data = message["service_data"]["data"]
            else:
                self._data = {}
        else:
            raise AttributeError("Given message ({}) is not a command message"
                                 "it should be of type \"event\"".format(message))

    def __eq__(self, other):
        if super(Command, self).__eq__(other):
            if self.notify_message == other.notify_message and \
                    self.title == other.title and \
                    self.domain == other.domain and \
                    self.service == other.service:
                return True
        return False

    def __hash__(self):
        return hash("{}{}{}{}{}".format(super(Command, self).__hash__(),
                    self.domain,
                    self.service,
                    self.message,
                    self.title))
    
    @property
    def domain(self):
        return self._domain

    @property
    def service(self):
        return self._service

    @property
    def notify_message(self):
        return self._notify_message

    @property
    def title(self):
        return self._title
    
    def execute(self):
        self._logger.info("execute {}".format(self.message))
        return [self]

    def make_msgs_from(self, old_state, new_state):
        return []

    @classmethod
    def make(cls, message: str, title: str, target: list, data: dict) -> 'Command':
        msg = copy.deepcopy(cls.Message)
        msg["service_data"]["message"] = message
        msg["service_data"]["title"] = title
        msg["service_data"]["target"] = target
        msg["service_data"]["data"] = data
        return cls(msg)

    @classmethod
    def make_from_yaml(cls, message: str, title: str, target: list, data: dict) -> 'Command':
        return cls.make(message, title, target, data)

    def __repr__(self, *args, **kwargs):
        s = "Command: domain '{}', service '{}', message '{}', title '{}', target {}, other data {}".format(self.domain,
                                                                                                            self.service,
                                                                                                            self.notify_message,
                                                                                                            self.title,
                                                                                                            self._target,
                                                                                                            self._data)
        return s


class Detachable(Command):
    """
    >>> import home
    >>> d = Detachable.make("some socket is now detachable", "", [], {})
    >>> msgs = d.make_msgs_from(home.appliance.socket.energy_guard.state.on.State([]),
    ...                         home.appliance.socket.energy_guard.state.detachable.State([]))
    >>> len(msgs)
    1
    >>> print(msgs)
    [Command: domain 'notify', service 'notify', message 'some socket is now detachable', title '', target [], other data {}]
    """

    Message = {
        "type": "call_service",
        "domain": "notify",
        "service": "notify",
        "service_data": {
        }
    }
    
    def make_msgs_from(self, old_state, new_state):
        result = []
        if (old_state.is_detachable != new_state.is_detachable) and new_state.is_detachable:
            result = self.execute()
        return result


