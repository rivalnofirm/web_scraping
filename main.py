import requests
from bs4 import BeautifulSoup
import csv

key = input('please enter the term :')
location = input('please enter the location too :')
url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=802959918&keywords={}&location={}&pageNum='.format(
    key, location)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

data = []
count_page = 0
for page in range(1, 11):
    count_page += 1
    print('scraping page :', count_page)
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')
items = soup.findAll('div', 'row businessCapsule--mainRow')
for item in items:
    name = item.find('span', 'businessCapsule--name').text
    address = ''.join(
        item.find('span', {'itemprop': 'address'}).text.strip().split('\n'))
    try:
        web = item.find('a', {'rel': 'nofollow noopener'})['href'].replace(
            'http://', '').replace('www.', '').replace('https://', '').split('/')[0]
    except:
        web = ''
    try:
        telp = item.find('span', 'business--telephoneNumber').text
    except:
        telp = ''
    image = item.find(
        'div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
    if 'http' not in image:
        image = 'https://www.yell.com{}'.format(image)
    data.append([name, address, web, telp, image])

index = ['Name', 'Address', 'Website', 'Phone Number', 'Image URL']
writer = csv.writer(
    open('results/{}_{}.csv'.format(key, location), 'w', newline=''))
writer.writerow(index)
for d in datas:
    writer.writerow(d)
