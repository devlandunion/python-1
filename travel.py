import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import math
import csv

baseUrl = "https://www.travelweekly.com"


def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)

    return html


def get_states_url(html):
    bsObject = BeautifulSoup(html, "lxml")

    stateUrls = []

    for ul_elem in bsObject.select('ul.results'):
        for li_elem in ul_elem.select('li'):
            link = li_elem.select('a')[0].get('href')
            name = li_elem.select('a')[0].text
            temp = { 'name': name, 'link': baseUrl + link }
            stateUrls.append(temp)
            with open('results/' + name + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter =',')
                writer.writerow(('City', 'Link'))
    
    return stateUrls


def get_cities_url(stateUrls):
    cityUrls = []

    for state in stateUrls:
        req = urllib.request.Request(state['link'], headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req)
        bsObject = BeautifulSoup(html, "lxml")

        for ul_elem in bsObject.select('ul.results'):
            for li_elem in ul_elem.select('li'):
                link = li_elem.select('a')[0].get('href')
                name = li_elem.select('a')[0].text
                temp = { 'state': state['name'], 'city': name, 'link': baseUrl + link }
                cityUrls.append(temp)

    return cityUrls


def get_washington_dc():
    hotelUrls = []
    name = 'Washington, DC'
    with open('results/' + name + '.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow(('City', 'Link'))

        link = 'https://www.travelweekly.com/Hotels/Washington-DC'
        city_url = { 'state': 'Washington, DC', 'city': 'Washington, DC', 'link': link }
        file_name = 'results/' + city_url['state'] + '.csv'

    try:
        html = get_html(city_url['link'])
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
            pageUrl = city_url['link'] + '?pg=' + str(index + 1)
            req = urllib.request.Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req)
            bsObject = BeautifulSoup(html, "lxml")

            for index, resultDiv in enumerate(bsObject.select('div.result')):
                link = baseUrl + resultDiv.find('a', {'class':'title'}).get('href')
                hotelUrls.append(link)
                write_hotels_csv(file_name, city_url['city'], link)

    except HTTPError as e:
        content = e.read()
        text = open('error.txt', 'a')
        text.write(str(content))


def get_hotels_url(cityUrls):
    hotelUrls = []

    for city_url in cityUrls:
        file_name = 'results/' + city_url['state'] + '.csv'

        try:
            html = get_html(city_url['link'])
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
                pageUrl = city_url['link'] + '?pg=' + str(index + 1)
                req = urllib.request.Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req)
                bsObject = BeautifulSoup(html, "lxml")

                for index, resultDiv in enumerate(bsObject.select('div.result')):
                    link = baseUrl + resultDiv.find('a', {'class':'title'}).get('href')
                    hotelUrls.append(link)
                    write_hotels_csv(file_name, city_url['city'], link)
        except HTTPError as e:
            content = e.read()
            text = open('error.txt', 'a')
            text.write(str(content))

    return hotelUrls


def write_hotels_csv(file_name, city_name, link):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow((city_name, link))


def main():
    targetUrl = "https://www.travelweekly.com/Hotels/Destinations"

    html = get_html(targetUrl)
    stateUrls = get_states_url(html)
    cityUrls = get_cities_url(stateUrls)
    hotelUrls = get_hotels_url(cityUrls)

    print(len(hotelUrls))

    # for city in stateUrls:
    #     print(city['name'])
    #     # print(city['city'])
    #     print(city['link'])
    #     print('\n')

def test():
    with open('test.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow(['city', 'Link'])
        writer.writerow(['New York', baseUrl])

if __name__ == '__main__':
    get_washington_dc()