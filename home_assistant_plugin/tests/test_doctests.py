import unittest
import doctest
import home_assistant_plugin


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(home_assistant_plugin.message))
    tests.addTests(doctest.DocTestSuite(home_assistant_plugin.service.notify.command))

    return tests