import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import helpform
#import newimagedlg
#import qrc_resources
import pyrocks
import ui_newmodeldlg
import ui_addphasedlg
import ui_addqxrddlg


__version__ = "0.0.1"
__author__ = "Patrick D. Cavanagh"


class NewModelDlg(QDialog,
                  ui_newmodeldlg.Ui_NewModelDlg):
    def __init__(self, parent=None):
        super(NewModelDlg, self).__init__(parent)
        self.__modelName = unicode('')
        self.setupUi(self)

    def accept(self):
        self.__modelName = self.modelNameLineEdit.text()
        QDialog.accept(self)

    def modelName(self):
        return self.__modelName 

class AddPhaseDlg(QDialog,
                  ui_addphasedlg.Ui_AddPhaseDlg):
    def __init__(self, parent=None):
        super(AddPhaseDlg, self).__init__(parent)
        self.__phaseName = unicode('')
        self.__phaseFormula = unicode('')
        self.__qxrd = 0.0
        self.__qxrdError = 0.0
        self.setupUi(self)

    def accept(self):
        self.__phaseName = self.phaseNameLineEdit.text()
        self.__phaseFormula = self.phaseFormulaLineEdit.text()
        self.__qxrd = self.wtPercDoubleSpinBox.value()
        self.__qxrdError = self.qxrdErrorDoubleSpinBox.value()
        QDialog.accept(self)

    def phaseName(self):
        return self.__phaseName
    def phaseFormula(self):
        return self.__phaseFormula
    def qxrd(self):
        return self.__qxrd
    def qxrdError(self):
        return self.__qxrdError

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        self.model = pyrocks.Model('unnamed')

        self.consoleBrowser = QTextBrowser()
        self.consoleBrowser.setMinimumSize(800,600)
        self.consoleBrowser.setAlignment(Qt.AlignLeft)
        self.consoleBrowser.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.consoleBrowser)
        self.consoleBrowser.insertPlainText("***** Pyrocks ver. %s - written by %s *****\n" % (__version__, __author__))
        
        self.treeWidget = QTreeWidget()
        self.treeWidget.setMinimumSize(200,600)
        logDockWidget = QDockWidget("Model Attributes", self)
        logDockWidget.setObjectName("ModelAttibutesWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)
        logDockWidget.setWidget(self.treeWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidget)
        
        self.populateTree()
 
        self.printer = None

        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)

        # create new action for a new file, both toolbar and menu
        fileNewAction = QAction(QIcon("images/filenew.png"), "&New", self)
        fileNewAction.setShortcut(QKeySequence.New)
        helpText = "Create a new model"
        fileNewAction.setToolTip(helpText)
        fileNewAction.setStatusTip(helpText)
        self.connect(fileNewAction, SIGNAL("triggered()"), self.fileNew)


        # add actions to menu and toolbar
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(fileNewAction)
       
        editMenu = self.menuBar().addMenu("&Edit")

        varMenu = self.menuBar().addMenu("&Variable")
        varAddAction = self.createAction("&Add Variable", self.varAdd, None, 
                None, "Add a new variable to model")
        varMenu.addAction(varAddAction)


        phaseMenu = self.menuBar().addMenu("&Phase")
        phaseAddAction = self.createAction("&Add Phase", self.phaseAdd, None, 
                None, "Add a new phase to model")
        phaseMenu.addAction(phaseAddAction)

        helpMenu = self.menuBar().addMenu("&Help")
        
        #fileToolbar.addAction(fileNewAction)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action 

    def fileNew(self):
        newModelDialog = NewModelDlg()
        if newModelDialog.exec_():
            self.model.name = newModelDialog.modelName()
        self.populateTree() 

    def varAdd(self):
        print 'new var' 

    def phaseAdd(self):
        addPhaseDialog = AddPhaseDlg()
        if addPhaseDialog.exec_():
            newPhase = addPhaseDialog.phaseName()
            self.model.add_phase(newPhase)
            self.model.phases[newPhase].add_qxrd(addPhaseDialog.qxrd())
            self.model.phases[newPhase].add_qxrd_error(addPhaseDialog.qxrdError())
            self.consoleBrowser.insertPlainText("New phase added: %s\n" % newPhase)
            self.populateTree() 
    
    def populateTree(self, selectedItem=None):
        selected = None
        self.treeWidget.clear()
        self.treeWidget.setItemsExpandable(True)  
        phases = {}

        # Add the project name to the top of the tree
        modelTreeItem = QTreeWidgetItem([self.model.name]) 
        self.treeWidget.addTopLevelItem(modelTreeItem) 
         
        # Populate the phases
        phaseTreeItem = QTreeWidgetItem(modelTreeItem, ["Phases"])
        for phase in self.model.phases:
            phases[phase] = QTreeWidgetItem(phaseTreeItem, [phase])

        # Populate the variables 
        varTreeItem = QTreeWidgetItem(modelTreeItem, ["Variables"])
        #for phase in self.model.phases:
        #    phases[phase] = QTreeWidgetItem(phaseTreeItem, [phase])

        # Expand the whole tree showing all phases and variables
        self.treeWidget.expandItem(modelTreeItem)
        self.treeWidget.resizeColumnToContents(0)
 
app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()
        
        
