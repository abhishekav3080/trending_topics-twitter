from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import pymongo
import requests
import json
from datetime import datetime

# Set up ProxyMesh
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = "YOUR_PROXYMESH_URL"
proxy.ssl_proxy = "YOUR_PROXYMESH_URL"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--proxy-server=%s' % proxy.http_proxy)

# Set up the WebDriver
service = Service('C:/Users/91902/OneDrive/Desktop/Twitter_trends_project_assignment/chromedriver.exe')  # Replace with the actual path to chromedriver.exe
driver = webdriver.Chrome(service=service, options=chrome_options)

# Log in to Twitter
driver.get('https://twitter.com/login')
time.sleep(2)

username = driver.find_element(By.NAME, 'session[username_or_email]')
password = driver.find_element(By.NAME, 'session[password]')
username.send_keys('YOUR_TWITTER_USERNAME')
password.send_keys('YOUR_TWITTER_PASSWORD')
password.send_keys(Keys.RETURN)
time.sleep(5)

# Fetch the top 5 trending topics
trending_topics = driver.find_elements(By.XPATH, '//section[@aria-labelledby="accessible-list-0"]//span')[:5]
trends = [topic.text for topic in trending_topics]

# Close the WebDriver
driver.quit()

# Print the trends
print(trends)

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

# Create a unique ID and store the data
unique_id = str(datetime.now().timestamp())
ip_address = requests.get('https://api.ipify.org').text
data = {
    '_id': unique_id,
    'trend1': trends[0],
    'trend2': trends[1],
    'trend3': trends[2],
    'trend4': trends[3],
    'trend5': trends[4],
    'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'ip_address': ip_address
}

collection.insert_one(data)
print('Data stored in MongoDB')
