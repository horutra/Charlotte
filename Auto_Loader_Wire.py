# Import necessary modules.
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from seleniumwire.utils import decode as decode_sw
from selenium.webdriver.common.by import By
import time
import json
import requests as mod_req
import yaml

# Function parses the json file into a string with necessary information.


def parser(json_dict):
    term = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Term']['Description']
    enrolled = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['Enrolled']
    capacity = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['Capacity']
    requisites = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['Requisites']
    if (requisites == []):
        requisites = 'None'
    term_name = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['SectionNameDisplay']
    waitlist = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['Waitlisted']
    available = int(capacity) - int(enrolled)
    mode_1 = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['InstructionalMethodDisplay']
    mode_2 = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][1]['InstructionalMethodDisplay']
    days_m1 = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['DaysOfWeekDisplay']
    days_m2 = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['DaysOfWeekDisplay']
    m1_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['StartTimeDisplay'] + ' - ' + json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['EndTimeDisplay']

    m2_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][1]['StartTimeDisplay'] + ' - ' + json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][1]['EndTimeDisplay']
    m1_ins = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['FacultyDisplay']
    m2_ins = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['InstructorDetails'][0]['FacultyName']
    final = term + " " + str(enrolled) + " " + str(capacity) + " " + requisites + \
        " " + term_name + " " + str(waitlist) + " " + str(available) + " " + mode_1 + " " + mode_2 + \
        " " + days_m1 + " " + days_m2 + " " + m1_times + \
        " " + m2_times + " " + m1_ins + " " + m2_ins
    return final


def main():
    # Setup Drivers.
    driver = webdriver.Firefox(seleniumwire_options={"disable_encoding": True})
    driver.get('https://stuserv.hartnell.edu/Student/Courses/')
    # Access elements and drop downs.
    filter = driver.find_element('id', 'submit-search-form')
    dropdown = Select(driver.find_element('id', 'term-id'))
    # Filter by 2025 Spring Semester.
    dropdown.select_by_visible_text('2025 Spring Semester')
    filter.click()
    time.sleep(4)
    selection = driver.find_elements(
        By.CLASS_NAME, 'esg-collapsible-group__title')
    responses = []
    for e in selection:
        e.click()
    # Wait for response to load.
    time.sleep(10)
    count = 0
    # Loop parses through each request in our driver, and finds the section requests.
    for request in driver.requests:
        if request.url == 'https://stuserv.hartnell.edu/Student/Courses/Sections' and request.headers['Content-Type'] == 'application/json, charset=utf-8':
            try:
                data = decode_sw(request.response.body, request.response.headers.get(
                    'Content-Encoding', 'identity'))
                response = json.loads(data.decode('utf-8'))
                responses.append(response)
                print(parser(response), '\n')
            except:
                print('Ran into exception:', count, '\n')
                count += 1
                pass

    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    main()
