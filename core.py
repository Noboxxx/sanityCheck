class Check:

    # states
    SUCCESS = 0
    WARNING = 1
    ERROR = 2
    NOT_CHECKED = 3

    # attributes
    name = 'Untitled'
    description = 'Description of the check'

    def __init__(self):
        self.state = self.NOT_CHECKED
        self.logs = list()

    def reset(self):
        self.state = self.NOT_CHECKED
        self.logs = list()

    def check(self):
        # reset parameters
        self.reset()

        # check
        try:
            self._check()
        except Exception as e:
            self.state = self.ERROR
            self.logs.append(str(e))

        # change not checked to success
        if self.state == self.NOT_CHECKED:
            self.state = self.SUCCESS

    def fix(self):
        # not checked or success ?
        if self.state == self.NOT_CHECKED:
            print('Please check first')
            return
        elif self.state == self.SUCCESS:
            print('Nothing to fix')
            return

        # fix
        self._fix()

        # check
        self.check()

    def _check(self):
        pass

    def _fix(self):
        pass


def getChecksFromData(data):
    pass


def getChecksFromJson(file):
    pass

