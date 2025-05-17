
from app.core.config import settings
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

SECRET_KEY = settings.CRYPTO_JS_SECRET.encode("utf-8")  # ✅ 16-byte key

def decrypt_password(encrypted_password: str) -> str:
    raw = base64.b64decode(encrypted_password)
    iv = raw[:16]  # ✅ Extract IV
    ciphertext = raw[16:]  # ✅ Extract encrypted data

    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)

    print("Raw Decrypted Output:", decrypted)  # 🔥 Debug output before unpadding
    
    final = unpad(decrypted, AES.block_size).decode("utf-8")  # ✅ Remove padding
    return final
