import json
from collections import defaultdict
import difflib
import matplotlib.pyplot as plt

companies = defaultdict(int)
location = defaultdict(int)
skills = defaultdict(int)
industry = defaultdict(int)

with open('143dataall.json','r') as f:
    allpeople = f.readlines()
    
    for person in allpeople:
        info = json.loads(person)
        if info:

            try:
                industry[info['industryName']] += 1
            except:
                # printing failure reason
                print("industry")
#                 print(info)
                print()
                print()
                print()
                print()

            if info['experience']:
                companies[info['experience'][0]['companyName']] += 1

            try:
                # split the location in city and state for furture analysis
                # and save that into tuple
                curPlace = info['geoLocationName']
                city, state = curPlace.split(',')
                found = None #indicator of whether location has found in certain format
                for savedCity, savedState in location:
                    if city in savedCity:
                        found = True
                        location[(savedCity, savedState)] += 1

                if not found:
                    location[(city,state)] += 1
            except:
                # printing failure reason
                print('geoloc')
#                 print(info)
#                 print()
#                 print()
#                 print()
#                 print()

            try:
                if info['skills']:
                    for skill in info['skills']:
                        if skill['name'].lower() == 'c' or skill['name'].lower() == 'c++' or skill['name'].lower() == 'c/c++' :
                            skills['c/c++'] += 1
                        else:
                            skills[skill['name'].lower()] += 1
            except:
                print('skill')
#                 print(info)
#                 print()
#                 print()
#                 print()
#                 print()
print(companies)
print(location)
print(industry)
print(skills)


def checkAlign(major, industry):
    '''
    this function check major and industry align or not
    if can't determine, print out for manual check
    : param major: input major
    : param industry: input working industry
    '''
    if major == 'computer science' or major == 'computational science' or major == '计算机科学':
        if industry == 'computer software' or industry == 'internet' \
        or industry == 'information technology & services':
            return True
        else:
            print("PoTenTial False!! , ", major, ' ', industry)
            return False
    elif major == 'electrical engineering' or major == 'integrated circuit design' or major == 'nanoscale devices and systems':
        if industry == 'semiconductors' or industry == 'consumer electronics' or industry == 'computer hardware'\
        or industry == 'computer networking' or industry == 'electrical & electronic manufacturing' \
        or industry == 'wireless' or industry == 'telecommunications':
            return True
        else:
            print("PoTenTial False!! , ", major, ' ', industry)
            return False
            
    elif major == 'machine learning and data science' or major == 'intelligent systems':
        print("PoTenTial False!! , ", major, ' ', industry)
        if industry == 'computer software' or industry == 'research':
            return True
        else:
            return False
        
    elif major == 'applied mathematics':
        if industry == 'information technology & services':
            return True
        else:
            print("PoTenTial False!! , ", major, ' ', industry)
            return False
            
    elif major == 'finance, general' or major == 'economics' or major == 'business' or major == 'quantitative finance':
        if industry == 'management consulting' or industry == 'financial services' or \
        industry == 'marketing & advertising' or industry == 'investment banking/venture' or\
        industry == 'banking' or industry == 'venture capital':
            return True
        else:
            print("PoTenTial False!! , ", major, ' ', industry)
            return False
            
    elif major == 'biochemistry and biostatistics' or major == 'bioinformatics and systems biology':
        if industry == 'research' or industry == 'biotechnology':
            return True
        else:
            print("PoTenTial False!! , ", major, ' ', industry)
            return False
    else:
        print('minority major ,', major, ' ', industry)
        return False
    


with open('143dataall.json','r') as f:
    allpeople = f.readlines()
    field_of_study = defaultdict(int)
    industryName = defaultdict(int)
    
    align = 0
    numpeople = len(allpeople)
    
    for person in allpeople:
        info = json.loads(person)
        if info:
            if 'education' in info and 'industryName' in info and info['education'] and 'fieldOfStudy' in info['education'][0]:
            #make sure all of the keys exist
                thisEdu = None
                thisIndustry = None

                # try to merge some of the majors by ckecking whether it is at least 50%
                # align with the exist major
                
                for key in field_of_study:
                    tmp = info['education'][0]['fieldOfStudy'].lower()
                    s = difflib.SequenceMatcher(None, key, tmp)
                    match = s.find_longest_match(0, len(key), 0, len(tmp))
                    
                    
                    if match.size > 0.5 * min(len(tmp), len(key)):
                        field_of_study[key] += 1
                        thisEdu = key
                        break
                if not thisEdu:
                    field_of_study[info['education'][0]['fieldOfStudy'].lower()] += 1
                    thisEdu = info['education'][0]['fieldOfStudy'].lower()
                    
                industryName[info['industryName'].lower()] += 1
                thisIndustry = info['industryName'].lower()
                
                # check a potential match below
                if checkAlign(thisEdu, thisIndustry):
                    align += 1
                    
    print(field_of_study, len(field_of_study))
    print(industryName, len(industryName))
    print(align, " of total ", numpeople)


labels = 'aligned', 'not aligned'
sizes = [align, numpeople - align]
colors = ['gold', 'lightskyblue']
explode = (0.1, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=False, startangle=140)
plt.title('job aligns with major')
plt.axis('equal')
plt.show()

###Andrew



#import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
#figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
##figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.
#
## Data to plot
#labels=['Signal Processing/COMMS','Photonics/Optics','Circuits','Computer CKT Design','Design Courses','Power','Theory Courses','ML/Controls','Programming Courses']
#sizes = [10,6,9,7,8,8,6,4,14]
#
##labels = 'Python', 'C++', 'Ruby', 'Java'
##sizes = [215, 130, 245, 210]
#colors = ['gold', 'lightcyan', 'lightcoral', 'lightskyblue', 'pink', 'lightgreen', 'plum', 'lightgrey', 'lightblue']
#explode = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1)  # explode 1st slice
#
## Plot
#plt.pie(sizes, explode=explode, labels=labels, colors=colors,
#autopct='%1.0f%%', shadow=False, startangle=140)
#
#plt.axis('equal')
#plt.title('ECE Courses\n\n')
#plt.show()

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
#figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

# Data to plot
labels=['Other ECE courses','Programming Courses']
sizes = [58,14]

#labels = 'Python', 'C++', 'Ruby', 'Java'
#sizes = [215, 130, 245, 210]
colors = ['gold', 'lightblue']
explode = (0.0, 0.1)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.0f%%', shadow=False, startangle=140)

plt.axis('equal')

plt.show()

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
#figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

# Data to plot
labels=['Python', 'C/C++', 'Labview','Matlab']
sizes = [8,4,1,1]

#labels = 'Python', 'C++', 'Ruby', 'Java'
#sizes = [215, 130, 245, 210]
colors = ['lightskyblue','gold', 'lightcyan', 'lightcoral']
explode = (0.1, 0.0, 0.0, 0.0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.0f%%', shadow=False, startangle=140)

plt.axis('equal')
plt.title('Languages\n\n')
plt.show()






import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
#figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

# Data to plot
labels=['Python','Matlab', 'Other MAE courses']
sizes = [4,1,66]

#labels = 'Python', 'C++', 'Ruby', 'Java'
#sizes = [215, 130, 245, 210]
colors = ['lightskyblue','pink','gold']
explode = (0.1,0.1, 0.0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.0f%%', shadow=False, startangle=140)

plt.axis('equal')

plt.show()








import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
#figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

# Data to plot
labels=['Higer level CSE Courses','Introduction Programming Courses']
sizes = [63,13]

#labels = 'Python', 'C++', 'Ruby', 'Java'
#sizes = [215, 130, 245, 210]
colors = ['gold', 'lightblue']
explode = (0.0, 0.1)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.0f%%', shadow=False, startangle=140)

plt.axis('equal')

plt.show()

#
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
figure(num=None, figsize=(6, 6), dpi=80, facecolor='w', edgecolor='k')
#figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

# Data to plot
labels=['Python', 'C/C++', 'Java','Matlab']
sizes = [4,3,5,1]

#labels = 'Python', 'C++', 'Ruby', 'Java'
#sizes = [215, 130, 245, 210]
colors = ['lightskyblue','gold', 'pink', 'lightcoral']
explode = (0.0, 0.0, 0.1, 0.0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.0f%%', shadow=False, startangle=140)

plt.axis('equal')
plt.title('Languages\n\n')
plt.show()

###Andrew
