# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialogblvDfy.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

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

