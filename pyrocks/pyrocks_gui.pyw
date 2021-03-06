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
import ui_addvardlg
import ui_addbulkdlg

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

class AddVarDlg(QDialog,
                  ui_addvardlg.Ui_AddVarDlg):
    def __init__(self, parent=None):
        super(AddVarDlg, self).__init__(parent)
        self.__variableName = unicode('')
        self.setupUi(self)
    def accept(self):
        self.__variableName = self.varNameLineEdit.text()
        QDialog.accept(self)
    def variableName(self):
        return self.__variableName
    def setVariableName(self, name):
        self.varNameLineEdit.setText(name)

class AddBulkDlg(QDialog,
                  ui_addbulkdlg.Ui_AddBulkDlg):
    def __init__(self, parent=None):
        super(AddBulkDlg, self).__init__(parent)
        self.setupUi(self)
    def accept(self):
        QDialog.accept(self)

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
        self.addDockWidget(Qt.BottomDockWidgetArea, consoleDockWidget)
       
        self.modelTable = QTableWidget()
        self.setCentralWidget(self.modelTable)
        self.populateModelTable(None)
 
        self.treeWidget = QTreeWidget()
        self.treeWidget.setMinimumSize(200,400)
        logDockWidget = QDockWidget("Model Attributes", self)
        logDockWidget.setObjectName("ModelAttibutesWidget")
        logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
                                      Qt.RightDockWidgetArea)
        logDockWidget.setWidget(self.treeWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, logDockWidget)
        
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
        #*******File Menu*******
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(fileNewAction)
        fileOpenAction = self.createAction("&Open", self.fileOpen, None,
                None, "Open a previously created model")
        fileMenu.addAction(fileOpenAction)
        fileSaveAction = self.createAction("&Save", self.fileSave, None,
                None, "Save the current model")
        fileMenu.addAction(fileSaveAction)

        #*******Edit Menu*******
        editMenu = self.menuBar().addMenu("&Edit")

        #*******Model Menu*******
        modelMenu = self.menuBar().addMenu("&Model")
        modelRunAction = self.createAction("&Run Optimization", self.runModel, None, 
                None, "Run the optimization of the model for all phases")
        modelMenu.addAction(modelRunAction)
        bulkAddAction = self.createAction("&Add Bulk Composition", self.bulkAdd, None, 
                None, "Add Bulk Composition for the Model")
        modelMenu.addAction(bulkAddAction)
        bulkEditAction = self.createAction("&Edit Bulk Composition", self.bulkEdit, None, 
                None, "Edit Bulk Composition for the Model")
        modelMenu.addAction(bulkEditAction)

        #*******Phase Menu*******
        phaseMenu = self.menuBar().addMenu("&Phase")
        phaseAddAction = self.createAction("&Add Phase", self.phaseAdd, None, 
                None, "Add a new phase to model")
        phaseMenu.addAction(phaseAddAction)
        phaseEditAction = self.createAction("&Edit Phase", self.phaseEdit, None, 
                None, "Edit the selected phase")
        phaseMenu.addAction(phaseEditAction)
        varAddAction = self.createAction("&Add Variable", self.varAdd, None, 
                None, "Add a new variable to model")
        phaseMenu.addAction(varAddAction)
        varEditAction = self.createAction("&Edit Variable", self.varEdit, None, 
                None, "Edit the selected variable")
        phaseMenu.addAction(varEditAction)

        #*******Help Menu*******
        helpMenu = self.menuBar().addMenu("&Help")
        
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
        self.populateModelTable()

    def fileOpen(self):
        fileDialog = QFileDialog()
        fn = fileDialog.getOpenFileName()
        if not fn.isNull(): 
            self.model = pyrocks.open_model(fn)
            self.populateTree()
            self.populateModelTable()
   
    def fileSave(self):
        fileDialog = QFileDialog()
        fn = fileDialog.getSaveFileName()
        if not fn.isNull(): 
            self.model = pyrocks.save_model(self.model, fn)

    def runModel(self):
        all_phase_flag=True
        # Addition of free variables
        free_var = [#'SiO2', 
        #            'TiO2', 
                    'Al2O3', 
        #            'Fe', 
        #            'MnO', 
                    'MgO', 
                    'CaO', 
        #            'Na2O', 
        #            'K2O']
                          ] 
        for x in free_var:
            if x != 'SiO2':
                self.model.add_free_variable(x + '_pos', {'objfun': -100, x: 100}) 
            self.model.add_free_variable(x + '_neg', {'objfun': -100, x: -100}) 

        if all_phase_flag == True:
            for x in self.model.phases:
                self.consoleBrowser.insertPlainText('**********Maximizing %s*********\n' % x)
                pyrocks.optimize_model(self.model, x, 10)
        else:
            pyrocks.optimize_model(model, maxPhase, 10)

    # Functions to add and edit phases 
    def phaseAdd(self):
        addPhaseDialog = AddPhaseDlg()
        if addPhaseDialog.exec_():
            newPhase = unicode(addPhaseDialog.phaseName())
            self.model.add_phase(newPhase)
            self.phaseStoreData(addPhaseDialog, newPhase)
            self.consoleBrowser.insertPlainText("New phase added: %s\n" % newPhase)
            self.populateTree() 
            self.populateModelTable() 
    
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
            self.populateModelTable() 

    def bulkAdd(self):
        addBulkDialog = AddBulkDlg()
        self.populateBulk(addBulkDialog) 
        if addBulkDialog.exec_():
            self.bulkStoreData(addBulkDialog)
            self.populateTree() 
            self.populateModelTable()
            print self.model.bulk 

    def bulkEdit(self):
        editBulkDialog = AddBulkDlg()
        self.populateBulk(editBulkDialog) 
        if editBulkDialog.exec_():
            self.bulkStoreData(editBulkDialog)
            self.populateTree() 
            self.populateModelTable() 

    # Functions to add and edit phase variables
    def varAdd(self):
        if self.treeWidget.currentItem() is not None:
            selPhase = unicode(self.treeWidget.currentItem().text(0))
            addVariableDialog = AddVarDlg()
            if addVariableDialog.exec_():
                newVariable = unicode(addVariableDialog.variableName())
                self.consoleBrowser.insertPlainText("New variable added: %s\n" % newVariable)
                # Extract the table oxide components to add to variable 

                test_model = addVariableDialog.tableWidget.model()  
                data = []
                for row in range(test_model.rowCount()):
                  #data.append([])
                  for column in range(test_model.columnCount()):
                    index = test_model.index(row, column)
                    if column==0: 
                        oxide = str(test_model.data(index).toString())
                    if column==1:
                        value = float(test_model.data(index).toFloat()[0])
                        self.model.phases[selPhase].add_phase_variable(newVariable, oxide, value)
                self.populateTree() 
                self.populateModelTable() 
        else:
            self.consoleBrowser.insertPlainText("Please select a phase to add a variable\n")
    
    def varEdit(self):
        editVariableDialog = AddVarDlg()
        editVariable = unicode(self.treeWidget.currentItem().text(0))
        editPhase = unicode(self.treeWidget.currentItem().parent().text(0))
        editVariableDialog.setVariableName(editVariable) 
        self.populateVariableComp(editVariableDialog, editPhase, editVariable) 
        if editVariableDialog.exec_():
            test_model = editVariableDialog.tableWidget.model()  
            data = []
            for row in range(test_model.rowCount()):
              #data.append([])
              for column in range(test_model.columnCount()):
                index = test_model.index(row, column)
                if column==0: 
                    oxide = str(test_model.data(index).toString())
                if column==1:
                    value = float(test_model.data(index).toFloat()[0])
                    self.model.phases[editPhase].add_phase_variable(editVariable, oxide, value)
            self.populateTree() 
            self.populateModelTable() 

    def bulkStoreData(self, dlg):
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
                self.model.add_bulk(oxide, value)

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

    def populateVariableComp(self, dialog, phase, variable):
        dialog.tableWidget.clear()
        dialog.tableWidget.setSortingEnabled(False)
        dialog.tableWidget.setRowCount(len(pyrocks.bulk))
        headers = ["Oxide", "Weight Percent"]
        dialog.tableWidget.setColumnCount(len(headers))
        dialog.tableWidget.setHorizontalHeaderLabels(headers)

        for row, comp in enumerate(pyrocks.bulk):
            #print self.model.phases[newPhase].oxide_comp[oxide]
            item = QTableWidgetItem(comp)
            try:
                item = QTableWidgetItem(QString("%6") \
                    .arg(float(self.model.phases[phase].phase_variables[variable][comp]), 6, 'g', 5, QChar(" ")))
                dialog.tableWidget.setItem(row, headers.index("Oxide"), QTableWidgetItem(comp))
                dialog.tableWidget.setItem(row, headers.index("Weight Percent"), item)
            except:
                pass
        dialog.tableWidget.resizeColumnsToContents()
        dialog.tableWidget.setSortingEnabled(True)

    def populateBulk(self, dialog):
        dialog.tableWidget.clear()
        dialog.tableWidget.setSortingEnabled(False)
        dialog.tableWidget.setRowCount(len(self.model.bulk))
        headers = ["Oxide", "Weight Percent"]
        dialog.tableWidget.setColumnCount(len(headers))
        dialog.tableWidget.setHorizontalHeaderLabels(headers)

        for row, oxide in enumerate(self.model.bulk):
            #print self.model.phases[newPhase].oxide_comp[oxide]
            item = QTableWidgetItem(oxide)
            item = QTableWidgetItem(QString("%6") \
                .arg(float(self.model.bulk[oxide]), 6, 'g', 5, QChar(" ")))
            dialog.tableWidget.setItem(row, 0, QTableWidgetItem(oxide))
            dialog.tableWidget.setItem(row, 1, item)
        dialog.tableWidget.resizeColumnsToContents()
        dialog.tableWidget.setSortingEnabled(True)

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

    def populateModelTable(self, selectedItem=None):
        selected = None
        self.modelTable.clear()
        self.modelTable.setSortingEnabled(False)
        self.modelTable.setRowCount(self.MODEL_ROW_LENGTH)
        headers = ["Var. Comp."]
        k=1

        for phase in self.model.phases:
            # Add all phases
            headers.append(self.model.phases[phase].name)
            # Add all variables for the current phase
            for variable in self.model.phases[phase].phase_variables:
                headers.append(variable)
        self.modelTable.setColumnCount(len(headers))
        self.modelTable.setHorizontalHeaderLabels(headers)

        # Populate the row labels starting with the oxides
        for index, oxide in enumerate(pyrocks.bulk):
            self.modelTable.setItem(index, headers.index("Var. Comp."), QTableWidgetItem(oxide))

        #Populate the table by iterating through all phases and variables
        for phase in self.model.phases:
            for i,x in enumerate(pyrocks.bulk):
                #oxide = unicode(self.modelTable.verticalHeaderItem(i).text())
                item = QTableWidgetItem(QString("%6") \
                    .arg(float(self.model.phases[phase].oxide_comp[x]), 6, 'g', 5, QChar(" ")))
                #print i,oxide,item.text() 
                self.modelTable.setItem(i, headers.index(phase), item)
            for variable in self.model.phases[phase].phase_variables:
                for i,x in enumerate(pyrocks.bulk):
                    try:
                        item = QTableWidgetItem(QString("%6") \
                            .arg(float(self.model.phases[phase].phase_variables[variable][x]), 6, 'g', 5, QChar(" ")))
                        self.modelTable.setItem(i, headers.index(variable), item)
                    except:
                        pass
                
        # hide the vertical header column
        self.modelTable.verticalHeader().setVisible(False)
        self.modelTable.resizeColumnsToContents()
        self.modelTable.setSortingEnabled(True)

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
        
        
