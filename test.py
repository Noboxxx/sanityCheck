from time import sleep
from .ui import openSanityCheck
from .core import Check


class ErrorCheck(Check):

    name = 'Error Check'
    description = 'Always fails'

    def _check(self):
        sleep(2)
        self.state = self.ERROR
        self.logs.append('It has fail')
        self.logs.append('Error detected!')


class CorruptedCheck(Check):

    name = 'Corrupted Check'
    description = 'is corrupted'

    def _check(self):
        raise Exception('PLOP')


class WarningCheck(Check):

    name = 'Warning Check'
    description = 'Always warn'

    def _check(self):
        sleep(2)
        self.state = self.WARNING
        self.logs.append('Beware!')


def main():
    checks = [
        ErrorCheck(),
        WarningCheck(),
        CorruptedCheck(),
        Check(),
    ]

    openSanityCheck(checks)
