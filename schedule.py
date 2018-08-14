# -*- coding: utf-8 -*-
"""
GS++ :: Tournament game scheduling app

support file for game_schedule.py, schedules tournament
based on data from TOURNAMENT database

Created on Wed Jun 27 09:15:46 2018

@author: Scott Sandman
"""

import sqlite3
from datetime import datetime, timedelta

def get_age_groups(tourn_id):
    """uses tournament id to select tournament age groups.
    returns a list.
    """
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    #get available age groups for tournament
    groups = cursor.execute('''SELECT age FROM age WHERE tourn_id=?''',
                                [tourn_id])
    temp_groups = groups.fetchall()
    db.close()
    #convert temp_groups from tuple in a list to a list
    age_groups = []
    for age in range(len(temp_groups)):
        age_groups.append(temp_groups[age][0])
    return age_groups

#print(get_age_groups(1))
    

def get_teams_by_age(tourn_id, age):
    """uses tournament id to select all teams registered for tournament and
    sorts teams into age groups.
    returns a dictionary with age group as key and values are tuples with team
    name, location, reg date and requests.
    """
    
    '''requests need to be added in registration.'''
    
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    select = cursor.execute('''SELECT team FROM teams WHERE tourn_id=? and age=? \
                            ORDER BY weight, registration''',
                            (tourn_id, age))
    temp_teams = select.fetchall()
    db.close()
    teams = []
    for t in range(len(temp_teams)):
        teams.append(temp_teams[t][0])
    return teams

#print(get_teams_by_age(1, '16u'))
    
def games_required(tourn_id, age):
    """
    function to calculate the number of games required for an age group in the
    tournament
        min games per team * number of teams
    """
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    g = cursor.execute('''SELECT games FROM age WHERE id=?''',
                            [tourn_id])
    games = g.fetchall()
    db.close()
    min_games = games[0][0]
    num_teams = len(get_teams_by_age(tourn_id, age))
    total = int(min_games * num_teams / 2)
    return total, min_games

#print(games_required(1, '16u'))
    
def get_team_requests(team):
    """
    retrieves team requests from team table in master database
    weights requests based on team distance and registration time
    returns __________
    """
    pass

def generate_game_times(tourn_id, age):
    """
    generates game times by for field by age group
    returns dictionary
    """
    db = sqlite3.connect('data/master')
    cursor = db.cursor()
    get_num_days = cursor.execute('''SELECT days FROM tournaments WHERE id=?''',
                                  [tourn_id])
    num_days = get_num_days.fetchone()
    num_days = num_days[0]
    get_age_data = cursor.execute('''SELECT start, time, field_id FROM age WHERE tourn_id=? and
                              age=?''', (tourn_id, age))
    age_info = get_age_data.fetchall()
    start_time = age_info[0][0]
    game_time_length = age_info[0][1]
    field_id = age_info[0][2]
    get_fields = cursor.execute('''SELECT field FROM fields WHERE tourn_id=? and
                                id=?''', (tourn_id, field_id))
    fields = get_fields.fetchall()
    field = fields[0][0]
    db.close()
    req, min_games = games_required(tourn_id, age)
#
    games_day = int(req / num_days)
    
    fields_with_times = dict()
    for d in range(num_days):
        game_times = []
        time = datetime.strptime(start_time, '%I:%M %p')
        for g in range(games_day):
            game_times.append(time)
            time = time + timedelta(hours = game_time_length)
        #convert time(floats) to strings
        for h in range(len(game_times)):
            hours = game_times[h].hour
            minutes = game_times[h].minute
            if hours > 12:
                hours -= 12
            hours = str(hours)
            if minutes == 0:
                minutes = ':00'
            else:
                minutes = ':' + str(minutes)
            game_times[h] = hours + minutes
        fields_with_times[d + 1] = game_times
    return field, fields_with_times
   
#print(generate_game_times(1, '16u'))

def generate_games(tourn_id, age):
    """
    create schedules for each age group based on the following criteria:
        1. (not implemented)-----if payment not made, do not schedule team
        2. team location (how far they have to travel)
        3. date team registered
        4. (not implemented)-----team requests (if any) and (if possible)
    """
    teams = get_teams_by_age(tourn_id, age)
#    teams = [1, 2, 3, 4, 5, 6, 7, 8, 9 , 10]
    req, min_games = games_required(tourn_id, age)
    games = []
    div = int(len(teams) / 2)
    pool1 = teams[:div]
    pool2 = teams[div:]
    h_or_a = 2 #home or away
    for m in range(min_games):
        for i in range(len(pool1)):
            if h_or_a % 2 == 0:
                games.append([pool1[i], pool2[i]])
                h_or_a += 1
            else:
                games.append([pool2[i], pool1[i]])
                h_or_a += 1
        temp = pool1[0]
        pool1.remove(temp)
        pool1.append(temp)        
#        req = 25
#        min_games = 5
    need_games = []
    if len(games) < req:            
        for t in teams:
            count = 0
            for g in games:
                if t in g:
                    count += 1
            if count < min_games:
                need_games.append(t)
    if len(need_games) > 0:
        n = 0
        while n < len(need_games) - 1:
            games.append([need_games[n], need_games[n + 1]])
            n += 2
    return games
        
#print(generate_games(1, '16u'))

def generate_schedule(tourn_id):
    """
    matches games with game times. stores in schedule table in master database.
    adds game numbers, field names, date and day of week.
    """
    age_groups = get_age_groups(tourn_id)
#    age_groups = ["16u"]        
    game_number = 1
    for age in age_groups:
        field, game_times = generate_game_times(tourn_id, age)
        games = generate_games(tourn_id, age)
        for day in game_times:
            for time in range(len(game_times.get(day))):
                print(day, game_number, game_times[day][time], games[game_number - 1], field)
                game_number += 1
       
            
#schedule(1)
            
        


















#    if validate_number_games(tourn_id) is False:
#        print('There are not enough available game slots to schedule.')
#        print('Games required: ', games_required(tourn_id))
#        print('Available game slots: ', game_slots_available(tourn_id))
#    else:
#        print('There are enough game time slots. Proceeding...')

#def validate_number_games(tourn_id):
#    """
#    function to compare total required games to available games
#    """
#    if games_required(tourn_id) <= game_slots_available(tourn_id):
#        return True
#    else:
#        return False
#validate_number_games(1)

#def game_slots_available(tourn_id):
#    """
#    function to calculate number of game slots available
#        number of fields * number of game slots per day * number of days
#    """
#    db = sqlite3.connect('data/master')
#    cursor = db.cursor()
#    select = cursor.execute('SELECT name, games FROM fields WHERE \
#                            tourn_id=?', [tourn_id])
#    fields = select.fetchall()
#    db.close()
#    total_games = 0
#    for i in range(len(fields)):
#        total_games += fields[i][1]
#    return total_games * num_tournament_days(tourn_id)
#
#print('Game slots available: ', game_slots_available(1))

"""
stopping point 07/30/18
need to take a harder look at how to calculate games per day.
should it calculate number of games for each day????? or just that day????
if just that day, you will need a total games required variable and reduce
by the day
"""
#def field_games_per_day(tourn_id, age):
#    """
#    calculates number of games required for a field on a given day.
#    retrieves max teams and open slots from age table in master database
#        number of games = (max - open) / 2 
#    """
#    db = sqlite3.connect('data/master')
#    cursor = db.cursor()
#    m_o = cursor.execute('''SELECT max, open FROM age WHERE tourn_id=? and
#                              age=?''', (tourn_id, age))
#    max_open = m_o.fetchall()
#    db.close()
#    max_teams = max_open[0][0]
#    open_slots = max_open[0][1]
#    return max_teams - open_slots

#print(field_games_per_day(1, '16u'))