def mars_scrape():

    # Dependencies
    from bs4 import BeautifulSoup as bs
    from selenium import webdriver
    import pandas as pd
    import tweepy
    from dotenv import load_dotenv
    import os
    import datetime

    # Setting browser
    load_dotenv()
    try: 
        google_chrome_bin = os.getenv('google_chrome_bin')
        chromedriver_path = os.getenv('chromedriver_path')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = google_chrome_bin
        browser = webdriver.Chrome(execution_path=chromedriver_path, chrome_options=chrome_options)
        return browser
    except:
        return 'browser not working'
    
    # News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html')
    content_titles = soup.find_all('div', class_ = 'content_title')
    ntitle = content_titles[1].text
    nbody = soup.find('div', class_ = 'article_teaser_body').text

    # Feature Image page
    url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html,'html')
    
    # Image Url
    lede = soup.find('figure', class_='lede')
    lede_img = lede.find('a')['href']
    feat_img = f'https://jpl.nasa.gov{lede_img}'
    
    # Image Details
    details = soup.find('aside', class_='image_detail_module')
    ps = details.find_all('p')
    det = []
    for p in ps:
        if ("Full-Res" not in p.text) and ("Views" not in p.text):
            img_det = {}
            img_det['detail'] = p.text
            det.append(img_det)

    # Weather from twitter
    api_key = os.getenv("api_key")
    api_secret_key = os.getenv("api_secret_key")
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
    facts.columns = ['Data','Values']
    facts = facts.to_html(classes="table table-hover table-dark table-striped", header=False, justify='center', index=False)
        
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
        browser.back()
        links.append(h)
    
    browser.quit()
    
    # Dictionary for Mongo
    mars = {
        'ntitle':ntitle,
        'nbody':nbody,
        'feat_img':feat_img,
        'img_det':det,
        'weather':weather,
        'facts':facts,
        'h':links,
        'date': str(datetime.date.today())
        }

    return mars