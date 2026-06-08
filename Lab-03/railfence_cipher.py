import sys
import os
import re  # Sử dụng thư viện re để kiểm tra định dạng chữ cái tiếng Anh chuẩn
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import requests

try:
    from ui.railfence import Ui_MainWindow
except ImportError:
    from railfence import Ui_MainWindow

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        try:
            self.ui.pushButton.clicked.connect(self.call_api_encrypt)
            self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)
        except AttributeError as e:
            print(f"Lỗi kết nối nút bấm UI: {e}")

    def validate_input(self, text, key_str, mode="encrypt"):
        text_type = "Văn bản gốc (Plain Text)" if mode == "encrypt" else "Bản mã (Cipher Text)"
        clean_text = text.strip()
        
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
        if not key_str.strip():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Số hàng) không được để trống!")
            return False

        # 4. Kiểm tra xem khóa có phải là số hay không
        if not key_str.strip().isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa phải là một số nguyên hợp lệ!")
            return False

        key = int(key_str.strip())
        
        # 5. Kiểm tra điều kiện số hàng >= 2
        if key < 2:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa hàng rào (Số hàng) phải lớn hơn hoặc bằng 2!")
            return False

        # 6. Kiểm tra điều kiện logic: số hàng phải nhỏ hơn độ dài chuỗi
        if key >= len(clean_text):
            QMessageBox.warning(self, "Lỗi Logic", f"Số hàng ({key}) phải nhỏ hơn độ dài của văn bản cần xử lý ({len(clean_text)})!")
            return False

        return True

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        
        try:
            plain_text = self.ui.textEdit.toPlainText()
            key_str = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy cấu phần ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(plain_text, key_str, "encrypt"):
            return

        payload = {"plain_text": plain_text.strip(), "key": int(key_str.strip())}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_3.setText(data["encrypted_text"])
                QMessageBox.information(self, "Thành Công", "Mã hóa Rail Fence thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        
        try:
            cipher_text = self.ui.textEdit_3.toPlainText()
            key_str = self.ui.textEdit_2.toPlainText()
        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không tìm thấy cấu phần ô nhập liệu trên UI: {e}")
            return

        if not self.validate_input(cipher_text, key_str, "decrypt"):
            return

        payload = {"cipher_text": cipher_text.strip(), "key": int(key_str.strip())}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_text"])
                QMessageBox.information(self, "Thành Công", "Giải mã Rail Fence thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())