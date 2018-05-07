import requests
from lxml import html
from re import findall
from PIL import Image
from io import BytesIO
import base64
from StringIO import StringIO
from collections import namedtuple
import sys
from selenium import webdriver
import codecs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


Advertisement = namedtuple('Advertisement','id price phone')

URLS = ['https://www.avito.ru/samara/kvartiry/3-k_kvartira_84_m_1010_et._1687747742',]

def get_image_pkey(ad_id, ad_phone):
    if ad_id and ad_phone:
        ad_subhash = findall(r'[0-9a-f]+', ad_phone)
        if int(ad_id) % 2 == 0:
            ad_subhash.reverse()
            ad_subhash = ''.join(ad_subhash)
    return ad_subhash[::3]

def recognize(base64_image):
    #image = Image.open(StringIO(base64.b64decode(base64_image))).convert('LA')
    #image.save("captcha.png", "PNG")
    #image = Image.open(StringIO(base64.b64decode(base64_image)))
    image = Image.open(BytesIO(base64.b64decode(base64_image))).convert('LA')
    image.save("captcha", 'png')
    image = image.convert('LA')
    left_margins = (2,13,20,27,39,46,53,65,73,84,92)
    DIGITS_BY_HIST = {44: '0', 16: '1',38: '2', 43: '3', 28: '4', 41: '5', 45: '6',25: '7', 53: '8', 47: '9'}
    digits=[]

    # The problem is here
    for index, left_margin in enumerate(left_margins, start=1):
        box = (left_margin,4, left_margin+6,14)
        digit = image.crop(box)
        characteristic = digit.histogram()[0]
        digits.append(DIGITS_BY_HIST.get(characteristic,'x'))
    return ''.join(digits)

def parse(url):
    ad_id = url.split('_')[-1]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    s = requests.Session()
    response = s.get(url, headers=headers)
    doc = html.fromstring(response.content)
    with open('current_url.html', 'w') as file_body:
        file_body.write(response.content)

    
    phone_hash = doc.xpath('//avito.item.phone')
    price = doc.xpath('//avito.item.price')
    """
    var_name, var_value = [item.strip('\'";') for item in line.split(' = ')]
    if var_name=='avito.item.price':
        price = int(var_value)
    if var_name=='avito.item.phone':
        phone_hash = var_value
    """
    pkey = get_image_pkey(ad_id, phone_hash)
    image_url = 'https://www.avito.ru/items/phone/{}?pkey={}'.format(ad_id,pkey)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'x-requested-with':'XMLHttpRequest', 'referer':url}
    print(image_url)
    image = s.get(image_url, headers=headers).json().get('image64')
    phone = None
    if image:
        base64_image = str(image.split(',')[1])
        phone = recognize(base64_image)

    result = Advertisement(ad_id, price, phone)
    return result

def smart_parse(url):
    #driver = webdriver.PhantomJS(executable_path='node_modules/phantomjs/bin/phantomjs') # or add to your PATH
    driver = webdriver.Chrome()
    driver.get(url)
    #driver.save_screenshot('screen.png') # save a screenshot to disk
    wait = WebDriverWait(driver, 12)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.item-phone-number.js-item-phone-number')))
    sbtn = driver.find_element_by_css_selector('div.item-phone-number.js-item-phone-number')
    
    print(sbtn.text + ' is being clicked')
    sbtn.click()
    print(sbtn.text + ' was being clicked like infa 100%')

    try:
        wait_ajax = WebDriverWait(driver, 15)
        element_ajax = wait_ajax.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-phone-big-number.js-item-phone-big-number > img"))
        )
        #print('element ajax ' + element_ajax.value_of_css_property('src'))
        #print element_ajax.get_attribute('src')
        image_src = element_ajax.get_attribute('src')
        #print (image_src)
        if image_src:
            base64_image = image_src.split(',')[1]
            print base64_image
            phone = recognize(base64_image)
            print 'and the phone is ' + phone
            #print('ajax element' + element_ajax.find_element_by_tag_name('img').get_attribute('src'))
    finally:
        driver.quit()
    #print(sbtn.location)
    # item-phone-big-number js-item-phone-big-number

    #with codecs.open('ajax_url.html', 'w', 'utf-8') as ajax_body:
    #    ajax_body.write(driver.page_source)

if __name__=='__main__':
    #TEMPLATE = "{:10} | {:11} | {:>6}"
    #print (TEMPLATE.format('ID','Phone','Price'))
    for url in URLS:
        #ad = parse(url)
        smart_parse(url)
    #if ad:
    #    print TEMPLATE.format(ad.id, ad.phone, ad.price)
    #else:
    #    print TEMPLATE.format(None,None,None)
