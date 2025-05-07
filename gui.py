#!/usr/bin/python3.9
'''
NOTE! This need so be added to ui_main_gui.py:

from PySide6.QtWidgets import QStyle

# Assuming you're in a class with self.delete_button, i.e. in:

class Ui_MainGui(object):
    def setupUi(self, Gui):
    
        icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning) # !
        self.delete_button.setIcon(icon)                              # !

'''

import sys
import json

from PySide6 import QtWidgets
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (QWidget, QDialog, QFileDialog, QMessageBox, 
    QDialogButtonBox, QProgressDialog, QListWidgetItem)

from ui_main_gui import Ui_MainGui
from ui_dialogs import Ui_TextDialog, Ui_AccDialog, Ui_ConfigDialog
from ui_helpers import Worker, Ui_AccItemWidget, Ui_ConfigItemWidget
from report_actions import generate_report
from chain import Chain
from logger import Logger


class Gui(QWidget, Ui_MainGui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Inery test chain")

        self.system_accounts = {}

        chain = Chain.get_instance() # NOTE  ! this will have to be moved to after getting setup inputs
                                     # NOTE 2! it can stay here, and call chain.setup() later
        Logger.get_instance(verbose=True)

        self.genesis_account = chain.genesis_account
        self.master_chain = chain.master_chain
        self.side_chains = chain.side_chains
        self.genesis_json = chain.genesis_json
        self.config = self.genesis_json["initial_configuration"]

        self.system_accounts = {}
        accounts = chain.system_accounts
        for acc in accounts:
            name = acc.pop("NAME")
            self.system_accounts[name] = acc
            self.add_acc_to_list(name, acc["PUBLIC_KEY"])

        self.genesis_name_input.setText(self.genesis_account["NAME"])
        self.genesis_pub_key_input.setText(self.genesis_account["PUBLIC_KEY"])
        self.genesis_priv_key_input.setText(self.genesis_account["PRIVATE_KEY"])
        for field in self.config:
            self.add_config_to_list(field, self.config[field], required=True)
        self.start_button.clicked.connect(chain.run_chain)
        self.stop_button.clicked.connect(chain.stop_chain)
        self.restart_button.clicked.connect(lambda: (chain.stop_chain(), chain.run_chain()))
        self.delete_button.clicked.connect(lambda: (chain.stop_chain(), chain.remove_chain()))
        self.unlock_button.clicked.connect(chain.unlock_wallet)
        self.submit_button.clicked.connect(self.querry)
        self.fresh_report_button.clicked.connect(lambda: self.querry(True))
        self.add_account_button.clicked.connect(self.prompt_add_acc_to_list)
        self.add_config_button.clicked.connect(self.prompt_add_config_to_list)


    # Querry
    def querry(self, fresh=False):
        # print('account: ', self.account_name_input.text())
        # print('action: ', self.action_input.text())
        # print('file name: ', self.file_name_input.text())

        if not Chain.get_instance().is_started():
            QMessageBox.warning(self, "Warning", "Chain not started!")
            return
        
        self.file_name = (
            self.file_name_input.text() 
            or 
            '_'.join([
                self.account_name_input.text(), 
                self.action_input.text(), 
                'report.json'
                ])
            )
        
        self.dialog = QProgressDialog('Generating report', None, 0, 100, self)
        self.dialog.setWindowTitle('Wait')
        self.dialog.setAutoClose(True)
        self.dialog.setAutoReset(True)
        self.dialog.show()

        self.thread = QThread()
        self.worker = Worker(generate_report,
                        self.account_name_input.text(), 
                        self.action_input.text(),
                        self.file_name,
                        fresh
                        ) 

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.dialog.setValue)
        self.worker.resultReady.connect(self.handle_result)

        self.thread.start()

    def handle_result(self, result):
        dialog = TextDialog(json.dumps(result, indent=4), self.file_name)
        dialog.exec()    

    # Control room 
    def prompt_add_acc_to_list(self):
        dialog = AccDialog(self)

        if dialog.exec() == QDialog.Accepted:
            name, keys = dialog.get_data()

            # Add to list
            if name in self.system_accounts:
                QMessageBox.warning(self, "Warning", "Same account exists already!")
                return
            
            self.system_accounts[name] = keys
            self.add_acc_to_list(name, keys["PUBLIC_KEY"]) 

    def add_acc_to_list(self, name, pubkey):
        item_widget = AccItemWidget(name, pubkey)
        list_item = QListWidgetItem(self.acc_listWidget)

        # Set item size
        list_item.setSizeHint(item_widget.sizeHint())

        self.acc_listWidget.addItem(list_item)
        self.acc_listWidget.setItemWidget(list_item, item_widget)

        # Connect buttons
        item_widget.remove_button.clicked.connect(lambda: self.remove_acc_item(list_item))
        item_widget.edit_button.clicked.connect(lambda: self.edit_acc_item(item_widget))
        item_widget.generate_key_button.clicked.connect(lambda: self.generate_key(item_widget))

    def remove_acc_item(self, item):
        row = self.acc_listWidget.row(item)
        widget = self.acc_listWidget.itemWidget(item)
        del self.system_accounts[widget.name.text()]
        self.acc_listWidget.takeItem(row)

    def edit_acc_item(self, item_widget):
        name = item_widget.name.text()
        keys = self.system_accounts[name]

        dialog = AccDialog(self)

        dialog.name_lineEdit.setText(name)
        dialog.pubkey_lineEdit.setText(keys["PUBLIC_KEY"])
        dialog.privkey_lineEdit.setText(keys["PRIVATE_KEY"])

        if dialog.exec() == QDialog.Accepted:
            new_name, new_keys = dialog.get_data()
            if new_name != name and new_name in self.system_accounts:
                QMessageBox.warning(self, "Warning", "Same account exists already! No changes were made.")
                return
            item_widget.update(new_name, new_keys["PUBLIC_KEY"])

            del self.system_accounts[name]
            self.system_accounts[new_name] = new_keys
    
    def prompt_add_config_to_list(self):
        dialog = ConfigDialog(self)

        if dialog.exec() == QDialog.Accepted:
            field, value = dialog.get_data()

            # Add to list
            if field in self.config:
                QMessageBox.warning(self, "Warning", "Same configuration exists already!")
                return
            
            self.config[field] = value                
            self.add_config_to_list(field, value)

    def add_config_to_list(self, field, value, required=False):
        item_widget = ConfigItemWidget(field, value, required)
        list_item = QListWidgetItem(self.config_listWidget)

        # Set item size
        list_item.setSizeHint(item_widget.sizeHint())

        self.config_listWidget.addItem(list_item)
        self.config_listWidget.setItemWidget(list_item, item_widget)

        # Connect buttons
        item_widget.remove_button.clicked.connect(lambda: self.remove_config_item(list_item))
        item_widget.edit_button.clicked.connect(lambda: self.edit_config_item(item_widget))
        
    def remove_config_item(self, item):
        row = self.config_listWidget.row(item)
        widget = self.config_listWidget.itemWidget(item)
        del self.config[widget.field]
        self.acc_listWidget.takeItem(row)

    def edit_config_item(self, item_widget):
        field = item_widget.field
        value = str(self.config[field])

        dialog = ConfigDialog(self)

        dialog.config_field_lineEdit.setText(field)
        dialog.config_value_lineEdit.setText(value)

        if item_widget.required:
            dialog.config_field_lineEdit.setEnabled(False)

        if dialog.exec() == QDialog.Accepted:
            new_field, new_value = dialog.get_data()
            if new_field != field and new_field in self.config:
                QMessageBox.warning(self, "Warning", "Same config exists already! No changes were made.")
                return
            item_widget.update(new_field, new_value)

            del self.config[field]
            self.config[field] = value

    def generate_key(self, item_widget):
        chain = Chain.get_instance()
        public, private = chain.create_key()
        self.system_accounts[item_widget.name.text()] = {"PUBLIC_KEY": public, "PRIVATE_KEY": private}
        item_widget.update(pubkey=public)


class TextDialog(QDialog, Ui_TextDialog):
    def __init__(self, text, file_name, parent=None):
        super().__init__(parent)
        self.file_name = file_name or ''
        self.setupUi(self)
        self.textEdit.setPlainText(text)

        # Connect the buttons
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save_to_file)
        self.buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.reject)

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Text",
            self.file_name,
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.textEdit.toPlainText())
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")


class AccDialog(QDialog, Ui_AccDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Connect the buttons
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

    # format - (NAME, {PUBKEY: value, PRIVKEY: value})
    def get_data(self):
        return(self.name_lineEdit.text(),
            {
                "PUBLIC_KEY": self.pubkey_lineEdit.text(),
                "PRIVATE_KEY": self.privkey_lineEdit.text()
            }
        )

class AccItemWidget(QWidget, Ui_AccItemWidget):
    def __init__(self, name, pubkey, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name.setText(name)
        self.pubkey.setText(pubkey)

    def update(self, name=None, pubkey=None):
        if name:
            self.name.setText(name)
        if pubkey:
            self.pubkey.setText(pubkey)

class ConfigDialog(QDialog, Ui_ConfigDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Connect the buttons
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

    def get_data(self):
        value = self.config_value_lineEdit.text()
        try:
            value = int(value)
        except ValueError:
            pass
        return(self.config_field_lineEdit.text(), value)
    
class ConfigItemWidget(QWidget, Ui_ConfigItemWidget):
    def __init__(self, field, value, required=False, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.config_value.setText(f'{field}: {value}')
        self.required = required
        self.field = field
        if required:
            self.remove_button.setEnabled(False)

    def update(self, field, value):
        self.config_value.setText(f'{field}: {value}')

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = Gui()
    window.show()

    app.exec()