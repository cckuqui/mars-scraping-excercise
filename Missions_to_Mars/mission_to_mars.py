# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import tweepy
from twitter import api_key, api_secret_key

def scrape():
    # News
    browser = Browser('chrome', {'executable_path': 'chromedriver.exe'})
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')
    content_titles = soup.find_all('div', class_ = 'content_title')
    ntitle = content_titles[1].text
    nbody = soup.find('div', class_ = 'rollover_description_inner').text

    # Feature Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html,'html')
    lede = soup.find('figure', class_='lede')
    lede_img = lede.find('a')['href']
    feat_img = f'https://jpl.nasa.gov{lede_img}'

    # Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth)
    username = 'MarsWxReport'
    tweets = []
    data = api.user_timeline(id=username, tweet_mode="extended")
    for t in data:
        tweets.append(t.full_text)
    weather = tweets[0]
    weather = weather.split(' http',1)[0]
    

    # Table Facts
    url = 'https://space-facts.com/mars/'
    facts = pd.read_html(url)[0]
    facts.columns = ['Data','Value']
    facts.set_index('Data', inplace=True)
    facts = facts.to_html(classes="table table-hover").strip()

    # Hemisphere Images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')
    links = []
    products = soup.find_all('div', class_='item')
    for p in products:
        h = {}
        hem = p.find('h3').text
        hem = hem.replace(' Hemisphere Enhanced','')
        h['item'] = hem
        browser.click_link_by_partial_text(hem)
        html = browser.html
        soup = bs(html, 'html')
        image_url = soup.find_all('li')
        for i in image_url:
            img = i.find('a')
            if 'Sample' in i.text:
                img = img.get('href')
                h['url'] = img
                print(img)
        browser.back()
        links.append(h)
    
    browser.quit()
    
    # Dictionary for Mongo
    mars = {'ntitle':ntitle,'nbody':nbody,'feat_img':feat_img,'weather':weather,'facts':facts,'h':links}
    # print(mars)

    return mars