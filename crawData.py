import csv
from linkedin_api import Linkedin
title = set()

for i in range(1, 16):
    with open('143_data/%s.csv'%i, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if row[1] == 'Title_link':
                continue
            title.add(row[1])
    csvfile.close()

p_list = []
for t in title:
    p_list.append(t.split('/')[-2])

# Authenticate using any Linkedin account credentials
api = Linkedin('abritten@ucsd.edu', 'Hello!11')

pro_list = []
n = 1
for p in p_list:

    profile = api.get_profile(p)
    pro_list.append(profile)
    
    print(n, ' ', p)
    n+= 1

p_list = []
with open('profile_list_remains.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # GET a profile
        
        p_list.append(line.strip())

import json
with open('143dataanother146.json','w') as f:
    for d in pro_list:
        j = json.dumps(d)
        f.writelines(j)
        f.writelines('\n')

