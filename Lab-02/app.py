from flask import Flask, render_template, request

from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher

app = Flask(__name__)

# Định nghĩa một hàm tiện ích để xuất thông báo lỗi đồng bộ, dễ nhìn
def render_error(message, back_url):
    return f"""
    <div style="font-family: Arial, sans-serif; margin: 50px auto; max-width: 600px; padding: 20px; border: 1px solid #f5c6cb; background-color: #f8d7da; color: #721c24; border-radius: 5px;">
        <h3 style="margin-top: 0;">⚠️ Lỗi dữ liệu đầu vào!</h3>
        <p>{message}</p>
        <hr style="border-top: 1px solid #f5c6cb;"/>
        <a href="{back_url}" style="color: #721c24; font-weight: bold; text-decoration: none;">← Quay lại để nhập lại</a>
    </div>
    """

@app.route("/")
def home():
    return render_template('index.html')


# ==================== CAESAR CIPHER ====================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    try:
        text = request.form['inputPlainText']
        key = int(request.form['inputKeyPlain'])
        cipher = CaesarCipher()
        encrypted_text = cipher.encrypt_text(text, key)
        return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/caesar")

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    try:
        text = request.form['inputCipherText']
        key = int(request.form['inputKeyCipher'])
        cipher = CaesarCipher()
        decrypted_text = cipher.decrypt_text(text, key)
        return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/caesar")


# ==================== VIGENERE CIPHER ====================
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        cipher = VigenereCipher()
        encrypted_text = cipher.encrypt_text(text, key)
        return f"Text gốc: {text}<br/>Key: {key}<br/>Mã hóa: {encrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/vigenere")

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        cipher = VigenereCipher()
        decrypted_text = cipher.decrypt_text(text, key)
        return f"Mã hóa: {text}<br/>Key: {key}<br/>Giải mã: {decrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/vigenere")


# ==================== RAIL FENCE CIPHER ====================
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    try:
        text = request.form['inputPlainText']
        # Đề phòng trường hợp nhập chữ vào ô số rớt vào lỗi ép kiểu int() trước khi vào thuật toán
        if not request.form['inputKeyPlain'].isdigit():
            raise ValueError("Số hàng rào phải là số nguyên, không được nhập chữ!")
            
        key = int(request.form['inputKeyPlain'])
        cipher = RailFenceCipher()
        encrypted_text = cipher.encrypt_text(text, key)
        return f"Text gốc: {text}<br/>Số hàng (Key): {key}<br/>Mã hóa: {encrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/railfence")

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    try:
        text = request.form['inputCipherText']
        if not request.form['inputKeyCipher'].isdigit():
            raise ValueError("Số hàng rào phải là số nguyên, không được nhập chữ!")
            
        key = int(request.form['inputKeyCipher'])
        cipher = RailFenceCipher()
        decrypted_text = cipher.decrypt_text(text, key)
        return f"Mã hóa: {text}<br/>Số hàng (Key): {key}<br/>Giải mã: {decrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/railfence")


# ==================== PLAYFAIR CIPHER ====================
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    try:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        cipher = PlayfairCipher()
        encrypted_text = cipher.encrypt_text(text, key)
        return f"Text gốc: {text}<br/>Key từ: {key}<br/>Mã hóa: {encrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/playfair")

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    try:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        cipher = PlayfairCipher()
        decrypted_text = cipher.decrypt_text(text, key)
        return f"Mã hóa: {text}<br/>Key từ: {key}<br/>Giải mã: {decrypted_text}"
    except ValueError as e:
        return render_error(str(e), "/playfair")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)