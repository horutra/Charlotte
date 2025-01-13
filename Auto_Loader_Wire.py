# Import necessary modules.
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from seleniumwire.utils import decode as decode_sw
from selenium.webdriver.common.by import By
import time
import json 

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
    sect_mods = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['InstructorDetails'][0]['InstructorMethod']
    # Modality 1 Days.
    sect_mod1_day = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['DaysOfWeekDisplay']
    # Modality 1 Times.
    sect_mod1_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['StartTimeDisplay'] + ' - ' + json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0][
        'Section']['FormattedMeetingTimes'][0]['EndTimeDisplay']
    # Modality 1 Schedule.
    sect_mod1_sch = json_dict["SectionsRetrieved"]["TermsAndSections"][0][
        "Sections"][0]["Section"]["FormattedMeetingTimes"][0]['DatesDisplay']
    # Modality 1 Location.
    sect_mod1_loc = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["LocationDisplay"]
    # Modality 1 Instructor.
    sect_mod1_inst = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['InstructorDetails'][0]['FacultyName']
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
    final_string = sect_term + ',' + sect_name + ',' + sect_requisites + ',' + \
        sect_desc + ',' + str(sect_avlb) + ',' + str(sect_enrl) + \
        ',' + str(sect_cap) + ',' + str(sect_wait) + \
        ',' + sect_mods + ',' + sect_mod1_sch + ',' + sect_mod1_inst + ',' + sect_mod1_times + ',' + sect_mod1_loc + ',' + \
        sect_mod1_day + ',' + sect_mod2_times + ',' + sect_mod2_day + ',' + \
        sect_mod2_inst + ',' + sect_mod2_loc + ',' + sect_mod2_inst + '\n'
    a_file.write(final_string)
    return


def main():
    # Setup Drivers.

    driver = webdriver.Chrome(seleniumwire_options={"disable_encoding": True})
    driver.get('https://stuserv.hartnell.edu/Student/Courses/')

    # Access elements and drop downs.
    filter = driver.find_element('id', 'submit-search-form')
    dropdown = Select(driver.find_element('id', 'term-id'))
    # Filter by 2025 Spring Semester.
    dropdown.select_by_visible_text('2025 Spring Semester')
    filter.click()
    time.sleep(4)

    responses = []
    max_pages = driver.find_element('id', 'course-results-total-pages').text
    page = 0    
    #Dynamic wait time 
    for i in range(int(max_pages)):
        selection = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'esg-collapsible-group__title')))
        for e in selection:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of(e))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(e))
                e.click()
            except:
                print("Waiting to load elements")

        page +=1
        print("Page", page, "done.")
        next_page = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID,'course-results-next-page')))
        if next_page:
            next_page.click()
        else:
            pass
        
        time.sleep(2)

    # Wait for response to load.
    count = 0
    # Loop parses through each request in our driver, and finds the section requests.
    time.sleep(3)
    test_file = open("Test.txt", "a")
    for request in driver.requests: 
        if request.url == ('https://stuserv.hartnell.edu/Student/Courses/Sections') and request.headers['Content-Type'] == 'application/json, charset=UTF-8':
            try:
                data = decode_sw(request.response.body, request.response.headers.get(
                    'Content-Encoding', 'identity'))
                response = json.loads(data.decode('utf-8'))
                responses.append(response)
                parser(response, test_file)
            except:
                print('Ran into exception:', count, '\n')
                count += 1
                pass
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    main()
