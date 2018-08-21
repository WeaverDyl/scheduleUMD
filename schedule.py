from urllib.request import Request, urlopen
import json
import sys
import getopt
from time import sleep
from datetime import date, datetime

def main():
    try:
        args = semester, course, section = get_args() # Grab command-line args    
        (result, message) = validate_args(args)
        if result:
            formatted_semester = format_semester(semester)
            check_class(course, section, formatted_semester)
            return
        else:
            raise ValueError(message)
    except (ValueError, getopt.GetoptError) as e: # specify
        print(f"Error: {e}")
        usage()
        return None

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
            site = "".join(site.split())

        try:
            # TODO: use umd.io when it's not broken

            # Find section within HTML
            find_section = site.find(section_code)

            # Get seat count for specified section
            find_seats = find_section + site[find_section:].find(seats_code)
            find_seats += len(seats_code)
            open_seats = int(site[find_seats])
            
            # If there's a seat, alert user and return
            if open_seats:
                print("Open Seat Exists! You can get in!")
                return
            
            # Else, sleep for 5 minutes and try again.
            print(f"No seats at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Checking in 5 minutes...")
            sleep(300)
        except Exception as e: # Gather possibilities
            # Can happen if section doesn't exist
            print("Unexpected error occurred. Exiting...")
            print(e)
            return

def format_semester(semester):
    # Returns the semester in the format that the schedule of classes expects:
    # semesterYY
    semester = semester.lower()
    year = date.today().strftime("%y")
    # Returns the current semester based on the current date
    if semester in ("fall", "winter", "spring", "summer"):
        if semester == "fall":
            return "08" + year
        elif semester == "winter":
            return "12" + year
        elif semester == "spring":
            return "01" + year
        else:
            return "05" + year
    else:
        raise ValueError("You've entered an invalid semester!")

def validate_args(args):
    # Checks to see if the required arguments were received
    term, course, section = args

    # Must specify a specific semester (fall, spring, winter, summer)
    if not term:
        return (False, "You must specify a semester")
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
            term = arg
        elif opt in ("-c", "--course"):
            course = arg
        elif opt in ("-s", "--section"):
            section = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        else:
            raise ValueError("You've entered an invalid argument.")
    return (term, course, section)

def usage():
    # Print the directions to use the program
    print(f"\nusage: {sys.argv[0]} -t TERM -c COURSE -s SECTION")
    print("Further Explanation:\n-t / --term\t: refers to the current semester. Valid input is:\n\t\t  Fall | Spring | Winter | Summer")
    print("-c / --course\t: refers to the course department and number. An example is 'ENGL101'.\n\t\t  Courses are 4 letters followed by 3 numbers.")
    print("-s / --section\t: refers to the section of the course. Sections are four digits, such as '0101'.")

if __name__ == "__main__":
    main()