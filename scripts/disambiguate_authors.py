""" Script for performing Scopus searches to disambiguate authors

    Some important notes:
    - The member lists are stored in Excel files, and not every one of these files has the 'First' and 'Last'
      columns. You will need to ensure that these columns exists in the pandas DataFrame
"""

from ..utils import elsapy_utils as ep
import pandas as pd
import json

pd.options.mode.chained_assignment = None  # default='warn'

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)

url = 'https://api.elsevier.com/content/search/author?query='

headers = {
    "Accept": "application/json",
    "X-ELS-APIKey": config['apikey'],
    "X-ELS-Insttoken": config['insttoken'],
    "X-RateLimit-Reset": None
}

filepath = '../../Datasets/{}_missing_members.xlsx'
site = 'WCHRI'  # change this to the corresponding site

df_site = pd.read_excel(filepath.format(site), header=0)

# create empty column for author ids
df_site['Auid'] = None

# set up the queries
df_site['request'] = url + df_site.copy().apply(
    lambda x: ep.build_query(x['First'], x['Last']),
    axis=1
)

# perform the searches
assert isinstance(headers, dict)
ep.api_search(df_site, letters=None, headers=headers)

# find the new missing ids
missing = df_site[df_site['auid'].isna()]
not_missing = df_site[~df_site['auid'].isna()]

print(
    '{}: {} out of {} authors identified ({:.2f}%)\n{} still missing'.format(
        site,
        len(not_missing),
        len(df_site),
        len(not_missing)/len(df_site)*100,
        len(missing)
    )
)

not_missing.to_excel(site + '_disambiguated_jan6.xlsx')
