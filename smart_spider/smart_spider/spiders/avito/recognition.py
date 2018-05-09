import os
import sys
import json
import requests
from lxml import html
from re import findall
from PIL import Image
from io import BytesIO
import base64
from StringIO import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from base64 import decodestring


URLS = ['https://www.avito.ru/samara/kvartiry/3-k_kvartira_84_m_1010_et._1687747742',]

def get_image_pkey(ad_id, ad_phone):
    if ad_id and ad_phone:
        ad_subhash = findall(r'[0-9a-f]+', ad_phone)
        if int(ad_id) % 2 == 0:
            ad_subhash.reverse()
            ad_subhash = ''.join(ad_subhash)
    return ad_subhash[::3]

def recognize(base64_image):
    with open("captcha.png","wb") as f:
        f.write(decodestring(base64_image))

    image = Image.open("captcha.png").convert('LA')

    left_margins = (2,13,20,27,39,46,53,65,73,84,92)
    DIGITS_BY_HIST = {44: '0', 16: '1',38: '2', 43: '3', 28: '4', 41: '5', 45: '6',25: '7', 53: '8', 47: '9'}
    digits=[]

    # The problem is here
    for index, left_margin in enumerate(left_margins, start=1):
        box = (left_margin,4, left_margin+6,14)
        digit = image.crop(box)
        characteristic = digit.histogram()[0]
        print (index, characteristic)
        digits.append(DIGITS_BY_HIST.get(characteristic,'x'))
    return ''.join(digits)


def smart_parse(uri):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/force-download, image/png, text/html, text/plain, "
                           "image/tiff, text/csv, application/zip, application/octet-stream")
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting",
                           False)
    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'
    opts = webdriver.firefox.options.Options()
    opts.add_argument('-headless')
    driver = webdriver.Firefox(firefox_profile=profile, executable_path='geckodriver', firefox_options=opts)
    #driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))
    #driver = webdriver.PhantomJS(executable_path='phantomjs/bin/phantomjs') # or add to your PATH
    #profile = webdriver.FirefoxProfile()
    #driver = webdriver.Firefox(profile, log_path='firefox.log')
    #driver = webdriver.Firefox(executable_path='geckodriver')

    driver.get(uri)
    wait = WebDriverWait(driver, 8)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.item-phone-number.js-item-phone-number')))
    sbtn = driver.find_element_by_css_selector('div.item-phone-number.js-item-phone-number')

    print(sbtn.text + ' is being clicked')
    sbtn.click()
    print(sbtn.text + ' was being clicked like infa 100%')

    try:
        wait_ajax = WebDriverWait(driver, 8)
        element_ajax = wait_ajax.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-phone-big-number.js-item-phone-big-number > img"))
        )

        image_src = element_ajax.get_attribute('src')
        if image_src:
            base64_image = image_src.split(',')[1]
            phone = recognize(base64_image)
            print ('and the phone is ' + phone)
    finally:
        driver.quit()

if __name__=='__main__':
    for url in URLS:
        smart_parse(url)
        
