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
    def setPhaseName(self, name):
        self.phaseNameLineEdit.setText(name)
    def setQxrd(self, value):
        self.wtPercDoubleSpinBox.setValue(value)
    def setQxrdError(self, error):
        self.qxrdErrorDoubleSpinBox.setValue(error)

class MainWindow(QMainWindow):
    MODEL_ROW_LENGTH = 20

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        if fn is not None:
            self.model = pyrocks.open_model(fn)
        else:
            self.model = pyrocks.Model('unnamed')

        self.consoleBrowser = QTextBrowser()
        self.consoleBrowser.setMinimumSize(800,50)
        self.consoleBrowser.setAlignment(Qt.AlignLeft)
        self.consoleBrowser.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.consoleBrowser.insertPlainText("***** Pyrocks ver. %s - written by %s *****\n" % (__version__, __author__))
        consoleDockWidget = QDockWidget("Console", self)
        consoleDockWidget.setObjectName("ConsoleDockWidget")
        consoleDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                          Qt.RightDockWidgetArea|
                                          Qt.TopDockWidgetArea|
                                          Qt.BottomDockWidgetArea)
        consoleDockWidget.setWidget(self.consoleBrowser)
        #self.addDockWidget(Qt.BottomDockWidgetArea, consoleDockWidget)
       
        self.modelTable = QTableWidget()
        self.setCentralWidget(self.modelTable)
        self.populateModelTable(self.modelTable, None)
 
        self.treeWidget = QTreeWidget()
        self.treeWidget.setMinimumSize(200,600)
        logDockWidget = QDockWidget("Model Attributes", self)
        logDockWidget.setObjectName("ModelAttibutesWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)
        logDockWidget.setWidget(self.treeWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, consoleDockWidget)
        
        self.populateTree()
 
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
        fileOpenAction = self.createAction("&Open", self.fileOpen, None,
                None, "Open a previously created model")
        fileMenu.addAction(fileOpenAction)
        fileSaveAction = self.createAction("&Save", self.fileSave, None,
                None, "Save the current model")
        fileMenu.addAction(fileSaveAction)
       
        editMenu = self.menuBar().addMenu("&Edit")

        varMenu = self.menuBar().addMenu("&Variable")
        varAddAction = self.createAction("&Add Variable", self.varAdd, None, 
                None, "Add a new variable to model")
        varMenu.addAction(varAddAction)


        phaseMenu = self.menuBar().addMenu("&Phase")
        phaseAddAction = self.createAction("&Add Phase", self.phaseAdd, None, 
                None, "Add a new phase to model")
        phaseMenu.addAction(phaseAddAction)
        phaseEditAction = self.createAction("&Edit Phase", self.phaseEdit, None, 
                None, "Edit the selected phase")
        phaseMenu.addAction(phaseEditAction)

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

    def fileOpen(self):
        fileDialog = QFileDialog()
        fn = fileDialog.getOpenFileName()
        if not fn.isNull(): 
            self.model = pyrocks.open_model(fn)
            self.populateTree()
   
    def fileSave(self):
        fileDialog = QFileDialog()
        fn = fileDialog.getSaveFileName()
        if not fn.isNull(): 
            self.model = pyrocks.save_model(self.model, fn)

    def varAdd(self):
        print 'new var' 

    def phaseAdd(self):
        addPhaseDialog = AddPhaseDlg()
        if addPhaseDialog.exec_():
            newPhase = unicode(addPhaseDialog.phaseName())
            self.model.add_phase(newPhase)
            self.phaseStoreData(addPhaseDialog, newPhase)
            self.consoleBrowser.insertPlainText("New phase added: %s\n" % newPhase)
            self.populateTree() 
    
    def phaseEdit(self):
        editPhaseDialog = AddPhaseDlg()
        editPhase = unicode(self.treeWidget.currentItem().text(0))
        editPhaseDialog.setPhaseName(editPhase) 
        editPhaseDialog.setQxrd(self.model.phases[editPhase].qxrd)
        editPhaseDialog.setQxrdError(self.model.phases[editPhase].qxrd_error)
        self.populatePhaseOxides(editPhaseDialog, editPhase) 
        if editPhaseDialog.exec_():
            self.phaseStoreData(editPhaseDialog, editPhase)
            self.populateTree() 

    def phaseStoreData(self, dlg, newPhase):
        self.model.phases[newPhase].add_qxrd(dlg.qxrd())
        self.model.phases[newPhase].add_qxrd_error(dlg.qxrdError())

        # Extract the table oxide components to add to phase 
        test_model = dlg.tableWidget.model()  
        data = []
        for row in range(test_model.rowCount()):
          data.append([])
          for column in range(test_model.columnCount()):
            index = test_model.index(row, column)
            if column==0: 
                oxide = str(test_model.data(index).toString())
            if column==1:
                value = float(test_model.data(index).toFloat()[0])
                self.model.phases[newPhase].set_oxide_comp(oxide, value)

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
            # Populate the additional variables for the phase
            for variable in self.model.phases[phase].phase_variables:
                QTreeWidgetItem(phases[phase], [variable])

        # Populate the variables 
        #varTreeItem = QTreeWidgetItem(modelTreeItem, ["Variables"])
        #for phase in self.model.phases:
        #    phases[phase] = QTreeWidgetItem(phaseTreeItem, [phase])

        # Expand the whole tree showing all phases and variables
        self.treeWidget.expandItem(modelTreeItem)
        self.treeWidget.expandItem(phaseTreeItem)
        self.treeWidget.resizeColumnToContents(0)

    def populatePhaseOxides(self, addPhaseDialog, newPhase, selectedItem=None):
        selected = None
        addPhaseDialog.tableWidget.clear()
        addPhaseDialog.tableWidget.setSortingEnabled(False)
        addPhaseDialog.tableWidget.setRowCount(len(self.model.phases[newPhase].oxide_comp))
        headers = ["Oxide", "Weight Percent"]
        addPhaseDialog.tableWidget.setColumnCount(len(headers))
        addPhaseDialog.tableWidget.setHorizontalHeaderLabels(headers)

        for row, oxide in enumerate(self.model.phases[newPhase].oxide_comp):
            #print self.model.phases[newPhase].oxide_comp[oxide]
            item = QTableWidgetItem(oxide)
            item = QTableWidgetItem(QString("%6") \
                .arg(float(self.model.phases[newPhase].oxide_comp[oxide]), 6, 'g', 5, QChar(" ")))
            addPhaseDialog.tableWidget.setItem(row, 0, QTableWidgetItem(oxide))
            addPhaseDialog.tableWidget.setItem(row, 1, item)
        addPhaseDialog.tableWidget.resizeColumnsToContents()
        addPhaseDialog.tableWidget.setSortingEnabled(True)

    def populateModelTable(self, tableWidget, selectedItem=None):
        selected = None
        tableWidget.clear()
        tableWidget.setSortingEnabled(False)
        tableWidget.setRowCount(self.MODEL_ROW_LENGTH)
        headers = []

        # Populate the row labels starting with the oxides
        tableWidget.setVerticalHeaderLabels(QStringList(pyrocks.bulk))

        for phase in self.model.phases:
            # Add all phases
            headers.append(self.model.phases[phase].name)
            # Add all variables for the current phase
            for variable in self.model.phases[phase].phase_variables:
                headers.append(variable)

# Two problems to work out
# assigning the data point to the correct row lab
# assigning the data point to the correct column

        tableWidget.setColumnCount(len(headers))
        tableWidget.setHorizontalHeaderLabels(headers)
        for phase in self.model.phases:
            for row, oxide in enumerate(self.model.phases[phase].oxide_comp):
                print self.model.phases[phase].oxide_comp[oxide]
                item = QTableWidgetItem(QString("%6") \
                    .arg(float(self.model.phases[phase].oxide_comp[oxide]), 6, 'g', 5, QChar(" ")))
                tableWidget.setItem(row, 0, item)
        tableWidget.resizeColumnsToContents()
        tableWidget.setSortingEnabled(True)

if __name__ == "__main__":
    import sys
    try:
        fn = sys.argv[1]
    except:
        #print "Please provide a filename: python pyrocks.py FILENAME"
        fn = None
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
        
        
