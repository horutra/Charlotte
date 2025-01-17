from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, json, csv, time


def getCookie(driver):
    # Get all cookies from Selenium Browser Driver
    cookies = driver.get_cookies()

    # Create an empty dictionary to store key-value pairs
    cookie_dict = {}

    # Loop through each cookie and add it to the cookie dictionary
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict

def getSession(cookies):
    # Create a new session object using the requests library - allows parameters to persist across requests
    session = requests.Session()

    # combines all the name-value pairs of cookies extracted from the Selenium browser session
    for cookies_name, cookies_value in cookies.items():
        # Set each cookie in the requests session, which will be sent along with future requests
        # This ensures that any session-specific cookies (e.g., for maintaining login or state) are sent automatically
        session.cookies.set(cookies_name, cookies_value)
    
    return session

def getSearchCriteriaJson(url, apiUrl, quantity, term, driver):
    # Use driver to navigate to url
    driver.get(url)

    # Grab cookies using function
    cookies = getCookie(driver)

    # Set data field of header to match term specified in main
    data = {
        "terms":[term] , "quantityPerPage":quantity
    }

    # Call getSession Function
    session = getSession(cookies)

    # Send a POST request to the API URL
    response = session.post(apiUrl, headers=[], json=data)

    # Check the response status and print the JSON data
    if response.status_code == 200:
        try:
            json_data = response.json()
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
    return None

def getSectionJson(apiUrl, courseId, sectionIds, enrollFile, session):
    # Body data, courseId and SectionIds are static currently, need to change to dynamic
    data = {
        "courseId":courseId,
        "sectionIds":sectionIds
    }

    # Send the POST request
    response = session.post(apiUrl, headers=[], json=data)

    # Check the response status and print the JSON data
    if response.status_code == 200:
        try:
            json_data = response.json()
            parseSection(json_data, enrollFile)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)


def parseSection(json_dict, a_file):
    # Add timestamp
    timestamp = time.ctime()

    # Accessing the term description
    sect_term = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Term"]["Description"]

    # Section requisites
    sect_requisites = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Requisites"]
    if not sect_requisites:
        sect_requisites = "None"

    # Section name and description
    sect_name = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["SectionNameDisplay"]
    sect_desc = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["SectionTitleDisplay"]

    # Available seats, capacity, enrolled, and waitlisted counts
    sect_avlb = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Available"]
    sect_cap = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Capacity"]
    sect_enrl = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Enrolled"]
    sect_wait = json_dict["SectionsRetrieved"]["TermsAndSections"][0]["Sections"][0]["Section"]["Waitlisted"]

    # Class Modality (Instructor Method)
    sect_mods = "None"
    instructor_details = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0].get('InstructorDetails', [])
    if instructor_details:
        sect_mods = instructor_details[0].get('InstructorMethod', 'None')

    # Modality 1 Days, Times, Schedule, Location, Instructor
    sect_mod1_day = "None"
    sect_mod1_times = "None"
    sect_mod1_sch = "None"
    sect_mod1_loc = "None"
    sect_mod1_inst = "None"

    formatted_meeting_times = json_dict['SectionsRetrieved']['TermsAndSections'][0]['Sections'][0]['Section'].get('FormattedMeetingTimes', [])
    if formatted_meeting_times:
        sect_mod1_day = formatted_meeting_times[0].get('DaysOfWeekDisplay', 'None')
        sect_mod1_times = formatted_meeting_times[0].get('StartTimeDisplay', 'None') + ' - ' + formatted_meeting_times[0].get('EndTimeDisplay', 'None')
        sect_mod1_sch = formatted_meeting_times[0].get('DatesDisplay', 'None')

    # Modality 1 Instructor
    if instructor_details:
        sect_mod1_inst = instructor_details[0].get('FacultyName', 'None')

    # Modality 2 (Optional - Only present if there is a second modality)
    sect_mod2_day = 'None'
    sect_mod2_times = 'None'
    sect_mod2_sch = 'None'
    sect_mod2_inst = 'None'
    sect_mod2_loc = 'None'

    # Check if Modality 2 exists (i.e., another set of meeting times)
    if len(formatted_meeting_times) > 1:
        sect_mod2_day = formatted_meeting_times[1].get('DaysOfWeekDisplay', 'None')
        sect_mod2_times = formatted_meeting_times[1].get('StartTimeDisplay', 'None') + ' - ' + formatted_meeting_times[1].get('EndTimeDisplay', 'None')
        sect_mod2_sch = formatted_meeting_times[1].get('DatesDisplay', 'None')
        
        # Handle Instructor for Modality 2
        if len(instructor_details) > 1:
            sect_mod2_inst = instructor_details[1].get('FacultyName', 'None')  # Checking if the second instructor exists
        else:
            sect_mod2_inst = 'None'
        
        sect_mod2_loc = formatted_meeting_times[1].get('LocationDisplay', 'None')

    # Writing parsed data to CSV
    final_row = [sect_term, timestamp, sect_name, sect_requisites, sect_desc, str(sect_avlb), str(sect_enrl),
                 str(sect_cap), str(sect_wait), sect_mods, sect_mod1_sch, sect_mod1_inst,
                 sect_mod1_times, sect_mod1_day, sect_mod1_loc, sect_mod2_sch, sect_mod2_inst,
                 sect_mod2_times, sect_mod2_day, sect_mod2_loc]

    with open(a_file, 'a', newline='') as file:  # Open in append mode, and ensure correct line breaks
        writer = csv.writer(file)
        writer.writerow(final_row)

def charlotteArt():
    print('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀        ⣰⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡄⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⢿⡿⠀⠈⠛⢿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡾⠟⠉⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣦⣤⣀⣀⣀⣠⣤⣶⠿⠋⠀⣾⡇⠀⠀⠀⠀⠈⠙⠛⠿⢶⣶⣤⣤⣤⣄⣀⣀⣤⣤⣤⣴⡾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀                                                                                    
     @@@@@@@  @@@  @@@   @@@@@@   @@@@@@@   @@@        @@@@@@   @@@@@@@  @@@@@@@  @@@@@@@@  
    @@@@@@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@       @@@@@@@@  @@@@@@@  @@@@@@@  @@@@@@@@  
    !@@       @@!  @@@  @@!  @@@  @@!  @@@  @@!       @@!  @@@    @@!      @@!    @@!       
    !@!       !@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!  @!@    !@!      !@!    !@!       
    !@!       @!@!@!@!  @!@!@!@!  @!@!!@!   @!!       @!@  !@!    @!!      @!!    @!!!:!    
    !!!       !!!@!!!!  !!!@!!!!  !!@!@!    !!!       !@!  !!!    !!!      !!!    !!!!!:    
    :!!       !!:  !!!  !!:  !!!  !!: :!!   !!:       !!:  !!!    !!:      !!:    !!:       
    :!:       :!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!    :!:      :!:    :!:       
    ::: :::   ::   :::  ::   :::  ::   :::  ::: :::   :::  ::     ::       ::     ::: ::: 
    :: :: :   :   : :   :    : :   :   : :  : ::  :   : :  :      :        :      : :: ::                                                                                                   ⠀⠀⠀⠀⠀⠀⠀⠀
        
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⠿⣶⣤⣀⠀⠀⠀⠀⠀⠙⣷⡀⣸⡏⠀⠀⠀⠀⠀⠀⠈⢿⣦⢀⣾⠏⠀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀@@@@@@@
        ⠀⠀⠀⠀⠀⠀⣀⣴⡾⠟⠉⠀⠀⠀⠀⠉⠻⢷⣦⡀⠀⠀⠀⠸⣷⣿⠇⠀⠀⢀⣀⣀⣠⣤⣤⣿⣿⡟⠀⢰⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀@@@@@@@@⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢠⣴⡾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣦⡀⠀⠀⢿⣿⣴⡶⠿⠛⠛⠉⠉⠉⠉⠉⠙⣿⣄⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀@@!  @@@  ⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⡄⠀⣼⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀!@!  @!@ ⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⣿⠁⠀⠀⠀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀@!@!!@!⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⣀⣴⣶⠿⠛⠛⠉⠉⠉⠉⠉⠀⠀⠀⠀⠘⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀!!@!@!⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣦⠀⠀⠀⠀⠀⠀⠀⠀!!: :!! ⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡄⠀⠀⠀⠀⠀⠀:!:  !:! ⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡆⠀⠀⠀⠀⠀::   :::  ⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀:   : :  ⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')


def main():
    # Set up Selenium to load the page and extract the token
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)

    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y-%H%M', t)

    # Variables for each college
    enrollFile = ("HartnellEnrollment-" + timestamp + ".csv")
    term = '2025SP'
    classTotal = 419
    searchCriteriaUrl = 'https://stuserv.hartnell.edu/Student/Courses'
    searchCriteriaApiUrl = 'https://stuserv.hartnell.edu/Student/Courses/PostSearchCriteria'
    sectionUrl = 'https://stuserv.hartnell.edu/Student/Courses/SearchResult'
    sectionApiUrl = 'https://stuserv.hartnell.edu/Student/Courses/Sections'
    
    charlotteArt()
    searchData = getSearchCriteriaJson(searchCriteriaUrl, searchCriteriaApiUrl, classTotal, term, driver)

    driver.get(sectionUrl)
    cookies = getCookie(driver)
    session = getSession(cookies)

    if searchData:
        # Create header for CSV file
        with open(enrollFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Term', 'Time Collected', 'Section Name', 'Requisites', 'Description', 'Available Seats', 'Enrolled', 
                             'Capacity', 'Waitlisted', 'Instructor Method', 'Modality 1 Schedule', 
                             'Modality 1 Instructor', 'Modality 1 Times', 'Modality 1 Days', 'Modality 1 Location', 
                             'Modality 2 Schedule', 'Modality 2 Instructor', 'Modality 2 Times', 'Modality 2 Days',  
                             'Modality 2 Location'])

        with ThreadPoolExecutor(max_workers=10) as executor:
            # Create a tqdm progress bar
            with tqdm(total=len(searchData["Courses"]), desc="Processing courses", ncols=100, unit="course") as pbar:
                futures = []
                for course in searchData["Courses"]:
                    courseId = course["Id"]
                    sectionIds = course["MatchingSectionIds"]
                    if sectionIds:
                        futures.append(executor.submit(getSectionJson, sectionApiUrl, courseId, sectionIds, enrollFile, session))
                
                # Track progress with as_completed to update the progress bar
                for future in as_completed(futures):
                    pbar.update(1)  # Update progress bar after each completed task

    print('Completed Scanning Sections, file output to ' + enrollFile)

    driver.quit()


if __name__ == '__main__':
    main()