# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newmodeldlg.ui'
#
# Created: Tue May 26 16:14:11 2015
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

class Ui_NewModelDlg(object):
    def setupUi(self, NewModelDlg):
        NewModelDlg.setObjectName(_fromUtf8("NewModelDlg"))
        NewModelDlg.resize(400, 105)
        self.buttonBox = QtGui.QDialogButtonBox(NewModelDlg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 60, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(NewModelDlg)
        self.widget.setGeometry(QtCore.QRect(20, 20, 361, 23))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.modelLabel = QtGui.QLabel(self.widget)
        self.modelLabel.setObjectName(_fromUtf8("modelLabel"))
        self.horizontalLayout.addWidget(self.modelLabel)
        self.modelNameLineEdit = QtGui.QLineEdit(self.widget)
        self.modelNameLineEdit.setObjectName(_fromUtf8("modelNameLineEdit"))
        self.horizontalLayout.addWidget(self.modelNameLineEdit)

        self.retranslateUi(NewModelDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewModelDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewModelDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(NewModelDlg)

    def retranslateUi(self, NewModelDlg):
        NewModelDlg.setWindowTitle(_translate("NewModelDlg", "Dialog", None))
        self.modelLabel.setText(_translate("NewModelDlg", "Model Name:", None))

