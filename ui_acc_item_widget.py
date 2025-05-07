# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acc_item_widgetScDzZY.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_AccItemWidget(object):
    def setupUi(self, AccItemWidget):
        if not AccItemWidget.objectName():
            AccItemWidget.setObjectName(u"AccItemWidget")
        AccItemWidget.resize(446, 27)
        self.horizontalLayout = QHBoxLayout(AccItemWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 1, -1, 1)
        self.name = QLabel(AccItemWidget)
        self.name.setObjectName(u"name")

        self.horizontalLayout.addWidget(self.name)

        self.pubkey = QLabel(AccItemWidget)
        self.pubkey.setObjectName(u"pubkey")

        self.horizontalLayout.addWidget(self.pubkey)

        self.generate_key_button = QPushButton(AccItemWidget)
        self.generate_key_button.setObjectName(u"generate_key_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generate_key_button.sizePolicy().hasHeightForWidth())
        self.generate_key_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.generate_key_button)

        self.edit_button = QPushButton(AccItemWidget)
        self.edit_button.setObjectName(u"edit_button")
        sizePolicy.setHeightForWidth(self.edit_button.sizePolicy().hasHeightForWidth())
        self.edit_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.edit_button)

        self.remove_button = QPushButton(AccItemWidget)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.remove_button)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)

        self.retranslateUi(AccItemWidget)

        QMetaObject.connectSlotsByName(AccItemWidget)
    # setupUi

    def retranslateUi(self, AccItemWidget):
        self.name.setText(QCoreApplication.translate("AccItemWidget", u"Name", None))
        self.pubkey.setText(QCoreApplication.translate("AccItemWidget", u"Pubkey", None))
        self.generate_key_button.setText(QCoreApplication.translate("AccItemWidget", u"Generate Key", None))
        self.edit_button.setText(QCoreApplication.translate("AccItemWidget", u"Edit", None))
        self.remove_button.setText(QCoreApplication.translate("AccItemWidget", u"Remove", None))
        pass
    # retranslateUi

