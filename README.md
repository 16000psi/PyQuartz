# PyQuartz

### CLI timmer app written in python

This is a timer CLI program.  It is currently under development. 

To use the program in its current state, clone this repository and navigate to the project directory.  Commands are as follows (preceeded by "python main.py"):

#### list

Lists all timers and their time elpsed.  Passing arguments "day", "week", or "workingweek" will limit the results to timers that have been used within the last day, seven days, or days up to and including the most recent monday respectively.


#### start 

Starts a timer.  Pass a name, if the timer already exists it will start that timer again, if not a new one will be created.


#### stop

Stops all timers by default, if passed with a timer name only that timer will be stopped.


#### session_list 

Lists all sessions. Sessions are indivdual spans of time which belong to timers and are summed together to get the total time for a timer.  Each time a timer is started, a new session is created for that timer.

#### delete

Deletes the timer matching the passed name.


### Development objectives

The current plan is to use the program in its current state for tracking my work to see how it should be changed to make it better for practical use.  Current ideas:

- Archiving: If the timer app is used often, listing all will become useless as many old timers will be shown.  Archiving would allow timers to be kept whilst being not listed by default. With that in mind, automatically archiving timers based on certain conditions (e.g. not used for 30 days) could be a good feature.
- Day / Week summary:  It would be really useful to see a breakdown of sessions over the day for filling in timesheets. 
- Groups: It would be cool to create optional groupings so that individual tasks could be tracked as part of larger projects more easily (for instance "Ticket 3235" belongs to "Project X", and tracking time for the ticket automatically tracks time for the project).
