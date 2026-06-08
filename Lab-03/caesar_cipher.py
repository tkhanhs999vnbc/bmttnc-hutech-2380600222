import sys
import os
import re  # Sử dụng thư viện re để kiểm tra định dạng chữ cái tiếng Anh
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests

try:
    from ui.caesar import Ui_MainWindow
except ImportError:
    from caesar import Ui_MainWindow

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

class CaesarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        try:
            self.ui.pushButton.clicked.connect(self.call_api_encrypt)
            self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)
        except AttributeError as e:
            print(f"Lỗi kết nối nút bấm: {e}")

    def validate_input(self, text, key_str, mode="encrypt"):
        text_type = "Văn bản gốc (Plain Text)" if mode == "encrypt" else "Bản mã (Cipher Text)"
        clean_text = text.strip()
        
        if not clean_text:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", f"{text_type} không được để trống!")
            return False
            
        # RÀNG BUỘC CHẶN CHỮ CÓ DẤU, SỐ VÀ KÝ TỰ ĐẶC BIỆT:
        if not re.match(r"^[a-zA-Z\s]+$", clean_text):
            QMessageBox.warning(
                self, 
                "Lỗi Nhập Liệu", 
                f"{text_type} chỉ được phép chứa các chữ cái tiếng Anh không dấu (A-Z, a-z).\n"
                "Vui lòng không nhập số, ký tự đặc biệt hoặc chữ tiếng Việt có dấu (như ư, á, à, ó...)!"
            )
            return False
            
        clean_key = key_str.strip()
        if not clean_key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Key) không được để trống!")
            return False

        # ĐÃ SỬA: Thay thế .isdigit() bằng Regex hỗ trợ dấu âm (-) ở đầu
        # ^-?\d+$ có nghĩa là: có thể có hoặc không có dấu trừ, theo sau bắt buộc là các chữ số
        if not re.match(r"^-?\d+$", clean_key):
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa phải là một số nguyên hợp lệ (ví dụ: 3 hoặc -3)!")
            return False

        key = int(clean_key)
        
        # ĐÃ SỬA: Luật mới chặn số 0 và giới hạn độ lớn từ -25 đến 25
        if key == 0 or not (-25 <= key <= 25):
            QMessageBox.warning(
                self, 
                "Lỗi Nhập Liệu", 
                "Khóa dịch chuyển mật mã Caesar phải nằm trong khoảng từ -25 đến 25 và phải khác 0!"
            )
            return False

        return True

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        
        try:
            plain_text = self.ui.textEdit.toPlainText()
            key_str = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(plain_text, key_str, "encrypt"):
            return

        payload = {"plain_text": plain_text.strip(), "key": int(key_str.strip())}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_3.setText(data["encrypted_message"])
                QMessageBox.information(self, "Thành Công", "Mã hóa Caesar thành công!")
            else:
                data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                error_msg = data.get("error", f"Server phản hồi mã lỗi: {response.status_code}")
                QMessageBox.critical(self, "Lỗi Server", error_msg)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        
        try:
            cipher_text = self.ui.textEdit_3.toPlainText()
            key_str = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(cipher_text, key_str, "decrypt"):
            return

        payload = {"cipher_text": cipher_text.strip(), "key": int(key_str.strip())}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_message"])
                QMessageBox.information(self, "Thành Công", "Giải mã Caesar thành công!")
            else:
                data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                error_msg = data.get("error", f"Server phản hồi mã lỗi: {response.status_code}")
                QMessageBox.critical(self, "Lỗi Server", error_msg)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarApp()
    window.show()
    sys.exit(app.exec_())