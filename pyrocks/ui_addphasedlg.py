# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addphasedlg.ui'
#
# Created: Fri May 29 11:01:44 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AddPhaseDlg(object):
    def setupUi(self, AddPhaseDlg):
        AddPhaseDlg.setObjectName(_fromUtf8("AddPhaseDlg"))
        AddPhaseDlg.resize(659, 430)
        self.buttonBox = QtGui.QDialogButtonBox(AddPhaseDlg)
        self.buttonBox.setGeometry(QtCore.QRect(290, 370, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayoutWidget = QtGui.QWidget(AddPhaseDlg)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 81))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.phaseNameLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.phaseNameLineEdit.setObjectName(_fromUtf8("phaseNameLineEdit"))
        self.gridLayout.addWidget(self.phaseNameLineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.phaseFormulaLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.phaseFormulaLineEdit.setObjectName(_fromUtf8("phaseFormulaLineEdit"))
        self.gridLayout.addWidget(self.phaseFormulaLineEdit, 1, 1, 1, 1)
        self.tableWidget = QtGui.QTableWidget(AddPhaseDlg)
        self.tableWidget.setGeometry(QtCore.QRect(410, 10, 231, 351))
        self.tableWidget.setMinimumSize(QtCore.QSize(2, 11))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(11)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(4, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(5, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(5, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(6, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(6, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(7, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(7, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(8, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(8, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(9, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(9, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(10, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(10, 1, item)
        self.gridLayoutWidget_2 = QtGui.QWidget(AddPhaseDlg)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(180, 100, 201, 80))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.wtPercentLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.wtPercentLabel.setObjectName(_fromUtf8("wtPercentLabel"))
        self.gridLayout_2.addWidget(self.wtPercentLabel, 1, 0, 1, 1)
        self.wtPercDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.wtPercDoubleSpinBox.setObjectName(_fromUtf8("wtPercDoubleSpinBox"))
        self.gridLayout_2.addWidget(self.wtPercDoubleSpinBox, 2, 0, 1, 1)
        self.qxrdErrorDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.qxrdErrorDoubleSpinBox.setObjectName(_fromUtf8("qxrdErrorDoubleSpinBox"))
        self.gridLayout_2.addWidget(self.qxrdErrorDoubleSpinBox, 2, 1, 1, 1)
        self.qxrdErrorLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.qxrdErrorLabel.setObjectName(_fromUtf8("qxrdErrorLabel"))
        self.gridLayout_2.addWidget(self.qxrdErrorLabel, 1, 1, 1, 1)

        self.retranslateUi(AddPhaseDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddPhaseDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddPhaseDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(AddPhaseDlg)

    def retranslateUi(self, AddPhaseDlg):
        AddPhaseDlg.setWindowTitle(_translate("AddPhaseDlg", "Dialog", None))
        self.label.setText(_translate("AddPhaseDlg", "Phase Name", None))
        self.label_2.setText(_translate("AddPhaseDlg", "Formula", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("AddPhaseDlg", "1", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("AddPhaseDlg", "2", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("AddPhaseDlg", "3", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("AddPhaseDlg", "4", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("AddPhaseDlg", "5", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("AddPhaseDlg", "6", None))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("AddPhaseDlg", "7", None))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("AddPhaseDlg", "8", None))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("AddPhaseDlg", "9", None))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("AddPhaseDlg", "10", None))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("AddPhaseDlg", "11", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("AddPhaseDlg", "Oxide", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("AddPhaseDlg", "Weight Percent", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("AddPhaseDlg", "SiO2", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("AddPhaseDlg", "TiO2", None))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("AddPhaseDlg", "Al2O3", None))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("AddPhaseDlg", "Fe", None))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("AddPhaseDlg", "MnO", None))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("AddPhaseDlg", "MgO", None))
        item = self.tableWidget.item(5, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("AddPhaseDlg", "CaO", None))
        item = self.tableWidget.item(6, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("AddPhaseDlg", "Na2O", None))
        item = self.tableWidget.item(7, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("AddPhaseDlg", "K2O", None))
        item = self.tableWidget.item(8, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(9, 0)
        item.setText(_translate("AddPhaseDlg", "SO3", None))
        item = self.tableWidget.item(9, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        item = self.tableWidget.item(10, 0)
        item.setText(_translate("AddPhaseDlg", "H2O", None))
        item = self.tableWidget.item(10, 1)
        item.setText(_translate("AddPhaseDlg", "0.0", None))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.wtPercentLabel.setText(_translate("AddPhaseDlg", "Weight Percent", None))
        self.qxrdErrorLabel.setText(_translate("AddPhaseDlg", "Error", None))

