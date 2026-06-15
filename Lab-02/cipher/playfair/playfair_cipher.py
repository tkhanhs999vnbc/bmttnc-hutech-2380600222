class PlayfairCipher: 
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = "".join([c for c in key if c.isalpha()])
        key = key.replace("J", "I")
        key = key.upper()
        
        unique_key = []
        for letter in key:
            if letter not in unique_key:
                unique_key.append(letter)
                
        key_set = set(unique_key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set
        ]
        matrix = unique_key.copy()

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break

        playfair_matrix = [matrix[i : i + 5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return 0, 0

    def encrypt_text(self, plain_text, key):
        # GIỮ NGUYÊN RÀNG BUỘC KEY: Phải chứa chữ cái để tạo ma trận
        if not key or not "".join([c for c in key if c.isalpha()]):
            raise ValueError("Key của Playfair phải chứa các ký tự chữ cái!")
            
        matrix = self.create_playfair_matrix(key)
        plain_text = plain_text.upper().replace("J", "I")
        
        # ĐÃ SỬA: Không xóa ký tự đặc biệt/số, mà ghi nhớ lại vị trí của chúng
        non_alpha_positions = [(idx, char) for idx, char in enumerate(plain_text) if not char.isalpha()]
        pure_letters = [char for char in plain_text if char.isalpha()]
        
        # Chuẩn bị các cặp chữ để mã hóa
        prepared_letters = []
        i = 0
        while i < len(pure_letters):
            prepared_letters.append(pure_letters[i])
            if i + 1 < len(pure_letters):
                if pure_letters[i] == pure_letters[i+1]:
                    prepared_letters.append("X")
                    i += 1
                else:
                    prepared_letters.append(pure_letters[i+1])
                    i += 2
            else:
                prepared_letters.append("X")
                i += 1

        encrypted_letters = []
        for i in range(0, len(prepared_letters), 2):
            pair = prepared_letters[i : i + 2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                encrypted_letters.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:
                encrypted_letters.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
            else:
                encrypted_letters.append(matrix[row1][col2] + matrix[row2][col1])

        # Chuyển danh sách cặp đã mã hóa thành chuỗi các ký tự
        result = list("".join(encrypted_letters))
        
        # Chèn trả số, khoảng trắng, ký tự đặc biệt về đúng vị trí cũ
        for pos, char in non_alpha_positions:
            if pos >= len(result):
                result.append(char)
            else:
                result.insert(pos, char)
                
        return "".join(result)

    def decrypt_text(self, cipher_text, key):
        # GIỮ NGUYÊN RÀNG BUỘC KEY: Phải chứa chữ cái để tạo ma trận
        if not key or not "".join([c for c in key if c.isalpha()]):
            raise ValueError("Key của Playfair phải chứa các ký tự chữ cái!")
            
        matrix = self.create_playfair_matrix(key)
        cipher_text = cipher_text.upper()
        
        # ĐÃ SỬA: Tương tự hàm mã hóa, ghi nhớ lại vị trí ký tự không phải chữ
        non_alpha_positions = [(idx, char) for idx, char in enumerate(cipher_text) if not char.isalpha()]
        pure_letters = [char for char in cipher_text if char.isalpha()]
        
        decrypted_letters = []
        for i in range(0, len(pure_letters), 2):
            pair = pure_letters[i : i + 2]
            if len(pair) < 2: 
                decrypted_letters.append(pair[0])
                break
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_letters.append(matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                decrypted_letters.append(matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2])
            else:
                decrypted_letters.append(matrix[row1][col2] + matrix[row2][col1])
                
        # Chuyển danh sách cặp đã giải mã thành chuỗi các ký tự
        result = list("".join(decrypted_letters))
        
        # Chèn trả số, khoảng trắng, ký tự đặc biệt về đúng vị trí cũ
        for pos, char in non_alpha_positions:
            if pos >= len(result):
                result.append(char)
            else:
                result.insert(pos, char)
                
        return "".join(result)