from PySide6.QtCore import QObject, Signal, QCoreApplication, QMetaObject
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy

class Worker(QObject):
    finished = Signal()
    progress = Signal(int) # progress percent (0–100)
    resultReady = Signal(object)  # New signal to emit the result when done

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.result = self.func(*self.args, **self.kwargs, report=self.progress.emit) 
        self.resultReady.emit(self.result)
        self.finished.emit()

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

