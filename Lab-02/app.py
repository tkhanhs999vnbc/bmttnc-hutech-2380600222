from flask import Flask, render_template, request

from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

# ==================== CAESAR CIPHER ====================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = CaesarCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = CaesarCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


# ==================== VIGENERE CIPHER ====================
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = VigenereCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Text gốc: {text}<br/>Key: {key}<br/>Mã hóa: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = VigenereCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Mã hóa: {text}<br/>Key: {key}<br/>Giải mã: {decrypted_text}"


# ==================== RAIL FENCE CIPHER ====================
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    cipher = RailFenceCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Text gốc: {text}<br/>Số hàng (Key): {key}<br/>Mã hóa: {encrypted_text}"

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = RailFenceCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Mã hóa: {text}<br/>Số hàng (Key): {key}<br/>Giải mã: {decrypted_text}"


# ==================== PLAYFAIR CIPHER ====================
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = PlayfairCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Text gốc: {text}<br/>Key từ: {key}<br/>Mã hóa: {encrypted_text}"

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = PlayfairCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Mã hóa: {text}<br/>Key từ: {key}<br/>Giải mã: {decrypted_text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)