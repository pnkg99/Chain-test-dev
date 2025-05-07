# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acc_dialogwczNkI.ui'
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
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

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

