# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addbulkdlg.ui'
#
# Created: Mon Jun 22 11:08:35 2015
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

class Ui_AddBulkDlg(object):
    def setupUi(self, AddBulkDlg):
        AddBulkDlg.setObjectName(_fromUtf8("AddBulkDlg"))
        AddBulkDlg.resize(271, 474)
        self.buttonBox = QtGui.QDialogButtonBox(AddBulkDlg)
        self.buttonBox.setGeometry(QtCore.QRect(50, 430, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tableWidget = QtGui.QTableWidget(AddBulkDlg)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 231, 351))
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
        self.label = QtGui.QLabel(AddBulkDlg)
        self.label.setGeometry(QtCore.QRect(20, 20, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(AddBulkDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddBulkDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddBulkDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(AddBulkDlg)

    def retranslateUi(self, AddBulkDlg):
        AddBulkDlg.setWindowTitle(_translate("AddBulkDlg", "Dialog", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("AddBulkDlg", "1", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("AddBulkDlg", "2", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("AddBulkDlg", "3", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("AddBulkDlg", "4", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("AddBulkDlg", "5", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("AddBulkDlg", "6", None))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("AddBulkDlg", "7", None))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("AddBulkDlg", "8", None))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("AddBulkDlg", "9", None))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("AddBulkDlg", "10", None))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("AddBulkDlg", "11", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("AddBulkDlg", "Oxide", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("AddBulkDlg", "Weight Percent", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("AddBulkDlg", "SiO2", None))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("AddBulkDlg", "TiO2", None))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("AddBulkDlg", "Al2O3", None))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("AddBulkDlg", "Fe", None))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("AddBulkDlg", "MnO", None))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(5, 0)
        item.setText(_translate("AddBulkDlg", "MgO", None))
        item = self.tableWidget.item(5, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(6, 0)
        item.setText(_translate("AddBulkDlg", "CaO", None))
        item = self.tableWidget.item(6, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(7, 0)
        item.setText(_translate("AddBulkDlg", "Na2O", None))
        item = self.tableWidget.item(7, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(8, 0)
        item.setText(_translate("AddBulkDlg", "K2O", None))
        item = self.tableWidget.item(8, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(9, 0)
        item.setText(_translate("AddBulkDlg", "SO3", None))
        item = self.tableWidget.item(9, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        item = self.tableWidget.item(10, 0)
        item.setText(_translate("AddBulkDlg", "H2O", None))
        item = self.tableWidget.item(10, 1)
        item.setText(_translate("AddBulkDlg", "0.0", None))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("AddBulkDlg", "Bulk Chemistry", None))

