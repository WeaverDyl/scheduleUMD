from urllib.request import Request, urlopen
import json
import sys
import getopt
from time import sleep
from datetime import date, datetime, timedelta
from twilio.rest import Client
from auth import account_sid, auth_token, twilio_num, your_number

def main():
    try:
        args = semester, year, course, section = get_args() # Grab command-line args    
        (result, message) = validate_args(args)
        if result:
            formatted_semester = format_semester(semester, year)
            check_class(course, section, formatted_semester)
            return
        else:
            raise ValueError(message)
    except Exception as e: # specify
        print(f"Error: {e}")
        usage()
        return None

def send_message(message):
    # Sends the user a specified message
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_num, to=your_number)

def check_class(course, section, formatted_semester):
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
    # Returns the current semester based on the current date
    if semester in ("fall", "winter", "spring", "summer"):
        if semester == "fall":
            month = "08"
        elif semester == "winter":
            month = "12"
            year = str(int(year) - 1)
        elif semester == "spring":
            month = "01"
        else:
            month = "05" # Summer
    else:
        raise ValueError("That semester is invalid")

    # Check that the semester hasn't already happened
    if validate_semester(month, year):
        return month + year
    else:
        raise ValueError("That semester is too far from the current date.")

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

def validate_args(args):
    # Checks to see if the required arguments were received
    term, year, course, section = args

    # Must specify a specific semester (fall, spring, winter, summer)
    if not term or not year:
        return (False, "You must specify a semester and year")
    # Must specify a course
    if not course:
        return (False, "You must specify a course")
    # Must specify a section
    if not section:
        return (False, "You must specify a section")
    return (True, "Successful!")

def get_args():
    try:
        term, course, section = None, None, None
        #course_set, section_set, begin_set, end_set, days_set = False, False, False, False, False
        opts, _ = getopt.getopt(sys.argv[1:], "t:c:s:h", ["term=", "course=", "section=", "help"])                           
    except getopt.GetoptError as e:
        raise ValueError(e) from None

    # Set boolean flags for each short/longopt
    for opt, arg in opts:
        if opt in ("-t", "--term"):
            term = arg[:len(arg) - 2]
            year = arg[len(arg) - 2:]
        elif opt in ("-c", "--course"):
            course = arg
        elif opt in ("-s", "--section"):
            section = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        else:
            raise ValueError("You've entered an invalid argument.")
    return (term, year, course, section)

def usage():
    # Print the directions to use the program
    print(f"\nusage: {sys.argv[0]} -t TERM -c COURSE -s SECTION")
    print("Further Explanation:\n-t / --term\t: refers to the current semester and year."\
          "Valid input is:\n\t\t  Fall## | Spring## | Winter## | Summer## (ex. fall18)")
    print("-c / --course\t: refers to the course department and number. An example is 'ENGL101'."\
          "\n\t\t  Courses are 4 letters followed by 3 numbers.")
    print("-s / --section\t: refers to the section of the course. Sections are four digits, such "\
          "as '0101'.")

if __name__ == "__main__":
    main()