# UCSD-Programming-for-Data-Analysis
# File structure
143_data is all the public id used to craw data

143CleanData.ipynb includes the data cleaning part and data visualization part

143dataall.json contains all the raw data we collected

ECE143.pptx is our presentation slides

crawData.ipynb (crawData.py) is the crawler we used

FirstDegreComparison.ipynb includes the degree comparison part

dataclean.py is our data cleaning part


# Our code including three parts
# 1. Data crawler

The file is crawData.py

modules including: 

```
import csv
from linkedin_api import Linkedin
```

```
run command: python crawData.py
```

In order to use this crawler, first:

Using **Python >= 3.6**:

```
$ pip install git+https://github.com/tomquirk/linkedin-api.git
```

And you need to authenticate using any Linkedin account credentials like:

api = Linkedin('username', 'password')

(Be careful, LinkedIn will restricted your account if you craw data for some time, please do not use your main account)

The cralwer function is 

```
profile = api.get_profile(p)
```
p is the public id in the file 143_data

# 2. Data clean

The file is dataclean.py

```
run command: python dataclean.py
```

modules including:
```
import json
from collections import defaultdict
import difflib
```

The data cleaning including check for major alignment, which also inevitably need some manual check

# 3. Data Visualization

The file is proj_script.py

```
run command: python proj_script.py
```

modules including:
```
import json
from collections import defaultdict
import plotly
import plotly.offline as of
import plotly.graph_objs as go
import math
import addfips
import xlrd
import difflib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import plotly.figure_factory as ff
import geopandas
import pandas as pd
from wordcloud import WordCloud
```
