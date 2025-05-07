# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_guiesEbhM.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainGui(object):
    def setupUi(self, MainGui):
        if not MainGui.objectName():
            MainGui.setObjectName(u"MainGui")
        MainGui.resize(731, 450)
        font = QFont()
        font.setPointSize(12)
        MainGui.setFont(font)
        self.horizontalLayout_6 = QHBoxLayout(MainGui)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tabWidget = QTabWidget(MainGui)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(390, 343))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.controlRoomTab = QWidget()
        self.controlRoomTab.setObjectName(u"controlRoomTab")
        self.horizontalLayout_5 = QHBoxLayout(self.controlRoomTab)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_2 = QTabWidget(self.controlRoomTab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setDocumentMode(True)
        self.actionsTab = QWidget()
        self.actionsTab.setObjectName(u"actionsTab")
        self.gridLayout = QGridLayout(self.actionsTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 139, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(282, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.actionsTab)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.start_button = QPushButton(self.actionsTab)
        self.start_button.setObjectName(u"start_button")

        self.verticalLayout_4.addWidget(self.start_button)

        self.stop_button = QPushButton(self.actionsTab)
        self.stop_button.setObjectName(u"stop_button")

        self.verticalLayout_4.addWidget(self.stop_button)

        self.restart_button = QPushButton(self.actionsTab)
        self.restart_button.setObjectName(u"restart_button")

        self.verticalLayout_4.addWidget(self.restart_button)

        self.delete_button = QPushButton(self.actionsTab)
        self.delete_button.setObjectName(u"delete_button")

        self.verticalLayout_4.addWidget(self.delete_button)

        self.label_2 = QLabel(self.actionsTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_2)

        self.unlock_button = QPushButton(self.actionsTab)
        self.unlock_button.setObjectName(u"unlock_button")

        self.verticalLayout_4.addWidget(self.unlock_button)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(282, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.tabWidget_2.addTab(self.actionsTab, "")
        self.genesisAccountTab = QWidget()
        self.genesisAccountTab.setObjectName(u"genesisAccountTab")
        self.verticalLayout_6 = QVBoxLayout(self.genesisAccountTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_2 = QFrame(self.genesisAccountTab)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 115))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(86, 0))

        self.horizontalLayout_7.addWidget(self.label_6)

        self.genesis_name_input = QLineEdit(self.frame_2)
        self.genesis_name_input.setObjectName(u"genesis_name_input")

        self.horizontalLayout_7.addWidget(self.genesis_name_input)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(86, 0))

        self.horizontalLayout_8.addWidget(self.label_8)

        self.genesis_pub_key_input = QLineEdit(self.frame_2)
        self.genesis_pub_key_input.setObjectName(u"genesis_pub_key_input")

        self.horizontalLayout_8.addWidget(self.genesis_pub_key_input)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(86, 25))

        self.horizontalLayout_9.addWidget(self.label_7)

        self.genesis_priv_key_input = QLineEdit(self.frame_2)
        self.genesis_priv_key_input.setObjectName(u"genesis_priv_key_input")

        self.horizontalLayout_9.addWidget(self.genesis_priv_key_input)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_6.addWidget(self.frame_2)

        self.verticalSpacer_4 = QSpacerItem(20, 228, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.tabWidget_2.addTab(self.genesisAccountTab, "")
        self.systemAccountsTab = QWidget()
        self.systemAccountsTab.setObjectName(u"systemAccountsTab")
        self.verticalLayout_3 = QVBoxLayout(self.systemAccountsTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.acc_listWidget = QListWidget(self.systemAccountsTab)
        self.acc_listWidget.setObjectName(u"acc_listWidget")

        self.verticalLayout_3.addWidget(self.acc_listWidget)

        self.add_account_button = QPushButton(self.systemAccountsTab)
        self.add_account_button.setObjectName(u"add_account_button")

        self.verticalLayout_3.addWidget(self.add_account_button)

        self.tabWidget_2.addTab(self.systemAccountsTab, "")
        self.generalTab = QWidget()
        self.generalTab.setObjectName(u"generalTab")
        self.verticalLayout_7 = QVBoxLayout(self.generalTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.config_listWidget = QListWidget(self.generalTab)
        self.config_listWidget.setObjectName(u"config_listWidget")

        self.verticalLayout_7.addWidget(self.config_listWidget)

        self.add_config_button = QPushButton(self.generalTab)
        self.add_config_button.setObjectName(u"add_config_button")

        self.verticalLayout_7.addWidget(self.add_config_button)

        self.tabWidget_2.addTab(self.generalTab, "")
        self.serversTab = QWidget()
        self.serversTab.setObjectName(u"serversTab")
        self.tabWidget_2.addTab(self.serversTab, "")

        self.horizontalLayout_5.addWidget(self.tabWidget_2)

        self.tabWidget.addTab(self.controlRoomTab, "")
        self.queryTab = QWidget()
        self.queryTab.setObjectName(u"queryTab")
        self.verticalLayout_2 = QVBoxLayout(self.queryTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser = QTextBrowser(self.queryTab)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(True)
        self.textBrowser.setMinimumSize(QSize(370, 140))
        self.textBrowser.setMaximumSize(QSize(16777215, 140))

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.frame = QFrame(self.queryTab)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(370, 0))
        self.frame.setMaximumSize(QSize(16777215, 141))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.account_name_input = QLineEdit(self.frame)
        self.account_name_input.setObjectName(u"account_name_input")

        self.horizontalLayout.addWidget(self.account_name_input)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.action_input = QLineEdit(self.frame)
        self.action_input.setObjectName(u"action_input")

        self.horizontalLayout_2.addWidget(self.action_input)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.file_name_input = QLineEdit(self.frame)
        self.file_name_input.setObjectName(u"file_name_input")

        self.horizontalLayout_3.addWidget(self.file_name_input)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.fresh_report_button = QPushButton(self.frame)
        self.fresh_report_button.setObjectName(u"fresh_report_button")

        self.horizontalLayout_4.addWidget(self.fresh_report_button)

        self.submit_button = QPushButton(self.frame)
        self.submit_button.setObjectName(u"submit_button")

        self.horizontalLayout_4.addWidget(self.submit_button)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 414, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.queryTab, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)


        self.retranslateUi(MainGui)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainGui)
    # setupUi

    def retranslateUi(self, MainGui):
        MainGui.setWindowTitle(QCoreApplication.translate("MainGui", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainGui", u"Chain actions:", None))
        self.start_button.setText(QCoreApplication.translate("MainGui", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("MainGui", u"Stop", None))
        self.restart_button.setText(QCoreApplication.translate("MainGui", u"Restart", None))
        self.delete_button.setText(QCoreApplication.translate("MainGui", u"Delete", None))
        self.label_2.setText(QCoreApplication.translate("MainGui", u"Wallet actions:", None))
        self.unlock_button.setText(QCoreApplication.translate("MainGui", u"Unlock", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.actionsTab), QCoreApplication.translate("MainGui", u"Actions", None))
        self.label_6.setText(QCoreApplication.translate("MainGui", u"Name:", None))
        self.genesis_name_input.setText("")
        self.label_8.setText(QCoreApplication.translate("MainGui", u"Public key:", None))
        self.genesis_pub_key_input.setText("")
        self.label_7.setText(QCoreApplication.translate("MainGui", u"Private key:", None))
        self.genesis_priv_key_input.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.genesisAccountTab), QCoreApplication.translate("MainGui", u"Genesis account", None))
        self.add_account_button.setText(QCoreApplication.translate("MainGui", u"Add account", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.systemAccountsTab), QCoreApplication.translate("MainGui", u"System accounts", None))
        self.add_config_button.setText(QCoreApplication.translate("MainGui", u"Add configuration field", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.generalTab), QCoreApplication.translate("MainGui", u"General settings", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.serversTab), QCoreApplication.translate("MainGui", u"Servers", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.controlRoomTab), QCoreApplication.translate("MainGui", u"Control room", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainGui", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Generate a json report based on the provided account name and action. Report lists all the actions by the corresponding block. Output file name (or path) can be set here, or the default naming will be used. Fresh report will not reuse data if there is a previous output file with the same path.</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainGui", u"Account name", None))
        self.account_name_input.setText(QCoreApplication.translate("MainGui", u"inery.token", None))
        self.label_4.setText(QCoreApplication.translate("MainGui", u"Action", None))
        self.action_input.setText(QCoreApplication.translate("MainGui", u"transfer", None))
        self.label_5.setText(QCoreApplication.translate("MainGui", u"File name", None))
        self.fresh_report_button.setText(QCoreApplication.translate("MainGui", u"Fresh report", None))
        self.submit_button.setText(QCoreApplication.translate("MainGui", u"Submit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.queryTab), QCoreApplication.translate("MainGui", u"Query", None))
    # retranslateUi

