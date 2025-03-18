import qrcode
import itsdangerous
import io
import base64
from flask import current_app


signer = itsdangerous.URLSafeTimedSerializer(current_app.secret_key)

# Generate token for cookie
def generate_token(user_id):
    return signer.dumps(user_id)

# Generate a URL containing the token
def generate_qr_code_url(user_id):
    token = generate_token(user_id)
    url = f"https://2613-130-88-226-14.ngrok-free.app/scan?token={token}"  # Replace with your actual URL
    return url

# Generate QR Code
def generate_qr_code_base64(user_id):
    url = generate_qr_code_url(user_id)
    
    # Create a QR code image
    img = qrcode.make(url)
    
    # Save the image in memory
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Convert the image to a base64 string
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
    
    return img_base64