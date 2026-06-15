class VigenereCipher:
    def __init__(self):
        pass

    def encrypt_text(self, plain_text, key):
        # GIỮ NGUYÊN RÀNG BUỘC KEY: Bắt buộc phải là chữ cái và không rỗng
        if not key or not key.isalpha():
            raise ValueError("Key của Vigenere phải là chuỗi ký tự chữ cái và không được để trống!")
        return self.vigenere_encrypt(plain_text, key)

    def decrypt_text(self, encrypted_text, key):
        # GIỮ NGUYÊN RÀNG BUỘC KEY: Bắt buộc phải là chữ cái và không rỗng
        if not key or not key.isalpha():
            raise ValueError("Key của Vigenere phải là chuỗi ký tự chữ cái và không được để trống!")
        return self.vigenere_decrypt(encrypted_text, key)

    def vigenere_encrypt(self, plain_text, key):
        # ĐỒNG BỘ: Chuyển toàn bộ văn bản và key về chữ IN HOA
        plain_text = plain_text.upper()
        key = key.upper()
        
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                # Do plain_text đã .upper() nên lược bỏ phần check chữ thường (isupper/islower)
                encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                key_index += 1
            else:
                # KHÔNG RÀNG BUỘC TEXT: Số, khoảng trắng, ký tự đặc biệt được giữ nguyên
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        # ĐỒNG BỘ: Chuyển toàn bộ văn bản mật mã và key về chữ IN HOA
        encrypted_text = encrypted_text.upper()
        key = key.upper()
        
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(key[key_index % len(key)]) - ord('A')
                # Do encrypted_text đã .upper() nên tính toán đồng bộ chữ hoa
                decrypted_text += chr((ord(char) - ord('A') - key_shift) % 26 + ord('A'))
                key_index += 1
            else:
                # KHÔNG RÀNG BUỘC TEXT: Số, khoảng trắng, ký tự đặc biệt được giữ nguyên
                decrypted_text += char
        return decrypted_text