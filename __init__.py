#from binaryninja import *
from binaryninja import BinaryView
from binaryninja import (PluginCommand, show_message_box, MessageBoxButtonSet, MessageBoxIcon)

import binaryninjaui
from binaryninjaui import (getMonospaceFont, UIAction, UIActionHandler, Menu, UIContext)
if "qt_major_version" in binaryninjaui.__dict__ and binaryninjaui.qt_major_version == 6:
    from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication, QWidget,
         QVBoxLayout, QHBoxLayout, QDialog, QFileSystemModel, QTreeView, QLabel, QSplitter,
         QInputDialog, QMessageBox, QHeaderView, QKeySequenceEdit, QCheckBox, QGroupBox, QSizePolicy, QScrollArea,
         QSpacerItem, QListView)
    from PySide6.QtCore import (QDir, Qt, QFileInfo, QItemSelectionModel, QSettings, QUrl, QRect)
    from PySide6.QtGui import (QFontMetrics, QDesktopServices, QKeySequence, QIcon)
else:
    from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication, QWidget,
         QVBoxLayout, QHBoxLayout, QDialog, QFileSystemModel, QTreeView, QLabel, QSplitter,
         QInputDialog, QMessageBox, QHeaderView, QKeySequenceEdit, QCheckBox, QGroupBox, QSizePolicy, QScrollArea,
         QSpacerItem, QListView)
    from PySide2.QtCore import (QDir, Qt, QFileInfo, QItemSelectionModel, QSettings, QUrl, QRect)
    from PySide2.QtGui import (QFontMetrics, QDesktopServices, QKeySequence, QIcon)

class Ninpatch(QDialog):

    def __init__(self, context, parent=None):
        super(Ninpatch, self).__init__(parent)

        # Create widgets
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.title = QLabel(self.tr("Ninpatch"))
        self.setWindowTitle(self.title.text())
        self.resize(419, 530)

        # ----
        self.groupBox = QGroupBox(self.tr("&Patches"))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)

        # ---- 
        self.listOfPatches = QListView(self.groupBox)
        self.bv = context.binaryView
        #self.test = bv.query_metadata("binpatch-patches")
        print("Here")
        print(context.binaryView.get_disassembly(0x13e7))
        print( self.bv.get_disassembly(0x13e7))
        print("------")

        # ----
        self.buttonSelect = QPushButton(self.groupBox.tr("&Select All"))
        self.buttonDeselect = QPushButton(self.groupBox.tr("&Deselect All"))
        self.hLayoutSeclection = QHBoxLayout()
        self.hLayoutSeclection.addWidget(self.buttonSelect)
        self.hLayoutSeclection.addWidget(self.buttonDeselect)

        # ----
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.addWidget(self.listOfPatches)
        self.verticalLayout.addLayout(self.hLayoutSeclection)

        # ----
        self.buttonPatch = QPushButton(self.tr("&Patch File"))
        self.hLayoutIO = QHBoxLayout()
        self.buttonImportPacthes = QPushButton(self.tr("&Import Patches"))
        self.buttonExportPatches = QPushButton(self.tr("&Export Patches"))
        self.hLayoutIO.addWidget(self.buttonImportPacthes)
        self.hLayoutIO.addWidget(self.buttonExportPatches)

        # ----
        self.hLayoutClose = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonClose = QPushButton(self.tr("&Close"))
        self.hLayoutClose.addItem(self.horizontalSpacer)
        self.hLayoutClose.addWidget(self.buttonClose)

        # ----
        self.vLayoutButtons = QVBoxLayout()
        self.vLayoutButtons.addWidget(self.buttonPatch)
        self.vLayoutButtons.addLayout(self.hLayoutIO)
        self.vLayoutButtons.addLayout(self.hLayoutClose)

        self.vLayoutPatches = QVBoxLayout()
        self.vLayoutPatches.addWidget(self.groupBox)
        self.vLayoutPatches.addLayout(self.vLayoutButtons)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.addLayout(self.vLayoutPatches)

        #self.saveButton = QPushButton(self.tr("&Save"))
        #self.saveButton.setShortcut(QKeySequence(self.tr("Ctrl+S")))

        # Add signals
        self.buttonPatch.clicked.connect(self.saveClicked)
        self.buttonClose.clicked.connect(self.close)

        # Set dialog layout
        self.setLayout(self.verticalLayout_3)

    def saveClicked(self):
        print("Click!")


def bp_patch(bv,function):
	patchesList = []
	tmpValues = bv.read(function, bv.get_instruction_length(function)).hex()

	try:
		patchesList = bv.query_metadata("binpatch-patches")
		patchesList.append(tmpValues)
		bv.store_metadata("binpatch-patches", patchesList)
	except:
		bv.store_metadata("binpatch-patches", [tmpValues])

	show_message_box("Do Nothing", str(hex(function)), MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)


def bp_view(bv,function):
	tmpVal = bv.query_metadata("binpatch-patches")
	show_message_box("View Patches", ', '.join(tmpVal)+"\n\n", MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)

PluginCommand.register_for_address(
	"NinPatch\\Patch\\Patch01", "Patch this", bp_patch
)

PluginCommand.register_for_address(
	"NinPatch\\View\\View Patches", "View all Patches", bp_view
)

binpatch = None

def launchPlugin(context):
    global binpatch
    if not binpatch:
        binpatch = Ninpatch(context, parent=context.widget)
    binpatch.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    binpatch = Ninpatch(None)
    binpatch.show()
    sys.exit(app.exec_())
else:
    UIAction.registerAction("NinPatch\\View Patches")
    UIActionHandler.globalActions().bindAction("NinPatch\\View Patches", UIAction(launchPlugin))
    Menu.mainMenu("Tools").addAction("NinPatch\\View Patches", "NinPatch")