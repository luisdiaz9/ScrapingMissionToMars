# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

def init_browser(): 
    exec_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

DataToHTML = {}

def scrape_last():
    try: 
        browser = init_browser()
        browser.is_element_present_by_css("div.content_title", wait_time=1)
        url_last = 'https://mars.nasa.gov/news/'
        browser.visit(url_last)
        html_last = browser.html
        soup = BeautifulSoup(html_last, 'html.parser')
        DataToHTML['header_last'] = soup.find('div', class_='content_title').find('a').text
        DataToHTML['content_last'] = soup.find('div', class_='article_teaser_body').text
        return DataToHTML
    finally:
        browser.quit()

def scrape_img():
    try: 
        browser = init_browser()
        url_main_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_main_img)
        html_main_img = browser.html
        soup = BeautifulSoup(html_main_img, 'html.parser')
        complement_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        root_main_img = 'https://www.jpl.nasa.gov'
        DataToHTML['url_main_img_final'] = root_main_img + complement_image_url
        return DataToHTML
    finally:
        browser.quit()

def scrape_msg():

    try: 
        browser = init_browser()
        url_pressure = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_pressure)
        html_pressure = browser.html
        soup = BeautifulSoup(html_pressure, 'html.parser')
        text_msg = soup.find_all('div', class_='js-tweet-text-container')
        for msg in text_msg: 
            aux = msg.find('p').text
            if 'sol' and 'pressure' in aux:
                DataToHTML['msg'] = aux
                break
            else: 
                pass
        return DataToHTML
    finally:
        browser.quit()

def scrape_table():
    url_table = 'http://space-facts.com/mars/'
    tables = pd.read_html(url_table)
    table_mars = tables[1]
    table_mars.columns = ['Description','Values of Mars']
    table_mars.set_index('Description', inplace=True)
    DataToHTML['table_mars'] = table_mars.to_html()
    return DataToHTML

def scrape_imgs():

    try: 
        browser = init_browser()
        url_imgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_imgs)
        html_imgs = browser.html
        soup = BeautifulSoup(html_imgs, 'html.parser')
        imgs = soup.find_all('div', class_='item')
        head_imgs = []
        url_main_imgs = 'https://astrogeology.usgs.gov' 
        for x in imgs: 
            header = x.find('h3').text
            url_complement_imgs = x.find('a', class_='itemLink product-item')['href']
            browser.visit(url_main_imgs + url_complement_imgs)
            html_full_imgs = browser.html
            soup = BeautifulSoup( html_full_imgs, 'html.parser')
            url_full_imgs = url_main_imgs + soup.find('img', class_='wide-image')['src']
            head_imgs.append({"header" : header, "url_full_imgs" : url_full_imgs})
        sort_aux1 = [{'header' : 'Valles Marineris Hemisphere Enhanced'},{'header' :  'Cerberus Hemisphere Enhanced'},{'header' : 'Schiaparelli Hemisphere Enhanced'},{'header' : 'Syrtis Major Hemisphere Enhanced' }]
        sort_aux2 = []
        for y in range(len(sort_aux1)):
            for x in range(len(head_imgs)):
                if sort_aux1[y]['header'] == head_imgs[x]['header']:
                    sort_aux2.append({"header" : sort_aux1[y]['header'], "url_full_imgs" : head_imgs[x]['url_full_imgs']})
        DataToHTML['imgs']=sort_aux2
        return DataToHTML
    finally:
        browser.quit()