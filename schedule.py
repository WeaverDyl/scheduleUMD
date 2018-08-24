import json, sys, getopt, argparse
from urllib.request import Request, urlopen
from time import sleep
from datetime import date, datetime, timedelta
from twilio.rest import Client

try:
    from auth import account_sid, auth_token, twilio_num, your_number
except ImportError:
    raise IOError("Create a `auth.py` file with fields according to the README instructions.")

def main():
    try:
        args = get_args() # Grab command-line args
        formatted_semester = format_semester(args.term, args.year)
        check_class(args.course, args.section, formatted_semester)
        return
    except Exception as e: # specify
        print(f"Error: {e}")
        return None

def send_message(message):
    # Sends the user a specified message
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_num, to=your_number)

def check_class(course, section, formatted_semester):
    # Checks the number of seats in a section and sends the user a text message
    # when a seat is available.
    section_code = '<spanclass="section-id">' + section
    seats_code = '<spanclass="open-seats-count">'
    base_url = f"https://app.testudo.umd.edu/soc/search?courseId={course}&sectionId={section}&termId=201808&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
    request = Request(base_url, headers={'User-Agent': 'scheduleUMD'})

    while True:
        # Get site HTML
        with urlopen(request) as resp:
            site = resp.read()
            encode = resp.headers.get_content_charset('utf-8')
            site = site.decode(encode)
            site = "".join(site.split()) # Remove any whitespace

        try:
            # TODO: use umd.io when it's not broken

            # Check for misformed course ID / section number
            if "No courses matched your search filters above.".replace(" ", "") in site:
                raise ValueError("Invalid course or section")

            # Find section within HTML
            find_section = site.find(section_code)

            # Get seat count for specified section
            find_seats = find_section + site[find_section:].find(seats_code)
            find_seats += len(seats_code)
            open_seats = int(site[find_seats])
            
            # If there's a seat, alert user and return
            if open_seats:
                print(f"Open seat found for section {section} of {course}! Sending message...")
                send_message(f"Open seat found for section {section} of {course}!")
                return
            
            # Else, sleep for 5 minutes and try again.
            print(f"No seats at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Checking in 5 minutes...")
            sleep(300)
        except ValueError as e:
            # Except in main()
            raise
        except Exception as e: # Gather possibilities
            print("Unexpected error occurred. Exiting...")
            print(e)
            return

def format_semester(semester, year):
    # Returns the semester in the format that the schedule of classes expects:
    # semesterYY
    semester = semester.lower()
    old_year = year
    year = year[len(year) - 2:] # Convert year to 2-digit form (2011 -> 11)
    # Returns the current semester based on the current date
    if semester in ("fall", "winter", "spring", "summer"):
        if semester == "fall":
            month = "08"
        elif semester == "winter":
            month = "12"
            year = str(int(year) - 1) # Recalculate year (winter 2018 = 201712)
        elif semester == "spring":
            month = "01"
        else:
            month = "05" # Summer
    else:
        raise ValueError(f"{semester} is an invalid semester")

    # Check that the semester hasn't already happened
    if validate_semester(month, year):
        return month + year[len(year) - 2:]
    else:
        raise ValueError(f"{semester} {old_year} is too far from the current date.")

def validate_semester(month, year):
    # Checks if the date provided is close to the dates given by the schedule
    # of classes formatted month/year (1217, 0518, 0818, 0119)

    # This is a pretty good way to ensure that no previous semesters are accidentally
    # used.

    # TODO: reconsider for some circumstances: summer I / summer II / winter length
    try:
        date_given = datetime.strptime(month + year, '%m%y')
        date_buffer_greater = date_given + timedelta(days=45)
        date_buffer_less = datetime.now() + timedelta(days=45)

        # Check that we're within 45 days of the semester the user gave
        # The 45 is arbitrary, but should work well enough for general use
        if datetime.now() > date_buffer_greater or date_given > date_buffer_less:
            return False
        return True
    except Exception:
        raise

def get_args():
    # Sets up the command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="The current semester (Fall/Spring/Winter/Summer)")
    parser.add_argument("year", help="The current year (2018/2019/etc...)")
    parser.add_argument("course", help="Stores course (ENGL101/CMSC131/etc...)")
    parser.add_argument("section", help="Stores section (0101/0102/etc...)")
    return parser.parse_args()

if __name__ == "__main__":
    main()