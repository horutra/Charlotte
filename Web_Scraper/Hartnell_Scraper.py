from selenium import webdriver
import requests

from selenium.webdriver.support.ui import Select 
from selenium.webdriver.chrome.options import Options
import time 

browser = webdriver.Chrome()
options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options = options) 
browser.get('https://stuserv.hartnell.edu/Student/Courses/')

filter = browser.find_element('id', 'submit-search-form')
dropdown = Select(browser.find_element('id', 'term-id'))
dropdown.select_by_visible_text("2025 Spring Semester") 
filter.click()

time.sleep(2)

section = browser.find_element('id', 'collapsible-view-available-sections-for-AAT-101-groupHeading')
section.click()

time.sleep(5)
browser.close()