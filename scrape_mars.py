# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 
    
    executable_path = {'executable_path': '/anaconda3/pkgs/selenium-chromedriver-2.27-0/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars global dictionary to be imported into Mongo
mars_info = {}

# NASA Mars News Scrape
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Use splinter to visit NASA news URL
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Store Mars News in mars_info dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# Featured Image Scrape
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Use splinter to visit JPL featured Sapce Images and collect featured image
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Store featured image in mars_info dictionary
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
        
    finally:

        browser.quit()

        

# Mars Weather Scrape
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Use splinter to visit Mars weather Twitter account
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words and exclude non weather related tweets 
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts Scrape
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames and assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save code to html file
    data = mars_df.to_html()

    # Save Mars facts to mars_info dictionary
    mars_info['mars_facts'] = data

    return mars_info


# Mars Hemispheres Scrape
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Use splinter to visit USGS Astrogeology website 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemi_urls = []

        # Store the main_url 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for individual hemisphere info websites 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemi_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemi_urls'] = hemi_urls

        
        # Return mars_data dictionary 
        return mars_info
        
    finally:

        browser.quit()
