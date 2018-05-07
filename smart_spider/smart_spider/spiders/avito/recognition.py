import requests
from lxml import html
from re import findall
from PIL import Image
import base64
from StringIO import StringIO
from collections import namedtuple
import sys

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
    image = Image.open(StringIO(base64.b64decode(base64_image))).convert('LA')
    left_margins = (2,13,20,27,39,46,53,65,73,84,92)
    DIGITS_BY_HIST = {44: '0', 16: '1',38: '2', 43: '3', 28: '4', 41: '5', 45: '6',25: '7', 53: '8', 47: '9'}
    digits=[]
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
    script = doc.xpath('//div[@class="clearfix" and @itemscope and @itemtype="http://schema.org/Product"]/script')
    if not script:
        return None
    script = script[0].text
    price, phone_hash = None, None

    for line in script.split('\n'):
        line = line.strip()
        if not line:
            continue

    var_name, var_value = [item.strip('\'";') for item in line.split(' = ')]
    if var_name=='avito.item.price':
        price = int(var_value)
    if var_name=='avito.item.phone':
        phone_hash = var_value
    pkey = get_image_pkey(ad_id, phone_hash)
    image_url = 'https://www.avito.ru/items/phone/{}?pkey={}'.format(ad_id,pkey)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'x-requested-with':'XMLHttpRequest', 'referer':url}
    image = s.get(image_url, headers=headers).json().get('image64')
    phone = None
    if image:
        base64_image = image.split(',')[1]
        phone = recognize(base64_image)

    result = Advertisement(ad_id, price, phone)
    return result

if __name__=='__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print "Parsing URL {}".format(url)
        ad = parse(url)

        if ad:
            print "Result: ID {}, phone {}, price {}.".format(ad.id,ad.phone, ad.price)
        else:
            print "Could not parse URL. "
    else:
        TEMPLATE = "{:10} | {:11} | {:>6}"
        print (TEMPLATE.format('ID','Phone','Price'))
        for url in URLS:
            ad = parse(url)
        if ad:
            print TEMPLATE.format(ad.id, ad.phone, ad.price)
        else:
            print TEMPLATE.format(None,None,None)
