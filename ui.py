from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QWidget, QApplication, \
    QPushButton, QHBoxLayout
from .core import Check
from .utils import getMayaMainWindow


class CheckItem(QTreeWidgetItem):

    DEFAULT_COLOR = QApplication.palette().text().color()

    STATES_COLORS = {
        Check.ERROR: QColor(255, 0, 0),
        Check.WARNING: QColor(255, 165, 0),
        Check.SUCCESS: QColor(0, 255, 0),
        Check.NOT_CHECKED: QColor(150, 150, 150),
    }

    def __init__(self, check: Check):
        super().__init__()
        self.check = check
        self.reload()

    def reload(self):
        self.setText(0, self.check.name)
        self.setToolTip(0, self.check.description)

        # logs items
        for i in range(self.childCount()):
            self.removeChild(self.child(i))

        for log in self.check.logs:
            item = QTreeWidgetItem()
            item.setText(0, str(log))
            self.addChild(item)

        # state color
        stateColor = self.STATES_COLORS.get(self.check.state, self.DEFAULT_COLOR)
        self.setTextColor(0, stateColor)

    def checkIt(self):
        self.check.check()
        self.reload()

    def reset(self):
        self.check.reset()
        self.reload()


class SanityCheckUi(QMainWindow):

    WINDOW_TITLE_PATTERN = 'Sanity Check - {name}'
    BUTTON_SIZE = QSize(75, 75)

    def __init__(self, parent, name, checks):
        super().__init__(parent)

        self.checks = checks

        self.setWindowTitle(self.WINDOW_TITLE_PATTERN.format(name=name))
        self.setStyleSheet('font-size: 30px;')

        self.checkTree = QTreeWidget()
        self.checkTree.setHeaderHidden(True)

        checkAllBtn = QPushButton()
        checkAllBtn.setFixedSize(self.BUTTON_SIZE)
        checkAllBtn.setToolTip('Check All')
        checkAllBtn.clicked.connect(self.checkAll)

        checkSelectedBtn = QPushButton()
        checkSelectedBtn.setFixedSize(self.BUTTON_SIZE)
        checkSelectedBtn.setToolTip('Check Selected')

        infoOnSelectedBtn = QPushButton()
        infoOnSelectedBtn.setFixedSize(self.BUTTON_SIZE)
        infoOnSelectedBtn.setToolTip('Info on Selected')

        resetSelectedBtn = QPushButton()
        resetSelectedBtn.setFixedSize(self.BUTTON_SIZE)
        resetSelectedBtn.setToolTip('Reset Selected')

        fixSelectedBtn = QPushButton()
        fixSelectedBtn.setFixedSize(self.BUTTON_SIZE)
        resetSelectedBtn.setToolTip('Fix Selected')

        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignLeft)
        buttonLayout.addWidget(checkAllBtn)
        buttonLayout.addWidget(checkSelectedBtn)
        buttonLayout.addWidget(resetSelectedBtn)
        buttonLayout.addWidget(infoOnSelectedBtn)
        buttonLayout.addWidget(fixSelectedBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.checkTree)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)

        self.reload()

    def reload(self):
        self.checkTree.clear()

        for check in self.checks:
            item = CheckItem(check)
            self.checkTree.addTopLevelItem(item)

    def checkAll(self):
        # items
        checkItems = list()
        for i in range(self.checkTree.topLevelItemCount()):
            checkItem = self.checkTree.topLevelItem(i)
            checkItems.append(checkItem)

        # reset
        for checkItem in checkItems:
            checkItem.reset()

        QApplication.processEvents()

        # check
        for checkItem in checkItems:
            checkItem.checkIt()
            QApplication.processEvents()


def openSanityCheck(checks):
    ui = SanityCheckUi(getMayaMainWindow(), 'Dev', checks)
    ui.resize(700, 1000)
    ui.show()
    return ui