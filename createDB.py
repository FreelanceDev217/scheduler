# -*- coding: utf-8 -*-
"""
GS++ :: Tournament game scheduling app

support file for game_schedule.py, creates database and associated tables

Created on Wed Jun 27 09:15:46 2018

@author: Scott Sandman
"""
import sqlite3

db = sqlite3.connect("data/master", detect_types = sqlite3.PARSE_DECLTYPES)
cursor = db.cursor()
cursor.execute('''PRAGMA foreign_key = on''')
cursor.execute('''CREATE TABLE tournaments
               (id INTEGER PRIMARY KEY,
               title TEXT,
               created DATE,
               start DATE, 
               end DATE,
               days INTEGER)''')
cursor.execute('''CREATE TABLE fields
               (id INTEGER PRIMARY KEY,
               field TEXT,
               start DATE,
               last DATE,
               tourn_id INTEGER,
               FOREIGN KEY(tourn_id) REFERENCES tournaments(id))''')
cursor.execute('''CREATE TABLE age
               (id INTEGER PRIMARY KEY,
               age TEXT,
               start DATE,
               last DATE,
               time REAL,
               games INTEGER,
               max INTEGER,
               open INTEGER,
               field_id INTEGER,
               tourn_id INTEGER,
               FOREIGN KEY(tourn_id) REFERENCES tournaments(id))''')
cursor.execute('''CREATE TABLE teams
               (id INTEGER PRIMARY KEY,
               team TEXT,
               location TEXT,
               age TEXT,
               contact TEXT,
               email TEXT,
               phone TEXT,
               registration DATE,
               weight INTEGER,
               tourn_id INTEGER,
               FOREIGN KEY(tourn_id) REFERENCES tournaments(id))''')
db.commit()
db.close()









