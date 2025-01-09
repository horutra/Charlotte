import json
Section_path = 'Section.json'

#going to try to read and open 
try:
    #reading class section from json file
    with open(Section_path, 'r') as file: 
        data = json.load(file)
    
    MinCredits = data["SectionsRetrieved"]["Course"]["MinimumCredits"]
    print("Reading Section Details (Minimum Credits)", MinCredits)


except FileExistsError:
    print("File does not exist.")
except json.JSONDecodeError:
    print("Error: Failed to decode json file. Check file format.")
finally:
    #Accessing the first element in the array
    print("File read succsfully.\n")
