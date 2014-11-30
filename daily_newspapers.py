"""

Quick Python sketch to graph numbers of daily newspapers in Trove by year.

A 'daily' newspaper is defined as one that has more than 300 issues in a given year.

Graphs are created using Plotly's Python API.

Add your Trove & Plotly credentials to credentials_fillmein.py and
save as credentials.py.

"""
import requests
import time
import plotly.plotly as py
from plotly.graph_objs import *

from credentials import TROVE_API_KEY, PLOTLY_ID, PLOTLY_KEY

py.sign_in(PLOTLY_ID, PLOTLY_KEY)

#Trove API url for all newspaper titles
titles_url = 'http://api.trove.nla.gov.au/newspaper/titles?encoding=json&key={}'
#Trove API url for details of an individual newspaper title
title_url = 'http://api.trove.nla.gov.au/newspaper/title/{}?encoding=json&key={}&include=years'

#Get list of all newspaper titles in Trove
response = requests.get(titles_url.format(TROVE_API_KEY))
titles = response.json()

years = {}
x = []
y = []

#Loop through all titles and get title id
for title in titles['response']['records']['newspaper']:
    title_id = title['id']
    #Get details for title
    response = requests.get(title_url.format(title_id, TROVE_API_KEY))
    details = response.json()
    #Loop through years and look at the number of issues
    for year in details['newspaper']['year']:
        date = int(year['date'])
        count = int(year['issuecount'])
        #If the number of issues is greater than 300, we'll say it's a daily in the given year
        if count > 300:
            print 'Daily!'
            #Update the daily count for the current year
            try:
                years[date] += 1
            except KeyError:
                years[date] = 1
    #Be nice to Trove API
    time.sleep(.5)

for year in sorted(years):
    if year < 1955:
        x.append(year)
        y.append(years[year])

#Plotly stuff from here on...
trace1 = Scatter(
        x=x,
        y=y
    )

layout = Layout(
    title='Daily newspapers in Trove',
    xaxis=XAxis(
        title='Year'
    ),
    yaxis=YAxis(
        title='Number of daily newspapers in Trove'
    )
)

data = Data([trace1])
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='daily-papers')