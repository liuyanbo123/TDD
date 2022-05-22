import time
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://localhost:8000')
print("test="+browser.title)
time.sleep(10)
assert 'Django' in browser.title