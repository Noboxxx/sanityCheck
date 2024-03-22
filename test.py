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
        WarningCheck(),
        Check(),
    ]

    openSanityCheck(checks)
