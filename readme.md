# ScheduleUMD

A command-line tool to assist students at The University of Maryland who want to get into specific classes.

## What This Does

scheduleUMD is a simple tool to solve a big problem (for college students): getting a seat in the class you want. This program automates the process of checking the waitlists and will automatically send the user a text message when a seat in the class they want opens up.

## Usage
To begin, you must have the [Twilio Python Helper Library](https://www.twilio.com/docs/libraries/python) installed. This can be done using `pip install twilio`.

Once the Twilio library is installed, add a `auth.py` file to the same directory as the `schedule.py` program. fill the file in this format:
    
	account_sid = ""
    auth_token = ""
    twilio_num = "+1" # Enter your Twilio phone number
    your_number = "+1" # Enter your own phone number

Then, you can run the program using the standard `python schedule.py` command.

You must provide three command line arguments:

1. The first argument you must provide is the current semester. This is one of `{Fall, Spring, Winter, Summer}`
	1. The proper format for this argument is the current semester followed by the two-digit year corresponding to the semester. An example of this argument is: `fall18`.

2. The second argument you must provide is the department / course ID combo of the course you want to find a seat for.
	1. The proper format for this argument is simply the course name, for example, `ENGL101`.

3. Finally, the last argument is the 4 digit section number of the course.
	1. An example for this argument is `0101`.

There is also a 'help' argument to explain all of this.

1. `python schedule.py -h` or `python schedule.py --help` will explain how to use this program.

So, if you wanted to find a seat for the Fall 2018 offering of section 0101 of ENGL101, you would run the program as: 

`python schedule.py fall18 engl101 0101`

## Todo
Eventually I want to rewrite this using the [UMD.io](https://github.com/umdio/umdio) API. Currently (as of 8/22/18), it seems to be having accuracy issues regarding course data. This prompted me to write scheduleUMD without any API, so much of the processing code is not easily readable.

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.