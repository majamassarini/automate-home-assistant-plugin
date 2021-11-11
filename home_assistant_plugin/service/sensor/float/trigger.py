import home
from home_assistant_plugin.message import Trigger
from home_assistant_plugin.service.sensor.trigger import FloatMixin
from home_assistant_plugin.service.trigger import GreaterThan as GTParent, LesserThan as LTParent, InBetween as IBParent


class Always(FloatMixin, Trigger, home.protocol.mean.Mixin):

    def get_value(self, description: 'home_assistant_plugin.message.Description') -> float:
        return float(description.state)


class GreaterThan(FloatMixin, GTParent):
    pass


class LesserThan(FloatMixin, LTParent):
    pass


class InBetween(FloatMixin, IBParent):
    pass
