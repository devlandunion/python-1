import urllib.request
from bs4 import BeautifulSoup
import math

baseUrl = "https://www.travelweekly.com"
cityUrl = "https://www.travelweekly.com/Hotels/Miami-Springs-FL"

req = urllib.request.Request(cityUrl, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req)
bsObject = BeautifulSoup(html, "lxml")

info_str = []
info_str = bsObject.find('div', {'class':'results'}).text.strip().lower().split(" ")

if(len(info_str) == 1):
    number_of_pages = 0
else:
    info_str.reverse()
    number_of_hotels = int(info_str[1])

    if(number_of_hotels < 15):
        number_of_hotels = 10

    number_of_pages = math.ceil(number_of_hotels/10)

for index in range(0, number_of_pages):
    pageUrl = cityUrl + '?pg=' + str(index + 1)
    req = urllib.request.Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    bsObject = BeautifulSoup(html, "lxml")

    for index, resultDiv in enumerate(bsObject.select('div.result')):
        link = baseUrl + resultDiv.find('a', {'class':'title'}).get('href')
        print(link)