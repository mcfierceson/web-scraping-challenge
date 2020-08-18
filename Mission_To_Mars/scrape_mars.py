#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time


# In[2]:


# In[175]:

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # In[4]:

    browser = init_browser()

    url = 'http://mars.nasa.gov/news/'
    browser.visit(url)


    # In[6]:


    html = browser.html
    soup = bs(html, 'html.parser')

    time.sleep(2)
    article = soup.find('div', class_ = 'list_text')
    news_div = article.find('div', class_="content_title")
    news_title = news_div.find('a').text
    news_p = article.find('div', class_ = "article_teaser_body").text

    # In[7]:


    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)


    # In[8]:


    image_link = browser.find_by_id('full_image')
    image_link.click()


    # In[9]:


    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_link = browser.links.find_by_partial_text('more info')
    more_info_link.click()


    # In[10]:


    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    image = jpl_soup.find('figure', class_ = 'lede')
    rel_image_url = image.img.get('src')

    featured_image_url = "https://www.jpl.nasa.gov" + rel_image_url


    # *******Twitter scrape no longer works, ignore and skip as per Stephen********

    # In[12]:


    # twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # browser.visit(twitter_url)

    # twitter_html = browser.html
    # twitter_soup = bs(twitter_html, 'html.parser')

    # tweet = twitter_soup.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text

    # print(tweet)


    # In[13]:


    import pandas as pd

    mars_url = "https://space-facts.com/mars/"

    tables = pd.read_html(mars_url)

    mars_df = tables[0]
    mars_df.columns = ('Description', 'Value')

    mars_df = mars_df.set_index('Description')


    # In[173]:


    mars_table = mars_df.to_html()
    mars_table = mars_table.replace('\n', '')


    # In[187]:


    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html


    # In[188]:


    hemi_soup = bs(hemi_html, 'html.parser')


    # In[189]:


    results = hemi_soup.find_all('div', class_ = 'description')


    # In[201]:


    hemisphere_image_urls = []
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            link = result.a['href']

            # Print results only if title, price, and link are available
            if (link):
                image_url = "https://astrogeology.usgs.gov" + link
                browser.visit(image_url)
                time.sleep(1)
                image_html = browser.html
                image_soup = bs(image_html, 'html.parser')
                image_title = image_soup.find('h2', class_='title').text
                downloads = image_soup.find('div', class_='downloads')
                full_link = downloads.a['href']
                entry = {'title' : image_title, 'url' : full_link}
                hemisphere_image_urls.append(entry)
        except AttributeError as e:
            print(e)

    scraped_data = {
                'news_title' : news_title,
                'news_paragraph' : news_p,
                'jpl_image' : featured_image_url,
                'mars_table' : mars_table,
                'mars_images' : hemisphere_image_urls
    }

    browser.quit()

    return scraped_data