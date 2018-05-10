from PIL import Image
import pytesseract
import os


my_path = os.path.abspath(os.path.dirname(__file__))
captcha_path = os.path.join(my_path, "captcha.png")

print (captcha_path)
captcha_image = Image.open(captcha_path)
print (pytesseract.image_to_string(captcha_image))
# print(phone)
#print(fancy_way)
