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
        if not key or not "".join([c for c in key if c.isalpha()]):
            raise ValueError("Key của Playfair phải chứa các ký tự chữ cái!")
            
        plain_text = "".join([c for c in plain_text if c.isalpha()])
        matrix = self.create_playfair_matrix(key)
        
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        encrypted_text = ""

        for i in range(0, len(plain_text), 2):
            pair = plain_text[i : i + 2]
            if len(pair) == 1:
                pair += "X"
            elif pair[0] == pair[1]:
                pair = pair[0] + "X"
                plain_text = plain_text[:i+1] + "X" + plain_text[i+1:]
                
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += (
                    matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
                )
            elif col1 == col2:
                encrypted_text += (
                    matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
                )
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def decrypt_text(self, cipher_text, key):
        if not key or not "".join([c for c in key if c.isalpha()]):
            raise ValueError("Key của Playfair phải chứa các ký tự chữ cái!")
            
        cipher_text = "".join([c for c in cipher_text if c.isalpha()])
        matrix = self.create_playfair_matrix(key)
        
        cipher_text = cipher_text.upper()
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i : i + 2]
            if len(pair) < 2: break
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += (
                    matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
                )
            elif col1 == col2:
                decrypted_text += (
                    matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
                )
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        return decrypted_text