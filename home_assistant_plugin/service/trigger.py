import copy
from home_assistant_plugin.message import Trigger


class Equals(Trigger):
    """
    >>> import home_assistant_plugin
    >>> import json
    >>> json_trigger = '''
    ... {
    ...    "type":"event",
    ...    "event":{
    ...       "data":{
    ...          "entity_id":"light.bed_light",
    ...          "new_state":{
    ...             "entity_id":"light.bed_light",
    ...             "state":"on",
    ...             "attributes":{
    ...                "rgb_color":[
    ...                   254,
    ...                   208,
    ...                   0
    ...                ]
    ...             }
    ...          }
    ...       },
    ...       "event_type":"state_changed"
    ...    }
    ... }
    ... '''
    >>> another_trigger = '''
    ... {
    ...    "id": 18,
    ...    "type":"event",
    ...    "event":{
    ...       "data":{
    ...          "entity_id":"light.bed_light",
    ...          "new_state":{
    ...             "entity_id":"light.bed_light",
    ...             "last_changed":"2016-11-26T01:37:24.265390+00:00",
    ...             "state":"on",
    ...             "attributes":{
    ...                "color_temp":380,
    ...                "supported_features":147,
    ...                "xy_color":[
    ...                   0.5,
    ...                   0.5
    ...                ],
    ...                "brightness":180,
    ...                "white_value":200,
    ...                "friendly_name":"Bed Light"
    ...             },
    ...             "last_updated":"2016-11-26T01:37:24.265390+00:00"
    ...          },
    ...          "old_state":{
    ...             "entity_id":"light.bed_light",
    ...             "last_changed":"2016-11-26T01:37:10.466994+00:00",
    ...             "state":"off",
    ...             "attributes":{
    ...                "supported_features":147,
    ...                "friendly_name":"Bed Light"
    ...             },
    ...             "last_updated":"2016-11-26T01:37:10.466994+00:00"
    ...          }
    ...       },
    ...       "event_type":"state_changed",
    ...       "time_fired":"2016-11-26T01:37:24.265429+00:00",
    ...       "origin":"LOCAL"
    ...    }
    ... }
    ... '''
    >>> match_trigger = '''
    ... {
    ...    "id": 18,
    ...    "type":"event",
    ...    "event":{
    ...       "data":{
    ...          "entity_id":"light.bed_light",
    ...          "new_state":{
    ...             "entity_id":"light.bed_light",
    ...             "last_changed":"2016-11-26T01:37:24.265390+00:00",
    ...             "state":"on",
    ...             "attributes":{
    ...                "rgb_color":[
    ...                   254,
    ...                   208,
    ...                   0
    ...                ],
    ...                "color_temp":380,
    ...                "supported_features":147,
    ...                "xy_color":[
    ...                   0.5,
    ...                   0.5
    ...                ],
    ...                "brightness":180,
    ...                "white_value":200,
    ...                "friendly_name":"Bed Light"
    ...             },
    ...             "last_updated":"2016-11-26T01:37:24.265390+00:00"
    ...          },
    ...          "old_state":{
    ...             "entity_id":"light.bed_light",
    ...             "last_changed":"2016-11-26T01:37:10.466994+00:00",
    ...             "state":"off",
    ...             "attributes":{
    ...                "supported_features":147,
    ...                "friendly_name":"Bed Light"
    ...             },
    ...             "last_updated":"2016-11-26T01:37:10.466994+00:00"
    ...          }
    ...       },
    ...       "event_type":"state_changed",
    ...       "time_fired":"2016-11-26T01:37:24.265429+00:00",
    ...       "origin":"LOCAL"
    ...    }
    ... }
    ... '''
    >>> trigger_data = json.loads(json_trigger)
    >>> trigger = home_assistant_plugin.service.trigger.Equals(trigger_data)
    >>> trigger.attributes["rgb_color"]
    [254, 208, 0]
    >>> another_trigger_data = json.loads(another_trigger)
    >>> another_trigger = home_assistant_plugin.service.trigger.Equals(another_trigger_data)
    >>> trigger.is_triggered(another_trigger)
    False
    >>> match_trigger_data = json.loads(match_trigger)
    >>> match_trigger = home_assistant_plugin.service.trigger.Equals(match_trigger_data)
    >>> trigger.is_triggered(match_trigger)
    True
    >>> str(match_trigger)
    "Triggered entity light.bed_light state on with attributes [{'rgb_color': [254, 208, 0], 'color_temp': 380, 'supported_features': 147, 'xy_color': [0.5, 0.5], 'brightness': 180, 'white_value': 200, 'friendly_name': 'Bed Light'}]"
    """

    def __eq__(self, other):
        if super(Equals, self).__eq__(other):
            if self.state == other.state and set(
                [value for key, value in self.attributes.items()]
            ) == set(
                [
                    value
                    for key, value in other.attributes.items()
                    if key in self.attributes
                ]
            ):
                return True
        return False

    def __hash__(self):
        return hash(
            "{}{}{}".format(super(Equals, self).__hash__(), self.entity_id, self.state)
        )

    def __str__(self, *args, **kwargs):
        s = "Triggered entity {} state {} with attributes [{}]".format(
            self.entity_id, self.state, self.attributes
        )
        return s

    def is_triggered(self, another_description):
        if super(Equals, self).is_triggered(another_description):
            other = self.__class__(another_description.message)
            if self.state == other.state and set(
                [key for key in self.attributes.keys()]
            ) == set(
                [key for key in other.attributes.keys() if key in self.attributes]
            ):
                self._logger.info("triggered {}".format(another_description))
                return True
        return False


class ChangedState(Trigger):
    """
    >>> from home_assistant_plugin.message import Description
    >>> class Example(ChangedState):
    ...     Message = {
    ...         "type": "event",
    ...         "event": {
    ...         "event_type": "state_changed", 
    ...             "data": {
    ...                 "entity_id": "example_id",
    ...                 "new_state": {"entity_id": "example_id", "state": "on"},
    ...             }
    ...         }
    ...     }
    >>> trigger = Example.make("example_id")
    >>> import json
    >>> message = '''
    ... {"id": 1, 
    ...   "type": "event", 
    ...   "event": {
    ...     "event_type": "state_changed", 
    ...     "data": {"entity_id": "example_id", 
    ...       "new_state": {"entity_id": "example_id", 
    ...         "state": "on", "attributes": {"an_attribute": "new_value", "min_mireds": 153, "max_mireds": 500}},
    ...       "old_state": {"entity_id": "example_id", 
    ...         "state": "off", "attributes": {"an_attribute": "old_value", "min_mireds": 153, "max_mireds": 500}}
    ...     }
    ...   }
    ... }
    ... '''
    >>> message_data = json.loads(message)
    >>> message_trigger = Example(message_data)
    >>> trigger == message_trigger
    True
    >>> message_description = Description(message_data)
    >>> trigger.is_triggered(message_description)
    True
    >>> str(trigger)
    'Triggered entity example_id with state changed in on'
    """

    def __eq__(self, other):
        if super(ChangedState, self).__eq__(other):
            if self.state == other.state:
                return True
        return False

    def __hash__(self):
        return hash(
            "{}{}{}".format(super(ChangedState, self).__hash__(), self.entity_id, self.state)
        )

    def __str__(self, *args, **kwargs):
        s = "Triggered entity {} with state changed in {}".format(
            self.entity_id, self.state)
        return s

    def is_triggered(self, another_description):
        if super(ChangedState, self).is_triggered(another_description):
            other = self.__class__(another_description.message)
            if self == other:
                if other.state != other._old_state:
                    return True


class ChangedAttribute(Trigger):
    """
    >>> from home_assistant_plugin.message import Description
    >>> class Example(ChangedAttribute):
    ...     Message = {
    ...         "type": "event",
    ...         "event": {
    ...         "event_type": "state_changed", 
    ...             "data": {
    ...                 "entity_id": "example_id",
    ...                 "new_state": {"entity_id": "example_id", "attributes": {"an_attribute": "a_value"}},
    ...             }
    ...         }
    ...     }
    >>> trigger = Example.make("example_id")
    >>> import json
    >>> message = '''
    ... {"id": 1, 
    ...   "type": "event", 
    ...   "event": {
    ...     "event_type": "state_changed", 
    ...     "data": {"entity_id": "example_id", 
    ...       "new_state": {"entity_id": "example_id", 
    ...         "state": "on", "attributes": {"an_attribute": "new_value", "min_mireds": 153, "max_mireds": 500}},
    ...       "old_state": {"entity_id": "example_id", 
    ...         "state": "off", "attributes": {"an_attribute": "old_value", "min_mireds": 153, "max_mireds": 500}}
    ...     }
    ...   }
    ... }
    ... '''
    >>> message_data = json.loads(message)
    >>> message_trigger = Example(message_data)
    >>> trigger == message_trigger
    True
    >>> message_description = Description(message_data)
    >>> trigger.is_triggered(message_description)
    True
    >>> len(set([trigger, message_trigger]))
    2
    >>> str(trigger)
    "Triggered entity example_id with at least one changed attribute in ['an_attribute']"
    """

    def __eq__(self, other):
        if super(ChangedAttribute, self).__eq__(other):
            if set(self.attributes.keys()).issubset(set(other.attributes.keys())):
                return True
        return False

    def __hash__(self):
        attributes = ".".join([attribute for attribute in self.attributes.keys()])
        return hash(
            "{}{}{}{}".format(super(ChangedAttribute, self).__hash__(), self.entity_id, self.state, attributes)
        )

    def __str__(self, *args, **kwargs):
        s = "Triggered entity {} with at least one changed attribute in {}".format(
            self.entity_id, list(self.attributes.keys())
        )
        return s

    def is_triggered(self, another_description):
        if super(ChangedAttribute, self).is_triggered(another_description):
            other = self.__class__(another_description.message)
            if self == other:
                for attribute in self.attributes.keys():
                    if attribute in other._old_attributes:
                        if other.attributes[attribute] != other._old_attributes[attribute]:
                            return True


class Comparison(Trigger):
    def __init__(self, message, events=None, value=None):
        message = self.override_value(message, value)
        super(Comparison, self).__init__(message, events)

    def __eq__(self, other):
        if super(Comparison, self).__eq__(other):
            if self.state == other.state:
                return True
        return False

    def __hash__(self):
        return hash(
            "{}{}{} comparison".format(
                super(Trigger, self).__hash__(), self.entity_id, self.state
            )
        )

    @staticmethod
    def override_value(message, value=None):
        if value:
            message["event"]["data"]["new_state"]["state"] = str(value)
        return message

    @classmethod
    def make(cls, entity_id, events=None, value=None):
        message = copy.deepcopy(cls.Message)
        message["event"]["data"]["entity_id"] = entity_id
        return cls(message, events, value)

    @classmethod
    def make_from_yaml(cls, entity_id, events=None, value=None):
        return cls.make(entity_id, events, value)

    def is_triggered(self, another_description):
        if super(Comparison, self).is_triggered(another_description):
            triggered = self.__class__ == another_description.__class__
            return triggered
        return False


class GreaterThan(Comparison):
    def is_triggered(self, another_description):
        if super(GreaterThan, self).is_triggered(another_description):
            triggered = self.state < another_description.state
            self._logger.debug(
                "{} triggered={} {} < {}".format(
                    self, triggered, self.state, another_description.state
                )
            )
            return triggered
        return False

    def __str__(self):
        s = super(GreaterThan, self).__str__()
        return "{} greater than {}".format(s, self.state)


class LesserThan(Comparison):
    def is_triggered(self, another_description):
        if super(LesserThan, self).is_triggered(another_description):
            triggered = self.state > another_description.state
            self._logger.debug(
                "{} triggered={} {} > {}".format(
                    self, triggered, self.state, another_description.state
                )
            )
            return triggered
        return False

    def __str__(self):
        s = super(LesserThan, self).__str__()
        return "{} lesser than {}".format(s, self.state)


class InBetween(Comparison):
    def __init__(self, message, events=None, value=None, range=None):
        message = self.override_value(message, value)
        super(InBetween, self).__init__(message, events, value)
        self._range = range if range else 1

    def is_triggered(self, another_description):
        if super(InBetween, self).is_triggered(another_description):
            triggered = (
                self.state < another_description.state < (self.state + self._range)
            )
            self._logger.debug(
                "{} triggered={} {} < {} < {}".format(
                    self,
                    triggered,
                    self.state,
                    another_description.state,
                    (self.state + self._range),
                )
            )
            return triggered
        return False

    def __str__(self):
        s = super(InBetween, self).__str__()
        return "{} in between [{}:{}]".format(s, self.state, (self.state + self._range))
