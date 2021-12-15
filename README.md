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

## Documentation

* [automate-home protocol commands/triggers chapter](https://automate-home.readthedocs.io/en/latest/performer.html)

## Contributing

Pull requests are welcome!

## License

The automate-home-assistant-plugin is licensed under MIT