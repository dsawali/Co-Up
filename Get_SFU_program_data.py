# pip install lxml
# install requests
from lxml import html
import requests
import json


""" Gets an unorganized list from SFU website in
    [["Faculty", "Program", "Program",...]] format. """
def Get_SFU_Data(tree):
    faculties_and_programs_unorganized=[]
    for i in range (1,9): #number of FACULTY_CHOICES
        className = '"toggleContent item'+str(i)+'"'
        xpathArg = '//div[@class = %s]//b/text()' % className
        programs_temp = tree.xpath(xpathArg)
        faculties_and_programs_unorganized.append(programs_temp)
    return Organize_SFU_Data(faculties_and_programs_unorganized)


""" Produces a dictionary in {"Faculty": "[Programs]"} format. """
def Organize_SFU_Data(data):
    faculties_and_programs = {}
    for i in data:
        faculty = i.pop(0)
        faculties_and_programs[faculty] = i
    return faculties_and_programs



### MAIN ###
page = page = requests.get('https://www.sfu.ca/programs/faculties-departments.html')
tree = html.fromstring(page.content)
faculties_and_programs = Get_SFU_Data(tree)

program_data_json = json.dumps(faculties_and_programs, indent=4)

f = open('SFU_program_data.json', 'w')
f.write(program_data_json)
f.close()

f = open("SFU_program_data.json", 'r')
data = f.read()
convertedBackToDict = json.loads(data)
f.close()
