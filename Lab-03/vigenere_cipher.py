import sys
import os
import re  # Sử dụng thư viện re để kiểm tra định dạng chữ cái tiếng Anh chuẩn
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
        
        try:
            self.ui.pushButton.clicked.connect(self.call_api_encrypt)
            self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)
        except AttributeError as e:
            print(f"Lỗi kết nối nút bấm UI: {e}")

    def validate_input(self, text, key, mode="encrypt"):
        text_type = "Văn bản gốc (Plain Text)" if mode == "encrypt" else "Bản mã (Cipher Text)"
        clean_text = text.strip()
        clean_key = key.strip()

        # 1. Kiểm tra trống dữ liệu văn bản
        if not clean_text:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", f"{text_type} không được để trống!")
            return False

        # 2. RÀNG BUỘC VĂN BẢN: Chỉ chấp nhận chữ cái tiếng Anh không dấu và khoảng trắng
        if not re.match(r"^[a-zA-Z\s]+$", clean_text):
            QMessageBox.warning(
                self, 
                "Lỗi Nhập Liệu", 
                f"{text_type} chỉ được phép chứa các chữ cái tiếng Anh không dấu (A-Z, a-z).\n"
                "Vui lòng không nhập số, ký tự đặc biệt hoặc chữ tiếng Việt có dấu!"
            )
            return False

        # 3. Kiểm tra trống dữ liệu Khóa
        if not clean_key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Key) không được để trống!")
            return False

        # 4. RÀNG BUỘC KHÓA (KEY): Chỉ chấp nhận chữ cái tiếng Anh không dấu, KHÔNG chứa khoảng trắng hay ký tự lạ
        if not re.match(r"^[a-zA-Z]+$", clean_key):
            QMessageBox.warning(
                self, 
                "Lỗi Nhập Liệu", 
                "Khóa Vigenere chỉ được chứa các chữ cái tiếng Anh không dấu (A-Z, a-z).\n"
                "Vui lòng không nhập số, khoảng trắng hoặc chữ có dấu!"
            )
            return False

        return True

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        
        try:
            plain_text = self.ui.textEdit.toPlainText()
            key = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy cấu phần ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(plain_text, key, "encrypt"):
            return

        payload = {"plain_text": plain_text.strip(), "key": key.strip()}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_3.setText(data["encrypted_text"])
                QMessageBox.information(self, "Thành Công", "Mã hóa Vigenere thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        
        try:
            cipher_text = self.ui.textEdit_3.toPlainText()
            key = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy cấu phần ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(cipher_text, key, "decrypt"):
            return

        payload = {"cipher_text": cipher_text.strip(), "key": key.strip()}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_text"])
                QMessageBox.information(self, "Thành Công", "Giải mã Vigenere thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())