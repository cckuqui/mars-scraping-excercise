# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import tweepy
from twitter import api_key, api_secret_key


def init_browser():
    return Browser('chrome', {'executable_path': 'chromedriver.exe'})

def MarsNews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    content_titles = soup.find_all('div', class_ = 'content_title')
    article_title = content_titles[1].text
    teaser_body = soup.find('div', class_ = 'article_teaser_body').text
    browser.quit()

    return article_title, teaser_body

def JPLMarsImage():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html,'html')

    lede = soup.find('figure', class_='lede')
    img = lede.find('a')['href']
    img_url = f'https://jpl.nasa.gov{img}'
    browser.quit()

    return img_url

def MarsWeather():
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth)
    username = 'MarsWxReport'
    tweets = []
    data = api.user_timeline(id=username, tweet_mode="extended")

    for t in data:
        tweets.append(t.full_text)
    weather = tweets[0]
    weather = weather.split(' http',1)[0]
    
    return weather

def MarsFacts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')

    facts = pd.read_html(url)
    facts_df = pd.DataFrame(facts[0])
    facts_df.columns = ['Data','Value']
    facts_df = facts_df.set_index('Data')
    browser.quit()

    facts_df

    return facts_df

def MarsHemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')

    list_hem = []
    hemispheres = {}
    products = soup('div', class_='description')

    for p in products:
        hem = p.find('h3').text
        hem = hem.replace(' Enhanced','')
        hemispheres['Hemisphere'] = hem
        browser.click_link_by_partial_text(hem)
        html = browser.html
        soup = bs(html,'html')
        image_url = soup.find_all('a', {'target':'_blank'})
        for i in image_url:
            if 'Sample' in i.text:
                hemispheres['Img link'] = i['href']
        list_hem.append(hemispheres)
    browser.quit()

    return list_hem

def scrape():
    title, body = MarsNews()
    mars_info = {'News Article':title,'News Teaser':body,'Image URL':JPLMarsImage(),\
        'Weather':MarsWeather(), 'Facts': MarsFacts(), 'Photos': MarsHemispheres()}
    
    return mars_info

