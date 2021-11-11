import copy
import logging

import home


class Description(home.protocol.Description):

    PROTOCOL = "home_assistant"

    Message = {"type": "none",
               }

    def __init__(self, message):
        super(Description, self).__init__(message)
        self._type = message["type"]
        self._entity_id = "none"
        self._message = message
        self._logger = logging.getLogger(__name__)
        self._label = str(self._message)

    def __eq__(self, other):
        if self.PROTOCOL == other.PROTOCOL:
            if self.type == other.type:
                return True
        return False

    def __hash__(self):
        return hash("{}".format(self.type))

    @property
    def type(self):
        return self._type

    @property
    def message(self):
        return self._message

    @classmethod
    def make(cls, entity_id):
        message = cls(copy.deepcopy(cls.Message))
        message._entity_id = entity_id
        return message

    @classmethod
    def make_from_yaml(cls, entity_id):
        return cls.make(entity_id)

    @classmethod
    def make_from(cls, message):
        description = cls(message)
        return description

    def __str__(self, *args, **kwargs):
        s = "{} [{}]".format(self.type, self.message)
        return s
    

class Trigger(home.protocol.Trigger, Description):

    Message = {"type": "event",
               "event": {
                   "data": {
                       "entity_id": "some id",
                       "new_state": {
                           "entity_id": "some id",
                           "state": "???",
                           "attributes": {}
                       }
                   },
                   "event_type": "state_changed",
               }
               }

    def __init__(self, message, events=None):
        super(Trigger, self).__init__(message, events)
        if message["type"] == self.Message["type"]:
            if message["event"]["event_type"] == self.Message["event"]["event_type"]:
                self._entity_id = message["event"]["data"]["entity_id"]
                self._state = message["event"]["data"]["new_state"]["state"]
                try:
                    self._attributes = message["event"]["data"]["new_state"]["attributes"]
                except KeyError as e:
                    pass
            else:
                raise AttributeError("Given message ({}) is not a state_changed event message"
                                     "it should have event_type \"state_changed\"".format(message))
        else:
            raise AttributeError("Given message ({}) is not a trigger message"
                                 "it should have type \"event\"".format(message))

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def state(self):
        return self._state

    @property
    def attributes(self):
        return self._attributes

    def __eq__(self, other):
        if super(Trigger, self).__eq__(other):
            if self.__class__ == other.__class__:
                if self.entity_id == other.entity_id:
                    return True
        return False

    def __hash__(self):
        return hash("{}{}".format(super(Trigger, self).__hash__(), self.entity_id))

    def is_triggered(self, another_description):
        if super(Trigger, self).is_triggered(another_description):
            try:
                other = self.__class__(another_description.message)
                if self.entity_id == other.entity_id:
                    return True
            except AttributeError:
                return False
        return False

    def __str__(self, *args, **kwargs):
        s = "Trigger entity {}".format(self.entity_id)
        return s

    @classmethod
    def make(cls, entity_id, events=None):
        message = copy.deepcopy(cls.Message)
        message["event"]["data"]["entity_id"] = entity_id
        return cls(message, events)

    @classmethod
    def make_from_yaml(cls, entity_id, events=None):
        return cls.make(entity_id, events)

    def make_new_state_from(self, another_description, old_state):
        new_state = super(Trigger, self).make_new_state_from(another_description, old_state)
        new_state = new_state.next(another_description.state)
        return new_state


class Command(home.protocol.Command, Description):
    """
    >>> import json
    >>> command_data = '''
    ... {
    ...   "type": "call_service",
    ...   "domain": "light",
    ...   "service": "turn_on",
    ...   "service_data": {
    ...     "entity_id": "light.kitchen"
    ...   }
    ... }
    ... '''
    >>> command_data = json.loads(command_data)
    >>> command = Command(command_data)
    >>> command.execute()
    [Command: domain 'light', service 'turn_on', entity_id 'light.kitchen']
    """

    Message = {"type": "call_service",
               "domain": "none",
               "service": "none",
               "service_data": {
                   "entity_id": "none",
               }
               }

    def __init__(self, message):
        super(Command, self).__init__(message)
        if message["type"] == self.Message["type"]:
            self._domain = message["domain"]
            self._service = message["service"]
            self._entity_id = message["service_data"]["entity_id"]
        else:
            raise AttributeError("Given message ({}) is not a command message"
                                 "it should be of type \"event\"".format(message))

    def __eq__(self, other):
        if super(Command, self).__eq__(other):
            if self.entity_id == other.entity_id and \
                    self.domain == other.domain and \
                    self.service == other.service:
                return True
        return False

    def __hash__(self):
        return hash("{}{}{}{}".format(super(Command, self).__hash__(),
                    self.domain,
                    self.service,
                    self.entity_id))

    @property
    def domain(self):
        return self._domain

    @property
    def service(self):
        return self._service

    @property
    def entity_id(self):
        return self._entity_id

    def execute(self):
        self._logger.info("execute {}".format(self.message))
        return [self]

    def make_msgs_from(self, old_state, new_state):
        return []

    @classmethod
    def make(cls, entity_id):
        message = copy.deepcopy(cls.Message)
        message["service_data"]["entity_id"] = entity_id
        return cls(message)

    def __repr__(self, *args, **kwargs):
        s = "Command: domain '{}', service '{}', entity_id '{}'".format(self.domain, self.service, self.entity_id)
        return s



