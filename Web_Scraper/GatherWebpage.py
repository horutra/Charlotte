from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import time
import json

def getCookie(driver):
    # Get all cookies from Selenium Browser Driver
    cookies = driver.get_cookies()

    # Create an empty dictionary to store key-value pairs
    cookie_dict = {}

    # Loop through each cookie and add it to the cookie dictionary
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict

def getSearchCriteriaJson(term, driver):
    # Navigate to the page to extract the tokens, API Url and page it 
    # is accessed from
    url = 'https://stuserv.hartnell.edu/Student/Courses'
    apiUrl = 'https://stuserv.hartnell.edu/Student/Courses/PostSearchCriteria'
    driver.get(url)

    # Grab cookies using function
    cookies = getCookie(driver)

    # Set data field of header to match term specified in main
    data = {
        "terms":[term]
    }

    # Create a new session object using the requests library - allows parameters to persist across requests
    session = requests.Session()

    # combines all the name-value pairs of cookies extracted from the Selenium browser session
    for cookies_name, cookies_value in cookies.items():
        # Set each cookie in the requests session, which will be sent along with future requests
        # This ensures that any session-specific cookies (e.g., for maintaining login or state) are sent automatically
        session.cookies.set(cookies_name, cookies_value)

    # Send a POST request to the API URL
    response = session.post(apiUrl, headers=[], json=data)

    # Check the response status and print the JSON data
    if response.status_code == 200:
        try:
            json_data = response.json()
            print("Criteria JSON Success!")
            #print(json.dumps(json_data, indent=2)) # contains the data output of the JSON
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
    

def getSectionJson(driver):
    # # Navigate to the page to extract the tokens, API Url and page it 
    # is accessed from
    url = 'https://stuserv.hartnell.edu/Student/Courses/SearchResult'
    api_url = 'https://stuserv.hartnell.edu/Student/Courses/Sections'
    driver.get(url)

    # Grab cookies using function
    cookies = getCookie(driver)

    # Body data, courseId and SectionIds are static currently, need to change to dynamic
    data = {
        "courseId":"11686","sectionIds":["100037"]
    }

    # Create a new session object using the requests library - allows parameters to persist across requests
    session = requests.Session()

    # combines all the name-value pairs of cookies extracted from the Selenium browser session
    for cookies_name, cookies_value in cookies.items():
        # Set each cookie in the requests session, which will be sent along with future requests
        # This ensures that any session-specific cookies (e.g., for maintaining login or state) are sent automatically
        session.cookies.set(cookies_name, cookies_value)

    # Send the POST request
    response = session.post(api_url, headers=[], json=data)

    # Check the response status and print the JSON data
    if response.status_code == 200:
        try:
            json_data = response.json()
            print("Section JSON Success!")
            #print(json.dumps(json_data, indent=2)) # contains the data output of the JSON
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

def parseCriteria(driver):
    getSearchCriteriaJson()

def parseAllSections(driver):  
    getSectionJson()

def main():
    # Set up Selenium to load the page and extract the token
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    term = '2025SP'
    getSearchCriteriaJson(term, driver)
    getSectionJson(driver)
    driver.quit()
    
main()