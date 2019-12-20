#!/usr/bin/env python
# coding: utf-8

# Mission to Mars - Scraping

# Dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

# create dictionary to capture mars data
mars_data = {}

# using flask app
def scrape_all():
    # Init chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    browser = Browser("chrome", executable_path="chromedriver", headless=False)

    title, news_p = get_mars_news(browser)

    # mars dictionary for scraping functions
    mars_news_data = { 
        "news_title": title,
        "news_text": news_p,
        "featured_image_url": get_feature_image(browser),
        "mars_weather": get_weather(browser),
        "mars_facts": get_mars_facts(),
        "hem_image_urls": get_hemisphere_data(browser)
    }

    # Close the browser after scraping
    browser.quit()

    return mars_news_data


# ### Visit NASA News site and get the latest news title and paragraph text
def get_mars_news(browser):
    
    # Visit NASA News Site
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)

    time.sleep(1)

    # Scrape page into Soup
    mars_html = browser.html
    soup = bs(mars_html, "html.parser")

    try:
        # Get the latest News Title
        #result = soup.find('li', class_='slide')
        result = soup.find('div', class_='image_and_description_container')
        title = result.find('div', class_="content_title").find('a').text
        #print(title)

        # Get the latest News Title's Paragraph Text
        #result = soup.find('li', class_='slide')
        result = soup.find('div', class_='image_and_description_container')
        news_p = result.find('div', class_="article_teaser_body").text
        #print(news_p)

        # # Store data in a dictionary
        # mars_data['news_title'] = title
        # mars_data['news_para'] = news_p
    
        # # Close the browser after scraping
        # browser.quit()            
        
    except AttributeError as e:
       print(e)

    # Return results
    return title, news_p


# In[5]:
# ### Visit url for JPL feactured space image

def get_feature_image(browser):
#   browser = init_browser()

    # Visit url for JPL Featured Space Image
    feature_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(feature_url)

    time.sleep(4)

    #find and click "full image" button
    full_image = browser.find_link_by_partial_text('FULL IMAGE')
    full_image.click()

    time.sleep(4)

    #find and click "more info" button
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    time.sleep(2)

    # Scrape page into Soup
    feature_html = browser.html
    soup = bs(feature_html, "html.parser")


    try:
        feature_url = soup.find('figure', class_="lede").a['href']
        featured_image_url = "https://www.jpl.nasa.gov" + feature_url
        #print(featured_image_url)
        
        # # Store data in a dictionary
        # mars_data['featured_image'] = featured_image_url


        # Close the browser after scraping
        # browser.quit()
         
    except AttributeError as e:
       print(e)

    # Return results
    return featured_image_url

# In[6]:
# ### Visit the Mars twitter account and get the latest tweet

def get_weather(browser):
#     browser = init_browser()

    # Visit the Mars twitter account
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    time.sleep(1)

    # Scrape page into Soup
    weather_html = browser.html
    soup = bs(weather_html, "html.parser")

    # Get the latest Mars weather tweet
    # result = soup.find_('div', class_='tweet', data-name_='Mars Weather')
    weather_tweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(weather_tweet)

    # Get the latest Mars weather tweet
    # result = soup.find_('div', class_='tweet', data-name_='Mars Weather')
    weather_tweet = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(weather_tweet)
 
    # # Store data in a dictionary
    # mars_data['weather_tweet'] = weather_tweet

    # # Close the browser after scraping
    # browser.quit()
    
    # Return results
    return weather_tweet

    
# In[7]:
# ### Visit the Mars Facts webpage and scrape the table containing facts about the planet.

# Visit the Mars Facts Webpage
def get_mars_facts():
    
    facts_url = "https://space-facts.com/mars/"
    
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_table = pd.read_html(facts_url)
    #facts_table
    
    # Create Dataframe
    mars_df = facts_table[0]
    mars_df.columns = ['Description', 'Value']
    #mars_df.head()
    
    # Set the index to the Item column
    mars_df.set_index('Description', inplace=True)
    #mars_df.head
        
    # # Generate HTML table from DataFrame
    # html_table = mars_df.to_html(index=False)
    mars_df.to_html()
    # #html_table
    
    # #strip unwanted lines
    # html_table.replace('\n', '')
        
    # # Store data in a dictionary
    # mars_data['mars_facts'] = html_table
        
    # Return results
    return mars_df.to_html()


# In[8]:
# ### Visit the USGS Astrogeology site and get the latest hemisphere titles and images.

def get_hemisphere_data(browser):

    # Visit the USGS Astrogeology site
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)

    time.sleep(1)

    # Scrape page into Soup
    hem_html = browser.html
    soup = bs(hem_html, "html.parser")

    # create list to capture data
    hemisphere_image_urls = []

    # Get the latest Hemisphere Images and Titles
    result = soup.find('div', class_="collapsible results").find_all('div', class_="item")
    print(result)

    #Loop through result data for title and image
    for hemisphere in result:
        
        #get image title
        descr = hemisphere.find('div', class_="description").find('a', class_="itemLink product-item").h3.text
        
        #remove "enhanced" from title
        h_title = ' '.join(descr.split()[0:-1])
                                                                  
        #get image url
        h_image = hemisphere.find('a', class_="itemLink product-item")['href']
        h_image_url =  'https://astrogeology.usgs.gov' + h_image
        print(h_image_url)
                                                                  
        #get full image (high resolution)
        browser.visit(h_image_url)
        time.sleep(1)
        
        find_image = browser.find_link_by_text('Sample').first
        full_image_url = find_image['href']
       
            
        # Store data in a hemisphere dictionary
        h_data = {
            "title" : h_title,
            "image_url" : full_image_url
        }
        
        #add data to list
        hemisphere_image_urls.append(h_data)
            
    #print(hemisphere_image_urls)
    
    # # Store data in a mars dictionary
    # mars_data['hemisphere_info'] = hemisphere_image_urls
    # #print(mars_data)
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return hemisphere_image_urls







