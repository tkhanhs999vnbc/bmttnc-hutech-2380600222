import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests

try:
    from ui.playfair import Ui_MainWindow
except ImportError:
    from playfair import Ui_MainWindow

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        
        plain_text = self.ui.textEdit.toPlainText().strip()
        key_text = self.ui.textEdit_2.toPlainText().strip()

        if not key_text or not plain_text:
            QMessageBox.warning(self, "Warning", "Please enter Plain Text and Key!")
            return

        payload = {
            "plain_text": plain_text,
            "key": key_text
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_3.setText(data["encrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Playfair Encrypted Successfully")
                msg.exec_()
            else:
                print("Server error code: %s" % response.status_code)
                QMessageBox.critical(self, "Server Error", "Server failed to encrypt. Check backend.")
        except requests.exceptions.RequestException as e:
            print("Network Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        
        cipher_text = self.ui.textEdit_3.toPlainText().strip()
        key_text = self.ui.textEdit_2.toPlainText().strip()

        if not key_text or not cipher_text:
            QMessageBox.warning(self, "Warning", "Please enter Cipher Text and Key!")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key_text
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_text"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Playfair Decrypted Successfully")
                msg.exec_()
            else:
                print("Server error code: %s" % response.status_code)
                QMessageBox.critical(self, "Server Error", "Server failed to decrypt. Check backend.")
        except requests.exceptions.RequestException as e:
            print("Network Error: %s" % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())