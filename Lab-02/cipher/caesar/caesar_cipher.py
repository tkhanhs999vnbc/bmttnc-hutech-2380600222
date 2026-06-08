from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        # Ràng buộc Key
        if not (1 <= key <= 25):
            raise ValueError("Key của Caesar phải nằm trong khoảng từ 1 đến 25!")
            
        alphabet_len = len(self.alphabet)
        text = text.upper()
        encrypted_text = []
        for letter in text:
            # Ràng buộc ký tự hợp lệ
            if letter not in self.alphabet:
                raise ValueError(f"Ký tự '{letter}' không nằm trong bảng chữ cái hỗ trợ!")
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index + key) % alphabet_len
            output_letter = self.alphabet[output_index]
            encrypted_text.append(output_letter)
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        if not (1 <= key <= 25):
            raise ValueError("Key của Caesar phải nằm trong khoảng từ 1 đến 25!")
            
        alphabet_len = len(self.alphabet)
        text = text.upper()
        decrypted_text = []
        for letter in text:
            if letter not in self.alphabet:
                raise ValueError(f"Ký tự '{letter}' không hợp lệ!")
            letter_index = self.alphabet.index(letter)
            output_index = (letter_index - key) % alphabet_len
            output_letter = self.alphabet[output_index]
            decrypted_text.append(output_letter)
        return "".join(decrypted_text)