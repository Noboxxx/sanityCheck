class CHECKSTATE:
    NONE = 0 # waiting to be checked
    SUCCESS = 10 # no errors found
    WARNING = 20 # skippable errors found
    ERROR = 30 # errors found
    CRITICAL = 40 # check failed to execute properly

class Check:

    niceName = ''

    fixable = True
    selectable = True
    hasTool = False

    def __init__(self):
        self.state = CHECKSTATE.NONE
        self.toSelect = list()

    def reset(self):
        self.state = CHECKSTATE.NONE
        self.toSelect = list()

    def getLabel(self):
        if self.niceName:
            return self.niceName

        return self.__class__.__name__

    def getDescription(self):
        return self.__doc__

    def assertIsFixable(self):
        if not self.fixable:
            raise Exception('Check is not fixable')
        elif self.state == CHECKSTATE.NONE:
            raise Exception('Check needs to be checked first')
        elif self.state == CHECKSTATE.SUCCESS:
            raise Exception('Check is a success therefore it doesn\'t need to be fixed')
        elif self.state == CHECKSTATE.CRITICAL:
            raise Exception('Check failed to execute properly therefore it cannot be fixed properly')

    def assertIsSelectable(self):
        if not self.selectable:
            raise Exception('Check is not selectable')
        elif not self.toSelect:
            raise Exception('Check contains nothing to be selected')

    def assertHasTool(self):
        if not self.hasTool:
            raise Exception('Check has no related tool')

    def check(self):
        self.reset()
        self.state = CHECKSTATE.NONE
        try:
            self._check()
        except Exception as e:
            self.state = CHECKSTATE.CRITICAL
            print(e)

    def fix(self):
        self.assertIsFixable()
        try:
            self._fix()
        except Exception as e:
            print(e)
        self.check()

    def select(self):
        self.assertIsSelectable()
        self._select()

    def openTool(self):
        self.assertHasTool()
        self.openTool()

    def _check(self):
        raise NotImplemented()

    def _fix(self):
        raise NotImplemented()

    def _select(self):
        raise NotImplemented()

    def _openTool(self):
        raise NotImplemented()