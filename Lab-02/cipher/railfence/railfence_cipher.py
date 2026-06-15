class RailFenceCipher:
    def __init__(self):
        pass

    def encrypt_text(self, plain_text, num_rails):
        # Kiểm tra nếu key không phải là số hoặc nhỏ hơn 2
        if not isinstance(num_rails, int) or num_rails < 2:
            raise ValueError("Số hàng rào (Key) của Rail Fence phải là số nguyên lớn hơn hoặc bằng 2!")
        return self.rail_fence_encrypt(plain_text, num_rails)

    def decrypt_text(self, cipher_text, num_rails):
        # Kiểm tra nếu key không phải là số hoặc nhỏ hơn 2
        if not isinstance(num_rails, int) or num_rails < 2:
            raise ValueError("Số hàng rào (Key) của Rail Fence phải là số nguyên lớn hơn hoặc bằng 2!")
        return self.rail_fence_decrypt(cipher_text, num_rails)

    def rail_fence_encrypt(self, plain_text, num_rails):
        plain_text = plain_text.upper()
        
        # Tách ký tự đặc biệt/số và chữ cái
        non_alpha_positions = [(idx, char) for idx, char in enumerate(plain_text) if not char.isalpha()]
        pure_letters = [char for char in plain_text if char.isalpha()]
        
        # RÀNG BUỘC MỚI: Key phải nhỏ hơn số lượng chữ cái thực tế cần mã hóa
        if num_rails >= len(pure_letters):
            raise ValueError(f"Key ({num_rails}) phải nhỏ hơn số lượng ký tự chữ cái thực tế ({len(pure_letters)})!")

        # Chạy thuật toán hàng rào zigzag
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1
        for letter in pure_letters:
            rails[rail_index].append(letter)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
            
        encrypted_letters = list(''.join(''.join(rail) for rail in rails))
        
        # Chèn trả các ký tự số và khoảng trắng về đúng vị trí ban đầu
        for pos, char in non_alpha_positions:
            if pos >= len(encrypted_letters):
                encrypted_letters.append(char)
            else:
                encrypted_letters.insert(pos, char)
                
        return ''.join(encrypted_letters)

    def rail_fence_decrypt(self, cipher_text, num_rails):
        cipher_text = cipher_text.upper()
        
        # Tách ký tự đặc biệt/số và chữ cái
        non_alpha_positions = [(idx, char) for idx, char in enumerate(cipher_text) if not char.isalpha()]
        pure_letters = [char for char in cipher_text if char.isalpha()]
        
        # RÀNG BUỘC MỚI: Key phải nhỏ hơn số lượng chữ cái khi giải mã
        if num_rails >= len(pure_letters):
            raise ValueError(f"Key ({num_rails}) phải nhỏ hơn số lượng ký tự chữ cái thực tế ({len(pure_letters)})!")

        num_letters = len(pure_letters)
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(num_letters):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rails = []
        start = 0
        pure_text_str = "".join(pure_letters)
        for length in rail_lengths:
            rails.append(pure_text_str[start:start + length])
            start += length

        decrypted_letters = []
        rail_index = 0
        direction = 1

        for _ in range(num_letters):
            decrypted_letters.append(rails[rail_index][0])
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Chèn trả các ký tự số và khoảng trắng về lại vị trí cũ
        for pos, char in non_alpha_positions:
            if pos >= len(decrypted_letters):
                decrypted_letters.append(char)
            else:
                decrypted_letters.insert(pos, char)

        return "".join(decrypted_letters)