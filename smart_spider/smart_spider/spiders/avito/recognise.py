import pytesseract
import os

from PIL import Image
from base64 import decodestring


MY_DIR = os.path.abspath(os.path.dirname(__file__))
CAPTCHA_DIR = os.path.join(MY_DIR, 'captcha')


def recognise_captcha(base64_image):
    #with open("captcha.png", "wb") as f:
    #    f.write(decodestring(base64_image))

    #image = Image.open("captcha.png").convert('LA')
    #print pytesseract.image_to_string(image)

    #captcha_path = os.path.join(CAPTCHA_DIR, image_name)
    captcha_image = Image.open(decodestring(base64_image))
    recognised = pytesseract.image_to_string(captcha_image)
    integers_only = int(recognised)
    return integers_only

