from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        # LUẬT MỚI: Key bắt buộc phải nằm trong khoảng [-25, 25] và không được bằng 0
        if key == 0 or not (-25 <= key <= 25):
            raise ValueError("Key của Caesar phải nằm trong khoảng từ -25 đến 25 (và khác 0)!")
            
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_text = []
        for letter in text:
            # Ràng buộc ký tự hợp lệ
            if letter not in self.alphabet:
                raise ValueError(f"Ký tự '{letter}' không nằm trong bảng chữ cái hỗ trợ!")
            
            letter_index = self.alphabet.index(letter)
            # Phép % xử lý hoàn hảo cho cả key dương và key âm trong khoảng [-25, 25]
            output_index = (letter_index + key) % alphabet_len
            output_letter = self.alphabet[output_index]
            encrypted_text.append(output_letter)
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        # LUẬT MỚI: Áp dụng tương tự cho hàm giải mã
        if key == 0 or not (-25 <= key <= 25):
            raise ValueError("Key của Caesar phải nằm trong khoảng từ -25 đến 25 (và khác 0)!")
            
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_text = []
        for letter in text:
            if letter not in self.alphabet:
                raise ValueError(f"Ký tự '{letter}' không hợp lệ!")
            
            letter_index = self.alphabet.index(letter)
            # Giải mã dịch ngược lại bằng cách trừ key
            output_index = (letter_index - key) % alphabet_len
            output_letter = self.alphabet[output_index]
            decrypted_text.append(output_letter)
        return "".join(decrypted_text)