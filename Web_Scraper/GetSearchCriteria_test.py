from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import time
import json

def getAntiForgery(driver):
    try:
        # Wait for the token input field to be available in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
        )

        # Find the token input field by its name attribute
        token_input = driver.find_element(By.NAME, "__RequestVerificationToken")
        
        # Extract the token value from the input field
        if token_input:
            token_value = token_input.get_attribute("value")
            print(f"Extracted Anti-Forgery Token")
            return token_value
        else:
            print("Token input field not found.")
            return None
    except Exception as e:
        print(f"Error while extracting the token: {e}")
        return None

def getCookie(driver):
    # Make sure the page is fully loaded
    time.sleep(5)  # Adjust the sleep time if necessary for the cookies to be set
    cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    print(f"Extracted Cookies")
    return cookie_dict

def getSearchCriteriaJson():
    # Set up Selenium to load the page and extract the token
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    # Navigate to the page to extract the tokens, api Url and page it 
    # is accessed from
    term = "2025SP" # 4 digit year, 2 character term uppercase
    targetUrl = 'https://stuserv.hartnell.edu/Student/Courses'
    apiUrl = 'https://stuserv.hartnell.edu/Student/Courses/PostSearchCriteria'
    driver.get(targetUrl)

    # Step 3: Wait for the page to load completely
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
    )
    token = getAntiForgery(driver)

    if not token:
        print("Failed to extract the anti-forgery token")
        driver.quit()
        return

    cookies = getCookie(driver)

    # Now you can print or extract the first header (or manipulate as needed)
    #print("Extracted Anti-Forgery Token: ", token)
    #print("Extracted Cookies: ", cookies)

    data = {
        "terms":[term]
    }

    session = requests.Session()
    
    for cookies_name, cookies_value in cookies.items():
        session.cookies.set(cookies_name, cookies_value)

    
    response = session.post(apiUrl, headers= [], json=data)

    # Check the response status and print the JSON data
    if response.status_code == 200:
        try:
            json_data = response.json()
            print("*****************Success!!!*******************")
            #print(json.dumps(json_data, indent=2))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

    # Close the Selenium browser session
    driver.quit()

getSearchCriteriaJson()