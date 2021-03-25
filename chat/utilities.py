import base64
from django.core.files.base import ContentFile
from datetime import datetime


def decode_img_binary(data, format):
    imgstr = data.encode('utf-8')
    image = ContentFile(
        base64.decodebytes(imgstr), name=datetime.now().strftime('%H%M%S') + '.' + format)
    return image


def encode_img_binary(image_file):
    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return str(encoded_string)
