import sys
import os
import re  # Sử dụng thư viện re để đếm chữ cái và kiểm tra định dạng Key
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

        # ĐÃ XÓA: Bỏ hoàn toàn mục "2. RÀNG BUỘC VĂN BẢN" để người dùng nhập chữ, số, ký tự đặc biệt tự do

        # 3. Kiểm tra trống dữ liệu Khóa
        if not key_str.strip():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa (Số hàng) không được để trống!")
            return False

        # 4. Kiểm tra định dạng Khóa (phải là số nguyên dương)
        if not key_str.strip().isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa hàng rào phải là một số nguyên dương hợp lệ!")
            return False

        key = int(key_str.strip())
        
        # 5. Kiểm tra điều kiện số hàng >= 2
        if key < 2:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Khóa hàng rào (Số hàng) phải lớn hơn hoặc bằng 2!")
            return False

        # 6. SỬA ĐỔI LOGIC MỚI: Đếm số chữ cái thực tế (bỏ qua số, khoảng trắng, ký tự đặc biệt)
        pure_letters = [char for char in clean_text if char.isalpha()]
        letter_count = len(pure_letters)

        if key >= letter_count:
            QMessageBox.warning(
                self, 
                "Lỗi Logic", 
                f"Số hàng rào ({key}) phải nhỏ hơn số lượng chữ cái thực tế cần mã hóa trong văn bản ({letter_count} chữ)!\n"
                "Nếu không, thuật toán zigzag sẽ không thể thực hiện."
            )
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