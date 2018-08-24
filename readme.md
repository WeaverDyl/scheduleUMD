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

You must provide two command line arguments:

1. The first argument you must provide is the department / course ID combo of the course you want to find a seat for.
	1. The proper format for this argument is simply the course name, for example, `ENGL101`.

2. the second argument is the 4 digit section number of the course.
	1. An example for this argument is `0101`.

There is also a 'help' argument to explain all of this.

1. `python schedule.py -h` or `python schedule.py --help` will explain how to use this program.

So, if you wanted to find a seat for section 0101 of ENGL101, you would run the program as: 

`python schedule.py engl101 0101`

## LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.