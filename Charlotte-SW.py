# Import necessary modules.
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from seleniumwire.utils import decode as decode_sw
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json
import pandas as pd

# Function parses the json file into a string with necessary information.


def parser(json_dict, a_file):
    sect_term = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Term"]["Description"]
    # Section requisites.
    sect_requisites = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Requisites"]
    if (sect_requisites == []):
        sect_requisites = "None"
    # Section name.
    sect_name = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["SectionNameDisplay"]
    # Section description.
    sect_desc = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["SectionTitleDisplay"]
    # Number of available seats.
    sect_avlb = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Available"]
    # Number of section capacity.
    sect_cap = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Capacity"]
    # Number of enrolled.
    sect_enrl = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Enrolled"]
    # Number of waitlisted.
    sect_wait = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Waitlisted"]
    # Class Modalities.
    sect_mods = 'None'
    try:
        sect_mods = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['InstructorDetails'][0]['InstructorMethod']
    except:
        pass
    # Modality 1 Days. None by default.
    sect_mod1_day = 'None'
    try:
        sect_mod1_day = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['FormattedMeetingTimes'][0]['DaysOfWeekDisplay']
    except:
        pass
    # Modality 1 Times. None by default.
    sect_mod1_time = 'None'
    try:
        sect_mod1_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['FormattedMeetingTimes'][0]['StartTimeDisplay'] + ' - ' + json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['FormattedMeetingTimes'][0]['EndTimeDisplay']
    except:
        pass
    # Modality 1 Schedule. None by default.
    sect_mod1_sch = 'None'
    try:
        sect_mod1_sch = json_dict["SectionsRetrieved"]["TermsAndSections"][0][
            "Sections"][0]["Section"]["FormattedMeetingTimes"][0]['DatesDisplay']
    except:
        pass
    # Modality 1 Location. None by default.
    sect_mod1_loc = 'None'
    try:
        sect_mod1_loc = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["LocationDisplay"]
    except:
        pass
    # Modality 1 Instructor. None by default.
    sect_mod1_inst = 'None'
    try:
        sect_mod1_inst = json_dict['SectionsRetrieved']['TermsAndSections'][
            0]['Sections'][0]['InstructorDetails'][0]['FacultyName']
    except:
        pass
    # Modality 2 Days. None by default unless section has second modality.
    sect_mod2_day = 'None'
    try:
        sect_mod2_day = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['DaysOfWeekDisplay']
    except:
        pass
    # Modality 2 Times. None by default unless section has second modality.
    sect_mod2_times = 'None'
    if (sect_mod2_day != 'None'):
        sect_mod2_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['StartTimeDisplay'] + ' - ' + json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
            'Section']['EndTimeDisplay']
    # Modality 2 Schedule. None by default unless section has second modality.
    sect_mod2_sch = 'None'
    if (sect_mod2_day != 'None'):
        sect_mod2_sch = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section']['DatesDisplay']
    # Modality 2 Instructor. None by default unless section has second modality.
    sect_mod2_inst = 'None'
    if (sect_mod2_day != 'None'):
        sect_mod2_inst = json_dict['SectionsRetrieved']['TermsAndSections'][0][
            'Sections'][0]['Section']['InstructorDetails'][0]['FacultyName']
    # Modality 2 Location. None by default unless section has second modality.
    sect_mod2_loc = 'None'
    if (sect_mod2_day != 'None'):
        sect_mod2_loc = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["LocationDisplay"]

    # final_string = sect_term + ',' + sect_name + ',' + sect_requisites + ',' + \
    #     sect_desc + ',' + str(sect_avlb) + ',' + str(sect_enrl) + \
    #     ',' + str(sect_cap) + ',' + str(sect_wait) + \
    #     ',' + sect_mods + ',' + sect_mod1_sch + ',' + sect_mod1_inst + ',' + sect_mod1_times + ',' + sect_mod1_loc + ',' + \
    #     sect_mod1_day + ',' + sect_mod2_times + ',' + sect_mod2_day + ',' + \
    #     sect_mod2_inst + ',' + sect_mod2_loc + ',' + sect_mod2_inst + ',' + time.ctime() + '\n'
    class_data = pd.DataFrame({
        'Section Term': [sect_term],
        'Section Name': [sect_name],
        'Sections Requisites': [sect_requisites],
        'Desctription': [sect_desc],
        'Available Seats': [sect_avlb],
        'Enrollments': [sect_enrl],
        'Capacity': [sect_cap],
        'Wait List': [sect_wait],
        'Modalities': [sect_mods],
        'Dates': [sect_mod1_sch],
        'Falculty Name': [sect_mod1_inst],
        'Class Times': [sect_mod1_times],
        'Class Location': [sect_mod1_loc],
        'Days of week': [sect_mod1_day],
        'Modality 2 Class Time': [sect_mod2_times],
        'Modality 2 Days of Week': [sect_mod2_day],
        'Mod 2 Instructor': [sect_mod2_inst],
        'Mod 2 Class Location': [sect_mod2_loc],
        'Day of scrape': [time.ctime()]
    })

    class_data.to_csv(a_file, mode='a', header=False, index=False)
    return


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
    # Wait for page to load.
    time.sleep(3)
    # Find the maximum number of pages.
    max_pages = driver.find_element('id', 'course-results-total-pages').text
    test_file = open('test.csv', 'a')
    for i in range(int(max_pages)):
        selection = driver.find_elements(
            By.CLASS_NAME, 'esg-collapsible-group__title')
        next_page = driver.find_element('id', 'course-results-next-page')
        for e in selection:
            e.click()
        time.sleep(3)
        # Next Page Element.
        next_page.click()
        # Wait for response to load.
        time.sleep(3)
    # Setup headers for output csv.
    class_data = pd.DataFrame([
        'Section Term',
        'Section Name',
        'Sections Requisites',
        'Desctription',
        'Available Seats',
        'Enrollments',
        'Capacity',
        'Wait List',
        'Modalities',
        'Dates',
        'Falculty Name',
        'Class Times',
        'Class Location',
        'Days of week',
        'Modality 2 Class Time',
        'Modality 2 Days of Week',
        'Mod 2 Instructor',
        'Mod 2 Class Location',
        'Day of scrape'
    ])
    class_data.to_csv(test_file, mode='a', header=True, index=False)
    # Loop parses through each request in our driver, and finds the section requests.
        for request in driver.requests:
            if request.url == 'https://stuserv.hartnell.edu/Student/Courses/Sections' and request.headers['Content-Type'] == 'application/json, charset=utf-8':
                try:
                    data = decode_sw(request.response.body, request.response.headers.get(
                    'Content-Encoding', 'identity'))
                    response = json.loads(data.decode('utf-8'))
                    parser(response, test_file)
                except:
                    pass

    # Wait, then shut down driver.
    time.sleep(5)
    driver.quit()
if __name__ == '__main__':
    main()
