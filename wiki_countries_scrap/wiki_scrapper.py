from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas
import re
import sqlite3

def get_soup():
    url = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
    page = urlopen(url)
    soup = bs(page, 'lxml')
    soup.prettify()
    return soup


def get_list_of_countries():
    spans = get_soup().select('tr > td > span')
    countries = []
    for span in spans:
        if span.get('id') == None:
            continue
        elif span.get('id') == 'Other_states':
            continue
        else: countries.append(span.get('id'))
    return countries

def create_table():
    conn = sqlite3.connect('list_of_countries.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS list_countries (number INTEGER, name TEXT)')
    conn.commit()
    c.close()
    conn.close()

def write_list_in_database():
    conn = sqlite3.connect('list_of_countries.db')
    c = conn.cursor()
    number = 0
    for country in get_list_of_countries():
        c.execute('INSERT INTO  list_countries (number, name) VALUES (?,?)', (number, country))
        conn.commit()
    c.close()
    conn.close()


create_table()
write_list_in_database()






