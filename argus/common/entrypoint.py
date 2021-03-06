#!/usr/bin/env python3

"""
Argus Entrypoint

Usage:
  entrypoint.py run <module>
  entrypoint.py test <module>
  entrypoint.py -h | --help
  entrypoint.py --version

Options:
  -h --help    Show this screen
  --version    Show version
"""

from docopt import docopt
import site


class Entrypoint:
    def __init__(self, arguements):
        self.args = arguements
        self.module_run_map = {
            "caterpillar": self._run_caterpillar,
            "faker": self._run_faker,
        }
        self.module_test_map = {
            "common": self._test_common,
            "caterpillar": self._test_caterpillar,
            "faker": self._test_faker,
        }
        self.app = None

    def run(self):
        if self.args["test"] or self.args["run"]:
            assert "<module>" in self.args
            module_name = self.args["<module>"].lower()
            if self.args["test"]:
                assert module_name in self.module_test_map
                self.module_test_map[module_name]()
            elif self.args["run"]:
                assert module_name in self.module_run_map
                self.module_run_map[module_name]()

    def _run_caterpillar(self):
        from argus.caterpillar.Caterpillar import Caterpillar

        self.app = Caterpillar()
        self.app.run()

    def _run_faker(self):
        from argus.faker.Faker import Faker

        self.app = Faker()
        self.app.run()

    def _test_common(self):
        import doctest

        doctest.testmod(argus.common.Common)

    def _test_caterpillar(self):
        import doctest

        doctest.testmod(argus.caterpillar.Caterpillar)

    def _test_faker(self):
        import doctest

        doctest.testmod(argus.faker.Faker)


if __name__ == "__main__":
    import sys

    sys.path.append("/app")
    arguements = docopt(__doc__, version="Entrypoint 0.1")
    entrypoint = Entrypoint(arguements)
    entrypoint.run()
