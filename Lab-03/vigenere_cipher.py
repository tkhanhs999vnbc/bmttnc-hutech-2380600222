import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests

try:
    from ui.vigenere import Ui_MainWindow
except ImportError:
    from vigenere import Ui_MainWindow

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        payload = {
            "plain_text": self.ui.textEdit.toPlainText(),
            "key": self.ui.textEdit_2.toPlainText().strip()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_3.setText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Vigenere Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        payload = {
            "cipher_text": self.ui.textEdit_3.toPlainText(),
            "key": self.ui.textEdit_2.toPlainText().strip()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Vigenere Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())