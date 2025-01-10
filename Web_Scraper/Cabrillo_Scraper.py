from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.chrome.options import Options
import time 

browser = webdriver.Chrome()
options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options = options) 
browser.get('https://success.cabrillo.edu/Student/Courses')

filter = browser.find_element('id', 'submit-search-form')
dropdown = Select(browser.find_element('id', 'term-id'))
dropdown.select_by_visible_text("Spring 2025") 
filter.click()

time.sleep(2)

section = browser.find_element('id', 'section-name-link-0')
section.click()
