import sys
import os
import re  # Sử dụng thư viện re để kiểm tra định dạng
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

        # ĐÃ XÓA: Bỏ hoàn toàn mục "2. RÀNG BUỘC VĂN BẢN" chặn số và ký tự đặc biệt cũ để thả tự do văn bản.

        # 3. Kiểm tra trống dữ liệu Khóa
        if not clean_key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Key) không được để trống!")
            return False

        # 4. GIỮ NGUYÊN RÀNG BUỘC KHÓA (KEY): Bắt buộc phải có chữ cái tiếng Anh để khởi tạo ma trận 5x5
        if not re.search(r"[a-zA-Z]", clean_key):
            QMessageBox.warning(
                self, 
                "Lỗi Nhập Liệu", 
                "Khóa Playfair bắt buộc phải chứa ký tự chữ cái tiếng Anh (A-Z, a-z) để khởi tạo ma trận!"
            )
            return False

        # Lọc lại chuỗi khóa viết hoa để kiểm tra logic ma trận như code cũ của bạn
        upper_key = re.sub(r'[^A-Z]', '', clean_key.upper())
        if not upper_key:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa Playfair phải chứa ít nhất một ký tự chữ cái hợp lệ!")
            return False

        # 5. GIỮ NGUYÊN RÀNG BUỘC GIẢI MÃ: Tổng số chữ cái thuần túy để giải mã bắt buộc phải là số chẵn
        if mode == "decrypt":
            upper_cipher = re.sub(r'[^A-Z]', '', clean_text.upper())
            if len(upper_cipher) % 2 != 0:
                QMessageBox.warning(
                    self, 
                    "Lỗi Định Dạng", 
                    "Bản mã Playfair không hợp lệ! Tổng số lượng các chữ cái trong văn bản bắt buộc phải là một số chẵn để chia cặp."
                )
                return False

        return True

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        
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
                QMessageBox.information(self, "Thành Công", "Mã hóa Playfair thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        
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
                QMessageBox.information(self, "Thành Công", "Giải mã Playfair thành công!")
            else:
                QMessageBox.critical(self, "Lỗi Server", f"Server phản hồi mã lỗi: {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Mạng", f"Không thể kết nối đến Server Flask!\nChi tiết: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())