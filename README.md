# GS++

Written in Python 3.6 using SQLite3 as database (anticipate updating to MySQL as project progresses)

Tournament game scheduling app. When created, the tournament is scheduled (currently set at 7 days) to generate the schedule automatically based on the registered teams in the database.

Tournament creator provides input to set up tournament (Title, Dates, Age Groups, Fields, Start times, Minimum games played).

Teams provide input (Name, age group, location, contact information).

All data is stored in tables in master database.

Creator inputs are used to calculate maximum number of games that can be played and maximum number of teams. Available team
slots are reduced by one each time a team registers. If all team slots are filled for an age group, no other teams may register.

Team location is used to "weight" the distance a team travels to the tournament. Current center point location is Charleston, SC. Higher weighted teams are scheduled to play the later games on day one of the tournament due to their travel requirements.

Currently, the scheduling portion of the app only handles a few options for number of teams and type of tournament.

Potential additions to the app:

Waiting list for teams after all slots are full
Different types of tournaments other than pool play
