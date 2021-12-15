import home
from home_assistant_plugin.message import Command as Parent


class Play(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> cmd = home_assistant_plugin.service.media_player.command.Play.make(["bath_player"])
    >>> old_state = home.appliance.sound.player.state.off.State()
    >>> new_state = old_state.next(home.appliance.sound.player.event.forced.Event.On)
    >>> msg = cmd.make_msgs_from(old_state, new_state)
    >>> msg[0].service
    'media_play'
    """

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "media_play",
        "service_data": {"entity_id": "none"},
    }

    def make_msgs_from(
        self,
        old_state: [
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
        new_state: [
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
    ):
        result = []
        if (old_state.is_on != new_state.is_on) and new_state.is_on:
            result = self.execute()
        return result


class Pause(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> cmd = home_assistant_plugin.service.media_player.command.Pause.make(["bath_player"])
    >>> old_state = home.appliance.sound.player.state.forced.on.State()
    >>> new_state = old_state.next(home.appliance.sound.player.event.forced.Event.Not)
    >>> msg = cmd.make_msgs_from(old_state, new_state)
    >>> msg[0].service
    'media_pause'
    """

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "media_pause",
        "service_data": {"entity_id": "none"},
    }

    def make_msgs_from(
        self,
        old_state: [
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
        new_state: [
            home.appliance.attribute.mixin.IsOn,
            home.appliance.attribute.mixin.IsOff,
        ],
    ):
        result = []
        if (old_state.is_on != new_state.is_on) and not new_state.is_on:
            result = self.execute()
        return result


class VolumeSet(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> cmd = home_assistant_plugin.service.media_player.command.VolumeSet.make(["bath_player"])
    >>> old_state = home.appliance.sound.player.state.forced.on.State()
    >>> new_state = old_state.next(home.appliance.sound.player.event.sleepy_volume.Event(15))
    >>> msg = cmd.make_msgs_from(old_state, new_state)
    >>> msg[0].service
    'volume_set'
    >>> msg[0].message["service_data"]["volume_level"]
    15
    """

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "volume_set",
        "service_data": {
            "entity_id": "none",
            "volume_level": 0.1,  # float between [0,1]
        },
    }

    def make_msgs_from(
        self,
        old_state: home.appliance.attribute.mixin.Volume,
        new_state: home.appliance.attribute.mixin.Volume,
    ):
        self.message["service_data"]["volume_level"] = new_state.volume
        result = self.execute()
        return result


class ShuffleSet(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> cmd = home_assistant_plugin.service.media_player.command.ShuffleSet.make(["bath_player"])
    >>> old_state = home.appliance.sound.player.state.forced.off.State()
    >>> msg = cmd.make_msgs_from(old_state, old_state)
    >>> msg[0].service
    'shuffle_set'
    >>> msg[0].message["service_data"]["shuffle"]
    True
    """

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "shuffle_set",
        "service_data": {"entity_id": "none", "shuffle": True},
    }

    def make_msgs_from(
        self, old_state: home.appliance.State, new_state: home.appliance.State
    ):
        result = self.execute()
        return result


class SelectSource(Parent):
    """
    >>> import home
    >>> import home_assistant_plugin

    >>> cmd = home_assistant_plugin.service.media_player.command.SelectSource.make(["bath_player"])
    >>> old_state = home.appliance.sound.player.state.forced.off.State()
    >>> new_state = old_state.next(home.appliance.sound.player.event.playlist.Event("morning playlist"))
    >>> msg = cmd.make_msgs_from(old_state, new_state)
    >>> msg[0].service
    'select_source'
    >>> msg[0].message["service_data"]["source"]
    'morning playlist'
    """

    Message = {
        "type": "call_service",
        "domain": "media_player",
        "service": "select_source",
        "service_data": {
            "entity_id": "none",
            "source": "none",  # a name in the sonos queue
        },
    }

    def make_msgs_from(
        self,
        old_state: home.appliance.attribute.mixin.Playlist,
        new_state: home.appliance.attribute.mixin.Playlist,
    ):
        self.message["service_data"]["source"] = new_state.playlist
        result = self.execute()
        return result
