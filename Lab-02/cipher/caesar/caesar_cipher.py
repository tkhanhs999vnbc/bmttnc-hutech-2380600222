from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def encrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet) # 26
        
        # RÀNG BUỘC CHUẨN: Chặn số 0 và chặn luôn tất cả các số chia hết cho 26 (vì làm dư bằng 0, chữ giữ nguyên)
        if key == 0 or key % alphabet_len == 0:
            raise ValueError("Key không được bằng 0 hoặc chia hết cho 26 (vì sẽ làm văn bản giữ nguyên)!")
            
        # Khi đã vượt qua kiểm tra trên, chắc chắn dư sẽ từ 1 đến 25 (hoặc từ -1 đến -25)
        effective_key = key % alphabet_len
            
        text = text.upper()
        encrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index + effective_key) % alphabet_len
                encrypted_text.append(self.alphabet[output_index])
            else:
                encrypted_text.append(letter) 
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        
        # Áp dụng tương tự cho hàm giải mã
        if key == 0 or key % alphabet_len == 0:
            raise ValueError("Key không được bằng 0 hoặc chia hết cho 26 (vì sẽ làm văn bản giữ nguyên)!")
            
        effective_key = key % alphabet_len
            
        text = text.upper()
        decrypted_text = []
        for letter in text:
            if letter in self.alphabet:
                letter_index = self.alphabet.index(letter)
                output_index = (letter_index - effective_key) % alphabet_len
                decrypted_text.append(self.alphabet[output_index])
            else:
                decrypted_text.append(letter)
        return "".join(decrypted_text)