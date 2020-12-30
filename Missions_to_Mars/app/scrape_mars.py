from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    scrape_mars ={}

    # Mars new: URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title and paragraph 
    title_results = soup.body.find('div', class_="content_title").text
    paragraph_results= soup.body.find('div', class_="article_teaser_body").text


    # Images to be scraped
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # click on 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')

    # Click on 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML with Beautiful Soup
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    # Extract/ Scrape the URL
    feature_url = image_soup.select_one("figure.lede a img").get("src")
    # a=feature_url.find('a')
    # href=a['href']

    image_web='https://www.jpl.nasa.gov'
    featured_image_url =image_web + feature_url

   

    #mars table to be scrape
    # open url in browser
    facts_url = "https://space-facts.com/mars/"

    browser.visit(facts_url)

    html = browser.html

    tables = pd.read_html(facts_url)
    mars_table = tables[0]
    # mars_facts.columns = ["Description", "Mars"]
    # mars_facts= mars_facts.set_index('Description', inplace=True)
    
    # Use Pandas to convert the data to a HTML table string
    mars_facts= mars_table.to_html(header=False, index = False, justify="left")

    # Four Hemispheres to be scrape
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_url)
    image_urls = []
    links=browser.find_by_css('a.product-item h3')

    for i in range(len(links)):
        Four_hemi={}
        browser.find_by_css('a.product-item h3')[i].click()
        grabbed_image= browser.links.find_by_text('Sample').first
        #grabbing href from sample image tag
        Four_hemi['image_urls']=grabbed_image['href']
        #extracting title for each image
        Four_hemi['title']=browser.find_by_css('h2.title').text
        #adding info into created list
        image_urls.append(Four_hemi)
        print(image_urls)
        browser.back()

    scrape_mars ={
        "title":title_results,
        "paragraph": paragraph_results,
        "Feature_Images": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres_images":Four_hemi
        }
    browser.quit()
    return scrape_mars

if __name__ == '__main__':
    scrape()    