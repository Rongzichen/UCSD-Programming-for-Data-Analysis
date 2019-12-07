import json
from collections import defaultdict
import difflib
import matplotlib.pyplot as plt
import plotly
# import plotly.plotly as py
import plotly.offline as of
import plotly.graph_objs as go
import math
import addfips
import xlrd

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def findStat():
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

    return [companies, location, industry, skills]


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
    

def plotAlignment():
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

# seperate the dict to be two lists
def seperateData(data):
    """
    this function is used to seperate the data format from dictionary to 
    the two list
    : param data: dictionary
    """
    assert isinstance(data, dict)
    dictionary = dict(data)
    keys = dictionary.keys()
    values = dictionary.values()
    return list(keys), list(values)

# seperate the data for company information
def seperateDataCompany(data):
    """
    this function is used to seperate the data format from dictionary to 
    the two list
    : param data: dictionary
    """
    assert isinstance(data, dict)
    dictionary = dict(data)
    tmp = dictionary.pop('University of California, San Diego - Jacobs School of Engineering')
    dictionary['University of California San Diego'] += tmp
    tmp = dictionary.pop('Amazon Web Services (AWS)')
    dictionary['Amazon'] += tmp
    
    keys = list(dictionary.keys())
    values = list(dictionary.values())    
    return (keys), (values)

# Set the top most skills we want to display
def getHighest(key, values, num):
    """
    this function is used to get the num of most highest data to display
    : param key: list
    : param values: list
    : param num: int
    """
    assert isinstance(key, list)
    assert isinstance(values, list)
    assert isinstance(num, int)
    key, values = getSorted(key, values)
    newKey = key[:num]
    newValue = values[:num]
    return newKey, newValue

# Sort the key and values
def getSorted(key, values):
    """
    this function is used to sort the two list in descending format
    : param key: list
    : param values: list
    """
    assert isinstance(key, list)
    assert isinstance(values, list)
    tmpDict = dict(zip(key, values))
    tmp = sorted(tmpDict.items(),key=lambda item:item[1],reverse=True)
    key = [i[0] for i in tmp]
    value = [i[1] for i in tmp]
    return key, value


# seperate the data for location information
def seperate_Loc_Data(data, us_state_abbrev):
    """
    this function is used to seperate the location data 
    : param data: list
    """
    assert data is not None
    dictionary = dict(data)
    keys = dictionary.keys()
    tmp = list(keys)
    values = dictionary.values()
    res = []
    for elem in keys:
        state = elem[1].strip()
        if state in us_state_abbrev:
            res.append(us_state_abbrev[state])
    return res, list(values)

def seperate_City_Data(data, us_state_abbrev):
    """
    this function is used to seperate the city data 
    : param data: list
    """
    assert data is not None
    dictionary = dict(data)
    keys = dictionary.keys()
    tmp = list(keys)
    values = dictionary.values()
    res = []
    for elem in keys:
        state = elem[1].strip()
        city = elem[0].strip()
#         print(city)
        if state in us_state_abbrev:
            res.append(city)
    return res, list(values)


def seperate_City_State_Data(data, us_state_abbrev):
    """
    this function is used to seperate the state and city data 
    : param data: list
    """
    assert data is not None
    dictionary = dict(data)
    keys = dictionary.keys()
    tmp = list(keys)
    v = list(dictionary.values())
    values = []
    res = []
    for i in range(len(keys)):
        state = tmp[i][1].strip()
        city = tmp[i][0].strip()
#         print(city)
        if state in us_state_abbrev:
            res.append((state, city))
            values.append(v[i])
    return res, list(values)

# count statistics data for loc and values
def coordinate_Loc_Val(loc, values):
    """
    this function is used to coordinate the location and it's values
    : param data: list
    """
    assert loc is not None
    assert values is not None
    res = dict()
    for i in range(len(loc)):
        if loc[i] not in res: res[loc[i]] = values[i]
        else: res[loc[i]] += values[i]
    return list(res.keys()), [math.log(i+1) for i in list(res.values())]

# take log to the data and see if it performance better
def log_the_value(label, values):
    '''
    Take the log to the data to make the visualization better
    '''
    assert label is not None
    assert values is not None
    return list(label), [(math.log(i+1)) for i in values]


def coordinate_City_Val(loc, city, values):
    """
    this function is used to coordiniate the city and it's population value
    : param data: list
    """
    assert loc is not None
    assert city is not None
    assert values is not None
    res = dict()
    print(loc)
    print(city)
    for i in range(len(loc)):
        if (loc[i],city[i]) not in res: res[(loc[i],city[i])] = values[i]
        else: res[(loc[i],city[i])] += values[i]
    return list(res.keys()), list(res.values())



def getFIPS_General(city_tuple, values): # not used as the addfips lib can not recognize some cities
    '''
    This function is to get the fips code from the city name
    : param city_tuple: tuple
    '''
    assert isinstance(values, list)
    res = []
    af = addfips.AddFIPS()
#     print(city_tuple)
#     print(values)
    for i in range(len (values)):
        res.append(af.get_county_fips(city_tuple[i][1], state=city_tuple[i][0]))
    res, values = getSorted(res, values)
    return res


def getFIPS(city_tuple, values):
    '''
    This function is to get the fips code from the city name- but used some hardcoded value
    : param city_tuple: tuple
    '''
    assert isinstance(values, list)
#     print(city_tuple)
#     print(values)
    res = []
    v = []
    cityName = []
    for i in range(len(values)):
        if city_tuple[i][1] == 'San Diego County':
            res.append('06073')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Sunnyvale':
            res.append('06085')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'San Francisco':
            res.append('06075')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Seattle':
            res.append('63000')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Redmond':
            res.append('57535')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Palo Alto':
            res.append('06086') # should be the same with sunnyvale
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'DuPage County':
            res.append('17043')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Mountain View':
            res.append('06087') # should be the same with sunnyvale
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Los Angeles':
            res.append('06037')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Morgan Hill':
            res.append('06074') # Should be the same with San Fransisco
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Castro Valley':
            res.append('06075')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Irvine':
            res.append('06059') # can't find it
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif (city_tuple[i][1] == 'Cupertino' or city_tuple[i][1] == 'San Jose'):
            res.append('06081')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'El Cajon':
            res.append('06071')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Trabuco Canyon':
            res.append('06065')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Santa Clara':
            res.append('06085')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Orange County':
            res.append('06059')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Corona':
            res.append('06011')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Trabuco Canyon':
            res.append('06065')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
        elif city_tuple[i][1] == 'Trabuco Canyon':
            res.append('06065')
            v.append(values[i])
            cityName.append(city_tuple[i][1])
    return res, v, cityName






