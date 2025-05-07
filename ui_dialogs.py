# -*- coding: utf-8 -*-

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDialogButtonBox, QTextEdit, QVBoxLayout, 
    QFrame, QHBoxLayout, QLabel, QLineEdit, QLayout)

class Ui_TextDialog(object):
    def setupUi(self, TextDialog):
        if not TextDialog.objectName():
            TextDialog.setObjectName(u"TextDialog")
        TextDialog.resize(408, 364)
        self.verticalLayout = QVBoxLayout(TextDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(TextDialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit)

        self.buttonBox = QDialogButtonBox(TextDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Discard|QDialogButtonBox.Save)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TextDialog)
        self.buttonBox.accepted.connect(TextDialog.accept)
        self.buttonBox.rejected.connect(TextDialog.reject)

        QMetaObject.connectSlotsByName(TextDialog)
    # setupUi

    def retranslateUi(self, TextDialog):
        TextDialog.setWindowTitle(QCoreApplication.translate("TextDialog", u"Dialog", None))
    # retranslateUi

class Ui_AccDialog(object):
    def setupUi(self, AccDialog):
        if not AccDialog.objectName():
            AccDialog.setObjectName(u"AccDialog")
        AccDialog.resize(500, 170)
        self.verticalLayout_2 = QVBoxLayout(AccDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(AccDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 115))
        font = QFont()
        font.setPointSize(12)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(86, 25))

        self.horizontalLayout.addWidget(self.label)

        self.name_lineEdit = QLineEdit(self.frame)
        self.name_lineEdit.setObjectName(u"name_lineEdit")

        self.horizontalLayout.addWidget(self.name_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(86, 25))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.pubkey_lineEdit = QLineEdit(self.frame)
        self.pubkey_lineEdit.setObjectName(u"pubkey_lineEdit")

        self.horizontalLayout_2.addWidget(self.pubkey_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.privkey_lineEdit = QLineEdit(self.frame)
        self.privkey_lineEdit.setObjectName(u"privkey_lineEdit")

        self.horizontalLayout_3.addWidget(self.privkey_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(AccDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(AccDialog)
        self.buttonBox.accepted.connect(AccDialog.accept)
        self.buttonBox.rejected.connect(AccDialog.reject)

        QMetaObject.connectSlotsByName(AccDialog)
    # setupUi

    def retranslateUi(self, AccDialog):
        AccDialog.setWindowTitle(QCoreApplication.translate("AccDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AccDialog", u"Name:", None))
        self.label_2.setText(QCoreApplication.translate("AccDialog", u"Public Key:", None))
        self.label_3.setText(QCoreApplication.translate("AccDialog", u"Private Key:", None))
    # retranslateUi

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        if not ConfigDialog.objectName():
            ConfigDialog.setObjectName(u"ConfigDialog")
        ConfigDialog.resize(383, 129)
        self.verticalLayout_2 = QVBoxLayout(ConfigDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(ConfigDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(12)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 25))
        self.label.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.config_field_lineEdit = QLineEdit(self.frame)
        self.config_field_lineEdit.setObjectName(u"config_field_lineEdit")

        self.horizontalLayout.addWidget(self.config_field_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 25))
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.config_value_lineEdit = QLineEdit(self.frame)
        self.config_value_lineEdit.setObjectName(u"config_value_lineEdit")

        self.horizontalLayout_2.addWidget(self.config_value_lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(ConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(ConfigDialog)
        self.buttonBox.accepted.connect(ConfigDialog.accept)
        self.buttonBox.rejected.connect(ConfigDialog.reject)

        QMetaObject.connectSlotsByName(ConfigDialog)
    # setupUi

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QCoreApplication.translate("ConfigDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("ConfigDialog", u"Field:", None))
        self.label_2.setText(QCoreApplication.translate("ConfigDialog", u"Value:", None))
    # retranslateUi

