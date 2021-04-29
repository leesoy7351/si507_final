#########################################
##### Name: Soyoung Lee             #####
##### Uniqname: soyolee             #####
#########################################


from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import plotly.graph_objects as go
import sqlite3
import plotly.express as px

BASE_URL = 'https://en.wikipedia.org/wiki/List_of_mass_shootings_in_the_United_States_in_'
CACHE_FILE_NAME = 'cache_final_project.json'
conn = sqlite3.connect("mass_shooting_us.sqlite")
cur = conn.cursor()

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

data_set_by_year_dict = {}

########## 1. Database creation: US Mass Shootings (2018 - 2021)

# data scraping (2018)
year = '2018'
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

soup = BeautifulSoup(response, 'html.parser')
table_parent = soup.find('tbody')
table_trs = table_parent.find_all('tr')
print(len(table_trs))

data_set = []
for i in range(1,len(table_trs)):
    lst = []
    td = table_trs[i].find_all('td')
    lst.append(year)
    lst.append(td[0].text.strip().split(", ")[0].strip())
    lst.append(td[1].text.strip().split(", ")[0].strip().lower())
    lst.append(td[1].text.strip().split(",")[1].split(" (")[0].strip().lower())
    if td[2].sup:
        _ = td[2].sup.extract()
        lst.append(td[2].text.strip())
    else:
        lst.append(td[2].text.strip())
    if td[3].sup:
        _ = td[3].sup.extract()
        lst.append(td[3].text.strip())
    else:
        lst.append(td[3].text.strip())
    lst.append(td[4].text.strip())
    if td[5].sup:
        _ = td[5].sup.extract()
        lst.append(td[5].text.strip())
    else:
        lst.append(td[5].text.strip())
    data_set.append(lst)
    data_set_by_year_dict[year] = data_set

# data scraping (2019 - 2021)
for year in range(2019, 2022):
    cache = open_cache()
    mass_shooting_url = BASE_URL + str(year)
    if (mass_shooting_url in cache.keys()):
        response = cache[mass_shooting_url]
        print('Using cache')
    else:
        response = requests.get(mass_shooting_url)
        cache[mass_shooting_url] = response.text
        print('Fetching')
        save_cache(cache)
        response = cache[mass_shooting_url]

    soup = BeautifulSoup(response, 'html.parser')
    table_parent = soup.find('tbody')
    table_trs = table_parent.find_all('tr')
    print(len(table_trs))

    data_set = []
    for i in range(1,len(table_trs)):
        lst = []
        td = table_trs[i].find_all('td')
        lst.append(year)
        lst.append(td[0].text.strip().split(", ")[0].strip())
        lst.append(td[1].text.strip().split("(")[0].strip())
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
        data_set_by_year_dict[year] = data_set


# creating database and insert rows
create_table='''
create table if not exists "mass_shooting_us"(
    "id" integer primary key autoincrement unique,
    "year" integer not null,
    "date" text,
    "city" text,
    "state" text,
    "dead" integer,
    "injured" integer,
    "total" integer,
    "description" text

    );
    '''
cur.execute(create_table)

insert_table ='''
    insert into mass_shooting_us
    values (null, ?, ?, ?, ?, ?, ?, ?, ?)
'''
for v in data_set_by_year_dict.values():
    for row in v:
        cur.execute(insert_table, row)
conn.commit()


########## 2. Database creation: US state Code
state_cd_url = 'https://www.50states.com/abbreviations.htm'
response_cd = requests.get(state_cd_url)
soup_cd = BeautifulSoup(response_cd.text, 'html.parser')
table_parent_cd = soup_cd.find('tbody')
table_trs_cd = table_parent_cd.find_all('tr')

us_code_lst =[]
for i in range(len(table_trs_cd)):
    each_state = []
    td_cd = table_trs_cd[i].find_all('td')
    each_state.append(td_cd[0].text)
    each_state.append(td_cd[1].text)
    us_code_lst.append(each_state)


create_table='''
create table if not exists "us_code"(
    "id" integer primary key autoincrement unique,
    "state_name" integer not null,
    "code" text
);
'''
cur.execute(create_table)
conn.commit()

insert_table ='''
    insert into us_code
    values (null, ?, ?)
'''
for i in us_code_lst:
    cur.execute(insert_table, i)
conn.commit()

insert_table ='''
    insert into us_code
    values (null, ?, ?)
'''
cur.execute(insert_table, ['Washington, D.C.', 'DC'])
conn.commit()
conn.close()