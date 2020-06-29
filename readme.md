# Web Scraping exercise - Mission to Mars

Web application that scrapes information of mars from various NASA related pages and displays the information in one page.

![Retrived from 'https://www.space.com/29004-manned-mars-missions-planetary-society.html' on 29/06/2020](https://cdn.mos.cms.futurecdn.net/rgnbYgsoFLDZ2D3QLBVrZ6-650-80.jpg)

## Process

Since the objective was to show web scraping, each data was retrive from different sources:

|Information Retrived|Source|
|:---:|:---:|
|Mars News|https://mars.nasa.gov/news/|
|Featured Image & image details|https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars|
|Mars Weather|https://twitter.com/marswxreport?lang=en|
|General Facts|https://space-facts.com/mars/|
|Mars Hemispheres|https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars|

From this, a dictionary was created and uploaded into a MongoDB database through Python's Flask library so that when you open the site you'll see the latest scrape made.

### Copyright

Exercise created by Trilogy Education Services © 2019. All Rights Reserved. Mars image not own, retrived from Space.com on 29/06/2020.
