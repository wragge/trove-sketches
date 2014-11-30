"""

Quick Python sketch to graph numbers of Trove contributors and resources 
from each Australian state against the population of that state.

Graphs are created using Plotly's Python API.

Add your Trove & Plotly credentials to credentials_fillmein.py and
save as credentials.py.

"""
import requests
import plotly.plotly as py
from plotly.graph_objs import *

from credentials import TROVE_API_KEY, PLOTLY_ID, PLOTLY_KEY

py.sign_in(PLOTLY_ID, PLOTLY_KEY)

#Trove API url to get contributor details
TROVE_URL = 'http://api.trove.nla.gov.au/contributor/?encoding=json&reclevel=full&key={}'

#Mapping NUC keys to state names
STATES = {
		'A': 'ACT',
		'N': 'NSW',
		'X': 'NT',
        'Q': 'Qld',
		'S': 'SA',
		'T': 'Tas',
		'V': 'Vic',
		'W': 'WA'
}

#State populations by NUC key
POPN = {
        'A': 385600,
        'N': 7500600,
        'X': 243700,
        'Q': 4708500,
        'S': 1682600,
        'T': 514700,
        'V': 5821300,
        'W': 2565600
}

#Total population of Australia
TOTAL_POP = 23425700

#Get contributor data from Trove
response = requests.get(TROVE_URL.format(TROVE_API_KEY))
data = response.json()
print data['response']['total']

#Loop through contributors
org_count = 0
resources = 0
states = {}
for contributor in data['response']['contributor']:
	code = ''
	total = contributor['totalholdings']
	if total > 0:
		if 'nuc' in contributor:
            #First letter of NUC id indicates the state.
			code = contributor['nuc'][0][0]
			print code
        #Sometimes the parent doesn't have a NUC, so get state key from children
		elif 'children' in contributor:
			for child in contributor['children']['contributor']:
				if 'nuc' in child:
					code = child['nuc'][0][0]
					break
		if code:
            #Add org counts and resource totals to state totals
			try:
				states[code]['count'] += 1
				states[code]['total'] += total
			except KeyError:
				states[code] = {}
				states[code]['count'] = 1
				states[code]['total'] = total
			org_count += 1
			resources += total

labels = STATES.values()
#Turn state populations into percentages of Australian total
pop = [(float(pop)/TOTAL_POP)*100 for pop in POPN.values()]
orgs = []
items = []
for letter in STATES.keys():
    #Turn org counts and resource totals into pecentages.
	orgs.append((states[letter]['count']/float(org_count))*100)
	items.append((states[letter]['total']/float(resources))*100)

#From here this is all standard Plotly stuff
trace1 = Bar(
		x=labels,
		y=orgs,
        name='Contributors'
	)

trace2 = Bar(
        x=labels,
        y=items,
        name='Resources'
    )

trace3 = Bar(
        x=labels,
        y=pop,
        name='Population'
    )

data = Data([trace1, trace2, trace3])
layout = Layout(
    barmode='group',
    xaxis=XAxis(
        title='State'
    ),
    yaxis=YAxis(
        title='Percentage of total'
    )
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Trove by state')
