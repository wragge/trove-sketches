"""

Quick Python sketch to graph numbers of books in Trove by languages
spoken at home in Australia according to 2011 census.

Graphs are created using Plotly's Python API.

Add your Trove & Plotly credentials to credentials_fillmein.py and
save as credentials.py.

"""
import operator
import requests
import plotly.plotly as py
from plotly.graph_objs import *

from credentials import TROVE_API_KEY, PLOTLY_ID, PLOTLY_KEY

py.sign_in(PLOTLY_ID, PLOTLY_KEY)

#Australian population
total_pop = 23425700

#Languages spoken at home according to 2011 Australian census by population
langs_spoken = {
    'Mandarin': 336178,
    'Italian': 299829,
    'Arabic': 287171,
    'Cantonese': 263538,
    'Greek': 252211,
    'Vietnamese': 233388,
    'Tagalog': 136846,
    'Spanish': 117493,
    'Hindi': 111349,
    'German': 80366,
    'Korean': 79784,
    'Punjabi': 71231,
    'Macedonian': 68843,
    'Persian': 62340,
    'Australian Indigenous Languages': 61749,
    'Croatian': 61545,
    'Turkish': 59625,
    'French': 57741,
    'Indonesian': 55861,
    'Serbian': 55114,
    'Polish': 50696,
    'Tamil': 50145,
    'Sinhalese': 48192,
    'Russian': 44054,
    'Japanese': 43690,
    'Dutch': 37247,
    'Urdu': 36835,
    'Thai': 36665,
    'Samoan': 36574,
    'Bengali': 35647,
    'Afrikaans': 35027,
    'Maltese': 34398,
    'Gujarati': 34210,
    'Portuguese': 33348,
    'Aramaic': 31317,
    'Khmer': 29518,
    'Nepali': 27156,
    'Malayalam': 25108,
    'Chinese': 23792
}

#Combine categories to match Trove language categories
lang_mappings = {
        'Mandarin': 'Chinese',
        'Cantonese': 'Chinese'
    }

#Match labels between census and Trove
lang_labels = {
    'Australian Indigenous Languages': 'Australian languages',
    'Punjabi': 'Panjabi'
}

url = 'http://api.trove.nla.gov.au/result?q= &zone=book&encoding=json&facet=language&n=0&key={}'

#Apply mappings to create new dictionary of languages/population
langs_mapped = dict(langs_spoken)
for lang, total in langs_spoken.items():
    if lang in lang_mappings:
        new_lang = lang_mappings[lang]
        langs_mapped[new_lang] += total
        del langs_mapped[lang]
 
#Sort by population
langs_mapped = sorted(langs_mapped.items(), key=operator.itemgetter(1))

#Get Trove data
response = requests.get(url.format(TROVE_API_KEY))
data = response.json()

trove_total = int(data['response']['zone'][0]['records']['total'])

langs_trove = {}

#Loop through Trove language facets to save totals
for lang in data['response']['zone'][0]['facets']['facet']['term']:
    langs_trove[lang['display']] = int(lang['count'])

data_spoken = []
data_trove = []
data_labels = []

#For each language spoken at home save populations and Trove totals as percentages.
for lang, total in langs_mapped:
    data_labels.append(lang)
    data_spoken.append((total/float(total_pop))*100)
    if lang in lang_labels:
        label = lang_labels[lang]
    else:
        label = lang
    data_trove.append((langs_trove[label]/float(trove_total))*100)

#Plotly stuff from here on
trace1 = Bar(
        y=data_labels,
        x=data_spoken,
        orientation='h',
        name='Population',
        line=Line(width=20)
    )

trace2 = Bar(
        y=data_labels,
        x=data_trove,
        orientation='h',
        name='Books'
    )

data = Data([trace1, trace2])
layout = Layout(
    title='Languages of Trove books compared to Australian population',
    barmode='group',
    bargap=0.3,
    autosize=False,
    height=1000,
    width=1000,
    xaxis=XAxis(
        title='Percentage of total'
    ),
    yaxis=YAxis(
        title='Language spoken at home in Australia (excluding English)'
    ),
    margin=Margin(
        l=250,
        pad=5
    ),
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Trove books languages')
