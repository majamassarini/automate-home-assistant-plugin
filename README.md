# automate-home-assistant-plugin
[![Build Status](https://app.travis-ci.com/majamassarini/automate-home-assistant-plugin.svg?branch=main)](https://app.travis-ci.com/majamassarini/automate-home-assistant-plugin)
[![codecov](https://codecov.io/gh/majamassarini/automate-home-assistant-plugin/branch/main/graph/badge.svg?token=)](https://codecov.io/gh/majamassarini/automate-home-assistant-plugin)

The **Home Assistant** plugin for the [automate-home project](https://github.com/majamassarini/automate-home).

## Yaml examples of usage

Triggers for a *Home Assistant* **wind sensor**.
```yaml
- !Performer
  name: "wind trigger"
  for appliance: "wind"
  commands: []
  triggers:
    - !home_assistant_plugin.service.sensor.float.trigger.Always {entity_id: "sensor.velocita_del_vento"}

- !Performer
  name: "strong wind trigger"
  for appliance: "wind"
  commands: []
  triggers:
    - !home_assistant_plugin.service.sensor.float.trigger.GreaterThan
      entity_id: "sensor.velocita_del_vento"
      events:
        - !home.event.wind.Event.Strong
      value: 3.0
```

Command for notifying a message through *Home Assistant*.

```yaml
- !Performer
  name: "notify microwave can be detached"
  for appliance: "microwave"
  commands:
    - !home_assistant_plugin.service.notify.command.Detachable {message: "the microwave could be detached", title: "", target: [], data: {}}
  triggers: []
```

Trigger and command for a *Home Assistant* **switch** (a smart plug, wired to
a `socket` or `sprinkler` appliance — pick the appliance's own forced event
via `events:`).
```yaml
- !Performer
  name: "kitchen plug"
  for appliance: "kitchen socket"
  commands:
    - !home_assistant_plugin.service.switch.command.TurnOn {entity_id: "switch.kitchen_plug"}
    - !home_assistant_plugin.service.switch.command.TurnOff {entity_id: "switch.kitchen_plug"}
  triggers:
    - !home_assistant_plugin.service.switch.trigger.On {entity_id: "switch.kitchen_plug"}
    - !home_assistant_plugin.service.switch.trigger.Off {entity_id: "switch.kitchen_plug"}
```

Trigger for a *Home Assistant* **binary sensor** (motion, door, rain, ...),
with the injected event configured explicitly since binary sensors cover too
many different real-world meanings to guess a default.
```yaml
- !Performer
  name: "hallway motion"
  for appliance: "hallway light"
  commands: []
  triggers:
    - !home_assistant_plugin.service.binary_sensor.trigger.On
      entity_id: "binary_sensor.hallway_motion"
      events:
        - !home.event.presence.Event.On
```

Trigger and command for a *Home Assistant* **cover** (a curtain/blind).
```yaml
- !Performer
  name: "bedroom curtain"
  for appliance: "bedroom curtain"
  commands:
    - !home_assistant_plugin.service.cover.command.OpenCover {entity_id: "cover.bedroom_curtain"}
    - !home_assistant_plugin.service.cover.command.CloseCover {entity_id: "cover.bedroom_curtain"}
  triggers:
    - !home_assistant_plugin.service.cover.trigger.Open {entity_id: "cover.bedroom_curtain"}
    - !home_assistant_plugin.service.cover.trigger.Closed {entity_id: "cover.bedroom_curtain"}
```

Trigger and command for a *Home Assistant* **climate** entity (a thermostat).
```yaml
- !Performer
  name: "living room thermostat"
  for appliance: "living room thermostat"
  commands:
    - !home_assistant_plugin.service.climate.command.SetTemperature {entity_id: "climate.living_room"}
    - !home_assistant_plugin.service.climate.command.SetHvacMode {entity_id: "climate.living_room"}
  triggers:
    - !home_assistant_plugin.service.climate.trigger.Heating {entity_id: "climate.living_room"}
    - !home_assistant_plugin.service.climate.trigger.Idle {entity_id: "climate.living_room"}
```

Trigger for a *Home Assistant* **input_boolean** or **input_button** helper
(manual scene toggles / scene buttons), again with the injected event
configured explicitly.
```yaml
- !Performer
  name: "movie night scene"
  for appliance: "living room lights"
  commands: []
  triggers:
    - !home_assistant_plugin.service.input_boolean.trigger.On
      entity_id: "input_boolean.movie_night"
      events:
        - !home.event.presence.Event.On
    - !home_assistant_plugin.service.input_button.trigger.Pressed
      entity_id: "input_button.movie_night_scene"
      events:
        - !home.event.presence.Event.On
```

## Documentation

* [automate-home protocol commands/triggers chapter](https://automate-home.readthedocs.io/en/latest/performer.html)

## Contributing

Pull requests are welcome!

## License

The automate-home-assistant-plugin is licensed under MIT