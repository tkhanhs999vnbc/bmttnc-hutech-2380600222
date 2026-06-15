from flask import Flask, render_template, request, jsonify
from io import BytesIO
import base64
import os
import subprocess
from PIL import Image

from cipher.caesar.caesar_cipher import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayfairCipher

app = Flask(__name__)

@app.route("/api/process", methods=["POST"])
def api_process():
    data = request.json
    algo = data.get("algorithm")
    action = data.get("action")
    text = data.get("text")
    key = data.get("key")
    
    try:
        if algo == "caesar":
            cipher = CaesarCipher()
            key = int(key)
            if action == "encrypt":
                return jsonify(success=True, result=cipher.encrypt_text(text, key))
            else:
                return jsonify(success=True, result=cipher.decrypt_text(text, key))
        elif algo == "vigenere":
            cipher = VigenereCipher()
            if action == "encrypt":
                return jsonify(success=True, result=cipher.encrypt_text(text, key))
            else:
                return jsonify(success=True, result=cipher.decrypt_text(text, key))
        elif algo == "railfence":
            cipher = RailFenceCipher()
            key = int(key)
            if action == "encrypt":
                return jsonify(success=True, result=cipher.encrypt_text(text, key))
            else:
                return jsonify(success=True, result=cipher.decrypt_text(text, key))
        elif algo == "playfair":
            cipher = PlayfairCipher()
            if action == "encrypt":
                return jsonify(success=True, result=cipher.encrypt_text(text, key))
            else:
                return jsonify(success=True, result=cipher.decrypt_text(text, key))
        else:
            return jsonify(success=False, error="Unknown algorithm")
    except Exception as e:
        return jsonify(success=False, error=str(e))


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


# ==================== STEGANOGRAPHY ====================
def encode_image(image_file, message):
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    message += '[EOF]'
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    data_index = 0
    msg_len = len(binary_message)
    pixels = img.load()
    
    for row in range(height):
        for col in range(width):
            if data_index < msg_len:
                r, g, b = pixels[col, row]
                
                if data_index < msg_len:
                    r = int(format(r, '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                if data_index < msg_len:
                    g = int(format(g, '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                if data_index < msg_len:
                    b = int(format(b, '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                    
                pixels[col, row] = (r, g, b)
            else:
                break
        if data_index >= msg_len:
            break
            
    return img

def decode_image(image_file):
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    
    binary_message = ""
    pixels = img.load()
    
    for row in range(height):
        for col in range(width):
            r, g, b = pixels[col, row]
            binary_message += format(r, '08b')[-1]
            binary_message += format(g, '08b')[-1]
            binary_message += format(b, '08b')[-1]
            
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))
        if message.endswith('[EOF]'):
            return message[:-5]
            
    return message

@app.route("/api/stego/encode", methods=["POST"])
def stego_encode():
    if 'image' not in request.files:
        return jsonify(success=False, error="Không tìm thấy file ảnh")
    
    image_file = request.files['image']
    text = request.form.get('text', '')
    
    if not text:
        return jsonify(success=False, error="Vui lòng nhập nội dung cần giấu")
        
    try:
        encoded_img = encode_image(image_file, text)
        img_io = BytesIO()
        encoded_img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify(success=True, image_base64=img_base64)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route("/api/stego/decode", methods=["POST"])
def stego_decode():
    if 'image' not in request.files:
        return jsonify(success=False, error="Không tìm thấy file ảnh")
        
    image_file = request.files['image']
    
    try:
        decoded_text = decode_image(image_file)
        return jsonify(success=True, result=decoded_text)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route("/launch_lab03/<algo>", methods=["POST"])
def launch_lab03(algo):
    try:
        lab03_dir = r"m:\THBMTTNC\Lab-03"
        scripts = {
            "caesar": "caesar_cipher.py",
            "vigenere": "vigenere_cipher.py",
            "railfence": "railfence_cipher.py",
            "playfair": "playfair_cipher.py"
        }
        
        if algo in scripts:
            script_path = os.path.join(lab03_dir, scripts[algo])
            subprocess.Popen(["python", script_path], cwd=lab03_dir)
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Algorithm not found")
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
