from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import plotly.graph_objects as go
import sqlite3

BASE_URL = 'https://en.wikipedia.org/wiki/List_of_mass_shootings_in_the_United_States_in_'
year = '2021'
CACHE_FILE_NAME = 'cache_final_project.json'

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''

    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILE_NAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

cache = open_cache()
mass_shooting_url = BASE_URL + year
if (mass_shooting_url in cache.keys()):
    response = cache[mass_shooting_url]
    print('Using cache')
else:
    response = requests.get(mass_shooting_url)
    cache[mass_shooting_url] = response.text
    print('Fetching')
    save_cache(cache)
    response = cache[mass_shooting_url]
# response = requests.get(mass_shooting_url)
soup = BeautifulSoup(response, 'html.parser')
table_parent = soup.find('tbody')
table_trs = table_parent.find_all('tr')

data_set = []
for i in range(1,len(table_trs)):
    lst = []
    td = table_trs[i].find_all('td')
    lst.append(year)
    lst.append(td[0].text.strip())
    lst.append(td[1].text[:-4].strip())
    lst.append(td[2].text.strip())
    if td[3].sup:
        _ = td[3].sup.extract()
        lst.append(td[3].text.strip())
    else:
        lst.append(td[3].text.strip())
    if td[4].sup:
        _ = td[4].sup.extract()
        lst.append(td[4].text.strip())
    else:
        lst.append(td[4].text.strip())
    lst.append(td[5].text.strip())
    if td[6].sup:
        _ = td[6].sup.extract()
        lst.append(td[6].text.strip())
    else:
        lst.append(td[6].text.strip())
    data_set.append(lst)

#df_2021 = pd.DataFrame(data_set, columns = ['year', 'date', 'city', 'state', 'dead', 'injured', 'total', 'description'])

# Database creation: US state Code
# state_cd_url = 'https://www.50states.com/abbreviations.htm'
# response_cd = requests.get(state_cd_url)
# soup_cd = BeautifulSoup(response_cd.text, 'html.parser')
# table_parent_cd = soup_cd.find('tbody')
# table_trs_cd = table_parent_cd.find_all('tr')

# us_code_lst =[]
# for i in range(len(table_trs_cd)):
#     each_state = []
#     td_cd = table_trs_cd[i].find_all('td')
#     each_state.append(td_cd[0].text)
#     each_state.append(td_cd[1].text)
#     us_code_lst.append(each_state)

# conn = sqlite3.connect("mass_shooting_us.sqlite")
# cur = conn.cursor()

# create_table='''
# create table if not exists "us_code"(
#     "id" integer primary key autoincrement unique,
#     "state_name" integer not null,
#     "code" text
# );
# '''
# cur.execute(create_table)
# conn.commit()

# insert_table ='''
#     insert into us_code
#     values (null, ?, ?)
# '''
# for i in us_code_lst:
#     cur.execute(insert_table, i)
# conn.commit()

# insert_table ='''
#     insert into us_code
#     values (null, ?, ?)
# '''
# cur.execute(insert_table, ['Washington, D.C.', 'DC'])
# conn.commit()

# Database creation: 2021 mass shooting database
# create_table='''
# create table if not exists "db_2021"(
#     "id" integer primary key autoincrement unique,
#     "year" integer not null,
#     "date" text,
#     "city" text,
#     "state" text,
#     "dead" integer,
#     "injured" integer,
#     "total" integer,
#     "description" text

# );
# '''
# cur.execute(create_table)

# insert_table ='''
#     insert into db_2021
#     values (null, ?, ?, ?, ?, ?, ?, ?, ?)
# '''
# for i in data_set:
#     cur.execute(insert_table, i)
# conn.commit()

# cur.execute('SELECT c.code, count(d.id), sum(injured), sum(dead) FROM db_2021 d join us_code c on c.state_name = d.state where year = 2021 group by state' )
# for row in cur:
#     print(row)

#df_2021 = pd.DataFrame(data_set, columns = ['year', 'date', 'city', 'state', 'dead', 'injured', 'total', 'description'])


# df['text'] = df['state'] + '<br>' + \
#     'dead ' + df['dead'] + ' injured ' + df['injured'] + '<br>' + \
#     'total ' + df['total']

# fig = go.Figure(data=go.Choropleth(
#     locations=df['state'],
#     z=df_group['year'].astype(float),
#     locationmode='USA-states',
#     colorscale='Reds',
#     autocolorscale=False,
#     text=df['text'], # hover text
#     marker_line_color='white', # line markers between states
#     colorbar_title="Millions USD"
# ))

# fig.update_layout(
#     title_text='2011 US Agriculture Exports by State<br>(Hover for breakdown)',
#     geo = dict(
#         scope='usa',
#         projection=go.layout.geo.Projection(type = 'albers usa'),
#         showlakes=True, # lakes
#         lakecolor='rgb(255, 255, 255)'),
# )

# fig.show()




# file1 = open("table_parent.txt", "a", encoding='utf-8')
# file1.write(table_parent.prettify())
# file1.close()


