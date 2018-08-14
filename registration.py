# -*- coding: utf-8 -*-
"""
GS++ :: Tournament game scheduling app

support file for game_schedule.py, allows teams to register for tournament
stores team info into master database

Created on Wed Jun 27 09:15:46 2018

@author: Scott Sandman
"""
from datetime import datetime
import sqlite3

'''NEED TO ADD TEAM REQUESTS AND STORE IN DATABASE'''

def is_valid_email(email):
    """ function evaluates email, returns boolean"""
    if "@" in email and "." in email:
        return True
    else:
        return False

def is_valid_phone(phone):
    """ function evaluates phone number, returns boolean"""
    if len(phone) == 10:
        return True
    else:
        return False

def team_distance(str):
    """
    function to weight teams distance from tournament for use
    in sorting teams prior to scheduling; higher weighted numbers give a team's
    request priority.
    
    team = a str with city and state (ex. 'Charleston, SC')
    
    current weights are setup with Charleston, SC as the base city
    
    returns an integer
    
    state abbrevations courtesy of Jeff Paine, 
    https://gist.github.com/JeffPaine/3083347
    """
    states = {"AL": 2, "AK": 10, "AZ": 6, "AR": 4, "CA": 6, "CO": 6, "CT": 5,
              "DC": 3, "DE": 3, "FL": 3, "GA": 1, "HI": 10, "ID": 6, "IL": 4,
              "IN": 4, "IA": 5, "KS": 5, "KY": 2, "LA": 4, "ME": 6, "MD": 3, 
              "MA": 5, "MI": 5, "MN": 6, "MS": 3, "MO": 4, "MT": 6, "NE": 5,
              "NV": 6, "NH": 5, "NJ": 4, "NM": 6, "NY": 5, "NC": 1, "ND": 6,
              "OH": 4, "OK": 5, "OR": 6, "PA": 4, "RI": 5, "SC": 0, "SD": 6, 
              "TN": 2, "TX": 5, "UT": 6, "VT": 6, "VA": 2, "WA": 6, "WV": 3,
              "WI": 5, "WY": 6}
    if str not in states:
        return False
    else:
        return states.get(str)   
    
#print(team_distance(str = 'AK'))

def registration():
    """
    create a function that returns user registration data from tournament inputs
    collects the following information:
        select tournament (from tournament table in master db)
        team name
        team location
        age classification
        registration date
        contact information (coach's name, email, cellphone)
    user input from registration form is stored in team table in master db
    """
    present = datetime.now()
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    
    """need to verify table selection to only return active tournaments"""
    
    cursor.execute('SELECT id, title, start, end FROM tournaments WHERE\
                   start > ?', [present])
    tournaments = cursor.fetchall()
    db.close()
#    print(tournaments)    
    while True:
        temp = []
        for t in range(len(tournaments)):
            temp.append(tournaments[t][0])
            print(tournaments[t])
        try:
            tourn_id = int(input('Enter the number of the tournament you wish to enter: '))
            if tourn_id not in temp:
                print('Selection is not available.')
                continue
        except ValueError:
            print('Invalid Input!')
            continue
        print('You have selected the ', tournaments[tourn_id - 1][1])
        print('')
        ans = input("If this is correct press 'y', if not press any other key. ")
        if ans == 'y':
            break
        else:
            continue
        
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    cursor.execute('''SELECT age FROM age WHERE tourn_id=? and open > ?''', (tourn_id, 0))
    age_groups = cursor.fetchall()
    db.close()
    while True:
        age_temp = []
        for a in range(len(age_groups)):
            age_temp.append(age_groups[a][0])
        print('Age groups available for the ', tournaments[tourn_id - 1][1], 'are: \n',
              age_temp)
        team_age_group = input('Enter team age division from above (ex. 10u): ')
        if not team_age_group:
            print('You must enter a valid age group!')
            continue
        if team_age_group not in age_temp:
            print('Invalid age group!')
            continue
        else:
            break        
    while True:
        team_name = input('Enter team name (ex. Carolina Prospects): ')
        if not team_name:
            print('Team name required!')
            continue
        else:
            break
    while True:
        team_location = input('Enter team city and state (ex. Charleston, SC): ')
        if not team_location:
            print('Team location required!')
            continue
        state = team_location[-2:]
        if team_distance(state) is False:
            print('Please enter a valid state!')
            continue
        else:
            team_weight = team_distance(state)
            break
    while True:
        contact_name = input('Enter team contact name: ')
        if not contact_name:
            print('Contact name required!')
            continue
        else:
            break
    while True:
        contact_email = input('Enter team contact email: ')
        if is_valid_email(contact_email) is False:
            print('Valid email required!')
            continue
        else:
            break
    while True:
        contact_phone = input('Enter team phone (xxxxxxxxxx): ')
        if is_valid_phone(contact_phone) is False:
            print('Valid phone number required!')
            continue
        else:
            break
    
    registration = datetime.now()
    
    db = sqlite3.connect("data/master")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO teams(team, location, age, contact, email, phone, \
                                        registration, weight, tourn_id)
                   VALUES(?,?,?,?,?,?,?,?,?)''', 
                   (team_name, team_location, team_age_group, contact_name,
                    contact_email, contact_phone, registration, team_weight, tourn_id))
    db.commit()
# ----subtract 1 from open slots
    slots = cursor.execute('''SELECT open FROM age WHERE tourn_id=? and age = ?''',
                           (tourn_id, team_age_group))
    avail_slots = slots.fetchone()
    new_slots = avail_slots[0] - 1
    cursor.execute('''UPDATE age SET open=? WHERE tourn_id=? and age=?''', 
                   (new_slots, tourn_id, team_age_group))
    db.commit()
    """
    add exception error here
    """
    db.close()


#registration()


