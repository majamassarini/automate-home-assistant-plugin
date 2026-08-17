import unittest  # noqa
import doctest
import home_assistant_plugin


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(home_assistant_plugin.message))
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.light.command)
    )
    tests.addTests(
        doctest.DocTestSuite(
            home_assistant_plugin.service.media_player.command
        )
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.sensor.trigger)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.notify.command)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.switch.trigger)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.switch.command)
    )
    tests.addTests(
        doctest.DocTestSuite(
            home_assistant_plugin.service.binary_sensor.trigger
        )
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.cover.trigger)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.cover.command)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.climate.trigger)
    )
    tests.addTests(
        doctest.DocTestSuite(home_assistant_plugin.service.climate.command)
    )
    tests.addTests(
        doctest.DocTestSuite(
            home_assistant_plugin.service.input_boolean.trigger
        )
    )
    tests.addTests(
        doctest.DocTestSuite(
            home_assistant_plugin.service.input_button.trigger
        )
    )

    return tests
