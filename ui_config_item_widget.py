# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_item_widgetVeXawz.ui'
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

class Ui_ConfigItemWidget(object):
    def setupUi(self, ConfigItemWidget):
        if not ConfigItemWidget.objectName():
            ConfigItemWidget.setObjectName(u"ConfigItemWidget")
        ConfigItemWidget.resize(287, 27)
        self.horizontalLayout = QHBoxLayout(ConfigItemWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 1, -1, 1)
        self.config_value = QLabel(ConfigItemWidget)
        self.config_value.setObjectName(u"config_value")

        self.horizontalLayout.addWidget(self.config_value)

        self.edit_button = QPushButton(ConfigItemWidget)
        self.edit_button.setObjectName(u"edit_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_button.sizePolicy().hasHeightForWidth())
        self.edit_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.edit_button)

        self.remove_button = QPushButton(ConfigItemWidget)
        self.remove_button.setObjectName(u"remove_button")
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.remove_button)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(ConfigItemWidget)

        QMetaObject.connectSlotsByName(ConfigItemWidget)
    # setupUi

    def retranslateUi(self, ConfigItemWidget):
        self.config_value.setText(QCoreApplication.translate("ConfigItemWidget", u"Name", None))
        self.edit_button.setText(QCoreApplication.translate("ConfigItemWidget", u"Edit", None))
        self.remove_button.setText(QCoreApplication.translate("ConfigItemWidget", u"Remove", None))
        pass
    # retranslateUi

