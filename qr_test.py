from pyzbar import pyzbar
import numpy as np
import secrets
import qrcode
from PIL import Image
import requests
from io import BytesIO

def kpop_qr_creator(user_id, template):
    kpop_code = secrets.token_urlsafe(16)
    print(f'kpop_code: {kpop_code}')
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_Q,
        box_size=7,
        border=0
    )
    qr.add_data(kpop_code)
    qr.make(fit=True)

    qr_image = qr.make_image()
    qr_w, qr_h = qr_image.size
    print(f'width: {qr_w}, height: {qr_h}')
    template = Image.open(f'qr_codes/templates/{template}.png', 'r')
    template.paste(qr_image, (846, 368))
    template.save('qr_codes/output.png')



coupon_code = pyzbar.decode(coupon)
print(coupon_code)

    
#image = cv2.imdecode()