# -*- coding: utf-8 -*-
"""
GS++ :: Tournament game scheduling app

Sets up the tournament parameters by receiving user input

All tables are stored in an sqlite3 db file -- "data/master"
    tournaments - parent
    age - child, Foreign Key is tournament id
    field - child, Foreign Keys are tournament and age ids.

The title, start date, end date and creation date are stored in the "tournaments"
table.

Field names, time of day to start scheduling and latest game start time are
stored in the "fields" table.

Age group, minimum games each team will be scheduled to play, time between game
start times, max number of teams per age group, and field assignments are stored
in the "age" table 

Created on Wed Jun 27 09:15:46 2018
@author: Scott Sandman
"""
#import time
from datetime import datetime
import sqlite3


def is_valid_time(time):
    """ evaluates a user input time. returns a boolean"""
    time_format = '%H:%M %p'
    is_valid = True
    try:
        datetime.strptime(time, time_format)
    except ValueError:
        is_valid = False
    if is_valid:
        return True
    else:
        return False

def avail_time(start, last, length):
    """calculates the time between when the first game begins until the last
    game can start. returns a float.
    """
    start_dt = datetime.strptime(start, '%I:%M %p')
    last_dt = datetime.strptime(last, '%I:%M %p')
    dt = last_dt - start_dt
    sec = dt.seconds
    hours = sec / 60 / 60
    return hours + length

def create_tournament():
    """
    requests the following user inputs:
        tournament title (string)
        tournament start/end dates (mm-dd-yyyy) (string)
        
        tournament age classifications (ex. 8u, 10u) (string)
        minimum number of games per teams (integer)
        available age groups
        fields to be scheduled
    stores data in the tournament table in the tournament database
    """
    while True:
        title = input('Enter Tournament Title: ')
        if not title:
            print('Tournament Title cannot be blank.')
            continue
        else:
            break
 
    created_on = datetime.now()
    
    while True:
        try:
            month, day, year = input('Enter Tournament start date (mm-dd-yyyy): ').split('-')
            start_date = datetime(int(year), int(month), int(day))
        except ValueError:
            print('Invalid date!')
            continue
        if start_date < created_on:
            print('Date cannot be in the past!')
            continue
        else:
            break
    while True:
        try:
            month, day, year = input('Enter Tournament end date (mm-dd-yyyy): ').split('-')
            end_date = datetime(int(year), int(month), int(day))
        except ValueError:
            print('Invalid date!')
            continue
        if end_date < start_date:
            print('End date must occur after Start date!')
            continue
        else:
            break
        
    delta_days = end_date - start_date
    tourn_days = delta_days.days + 1
    
    db = sqlite3.connect("data/master")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO tournaments(title, created, start, end, days)
                   VALUES(?,?,?,?,?)''', 
                   (title, created_on, start_date, end_date, tourn_days))
    db.commit()
    """
    add exception error here
    """
# ---- get tournament id for input as table FOREIGN KEY
    tid = cursor.execute('SELECT id FROM tournaments WHERE title=?', [title])
    t_id = tid.fetchall()
    tourn_id = t_id[0][0] 
    db.close()

# ---- enter fields available for tournament ---    
    avail_fields = []
    while True:
        try:
            num_fields = int(input('Enter number of fields to be used: '))
        except ValueError:
            print("Invalid input!")
            continue
        if num_fields <= 0:
            print("Invalid input!")
            continue
        else:
            break
    for i in range(num_fields):
        while True:
            field = input('Enter name of field number {}: '.format(i + 1))
            if not field:
                print('Field cannot be blank!')
                continue
            if field in avail_fields:
                print('You have already entered that field.')
                continue
            else:
                avail_fields.append(field)
                break
        while True:
            start_time = input('Enter earliest game start time \
                               (ex. 9:00 am): ')
            if is_valid_time(start_time) == False:
                print('Invalid time entered.')
                continue
            else:
                break
        while True:
            last_time = input('Enter latest game start time (ex. 8:00 pm): ')
            if is_valid_time(last_time) == False:
                print('Invalid time entered.')
                continue
            else:
                break
        
        db = sqlite3.connect('data/master')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO fields(field, start, last, tourn_id)
                        VALUES(?,?,?,?)''',
                        (field, start_time, last_time, tourn_id))
        db.commit()
        """
        add exception error here
        """
        db.close()
        
# ---- enter available age groups for tournament --- 
    age_groups = ['8u', '9u', '10u', '11u', '12u', '13u', '14u', '15u', '16u', '17u']
    while True:
        avail_age_groups = input('Enter available age groups (ex. 8u, 10u, 12u): ')
        if not avail_age_groups:
            print('Age group required')
            continue
        temp_age_groups = avail_age_groups.split(', ')
        for age in temp_age_groups:
            if age not in age_groups:
                print('Invalid age group: ', age)
                continue
            else:
                break
        break
    for age in temp_age_groups:
        while True:
            game_time_length = float(input("Enter length of game time in hours \
                                           (ex. 1.5 for  1-1/2 hours) \
                                           for the {} age group: ".format(age)))
            '''add error handling'''
            if game_time_length <= 0:
                print('Game time length cannot be negative or 0!')
                continue
            else:
                break
        while True:
            min_games = int(input("Enter minimum number of games for each \
                                  team in the {} age group: ".format(age)))
            
            '''Need to except ValueError here'''
            
            if min_games == 0:
                print('Minimum games cannot be 0.')
                continue
            else:
                print("")
                break
    # ---- assign field(s) to age group
        db = sqlite3.connect('data/master')
        cursor = db.cursor()
        select = cursor.execute('''SELECT id, field FROM fields WHERE \
                                 tourn_id=?''', [tourn_id])
        field_select = select.fetchall()
        db.close()
       
        while True:
            field_temp = []
            for f in range(len(field_select)):
                field_temp.append(f + 1)
                print(f + 1, field_select[f][1])
            field_by_age = int(input('Enter number of field(s) to assign (ex. 1, 2): '))
            '''add error handling'''
#            field_list = field_by_age.split(', ')
#            for i in field_list:
            if field_by_age not in field_temp:
                print('Invalid selection!')
                continue
            print('You have assigned field', field_select[field_by_age - 1][1])
            print("")
            break
    # ----calculate available hours for games for checking max teams
        game_hours = avail_time(start_time, last_time, game_time_length)
#        num_fields_for_age = 1 #len(field_list)
    # ----calculates max number of teams for the age group by dividing avail game time
    #     by game time length * number of days * number of fields * 2 (2 teams per game)
        max_teams = int(game_hours / game_time_length * tourn_days / min_games * 2)
        print('Max number of teams for the {} age group: '.format(age), max_teams)
        open_slots = max_teams
        db = sqlite3.connect('data/master')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO age(age, start, last, time, games, max, open, \
                                          field_id, tourn_id)
                        VALUES(?,?,?,?,?,?,?, ?,?)''',
                        (age, start_time, last_time, game_time_length, min_games,
                         max_teams, open_slots, field_by_age, tourn_id))
        db.commit()
        """
        add exception error here
        """
        db.close()

#create_tournament()
























#        another_field = input("Would you like to enter another field? \
#                              press 'y' for yes and any other key for no. ")
#        if another_field == 'Y' or another_field == 'y':
#            print('You have entered the following fields so far: ', avail_fields)
#            continue
#        else:
#            break
#        break

#        while True:
#            num_games = int(input('Enter number of games per day for field: '))
#            if num_games == 0:
#                print('Number of games cannot be 0!')
#                '''add error handling for non-integers'''
#                continue
#            else:
#                break

#def is_valid_date(date):
#    """ evaluates if input date is valid, returns boolean"""
#    if '-' not in date:
#        return False
#    if len(date) != 10:
#        return False
#    month, day, year = date.split('-')
#    is_valid = True
#    try:
#        datetime(int(year), int(month), int(day))
#    except ValueError:
#        is_valid = False
#    
#    if is_valid:
#        return True
#    else:
#        return False
    
#def is_future_date(date):
#    """ confirms date is in future, assumes date is valid, returns boolean"""
#    present = datetime.now()
##    month, day, year = date.split('-')
##    if present < datetime(int(year), int(month), int(day)):
#    if present < date:
#        return True
#    else:
#        return False
    
#def end_date_after(start, end):
#    """confirms end_date occurs after start_date, assumes both dates are valid
#    returns a boolean
#    """
##    month, day, year = start.split('-')
##    month1, day1, year1 = end.split('-')
##    if datetime(int(year), int(month), int(day)) < datetime(int(year1),
##                int(month1), int(day1)):
#    if end_date > start_date:
#        return True
#    else:
#        return False

#def num_tournament_days(start, end):
#    """
#    uses tournament start/end dates to calculate number
#    of days in tournament. assumes dates have been validated.
#        end date - start date
#        returns an integer
#    """
#    month, day, year = start.split('-')
#    month1, day1, year1 = end.split('-')
#    num_days = (datetime(int(year1), int(month1), int(day1)) - datetime(int(year),
#                        int(month), int(day))).days
#    return num_days + 1