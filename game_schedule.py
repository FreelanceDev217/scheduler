# -*- coding: utf-8 -*-
"""
GS++ :: Tournament game scheduling app

schedule app adds team information through registration form to database
tables set up in database for tournament, teams, schedule and standings
at admin scheduled time, scheduler executes to schedule tournament

supporting files:
    tournament.py
    registration.py
    schedule.py
    createDB.py
    data/master (sqlite3)

Created on Wed Jun 27 09:15:46 2018

@author: Scott Sandman
"""

import sqlite3
import time
from datetime import datetime
from schedule import generate_schedule 

"""
automatically schedule tournament at an administrator
specified time prior to start of tournament (ex. 3 days)
"""
set_time = datetime(2018, 8, 13, hour = 12, minute = 30)
while datetime.now() < set_time:
    time.sleep(1)

tourn_id = 1
generate_schedule(tourn_id)

def enter_game_scores():
    """
    function that allows administrator to input game scores
    updates standings
    """
    pass

def standings():
    """
    create database for standings
        define sort criteria (ex. wins/runs allowed/run differential)
    """
    pass


