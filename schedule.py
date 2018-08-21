import urllib.request
import json
import sys
import getopt
from datetime import date

def main():
    try:
        args = semester, course, section = get_args() # Grab command-line args    
        (result, message) = validate_args(args)
        if result:
            formatted_semester = format_semester(semester)
            find_class(course, section, formatted_semester)
            pass # THEN??
            # ^ class = find_class(args) --- might be a list??? multiple sections may appear
            # give user numbered list, ask them to choose their ideal section if applicable
            # ask user for email/phone#
        else:
            raise ValueError(message)
    except Exception as e: # specify
        print(f"Error: {e}")
        return None

def find_class(course, section, formatted_semester):
    base_url = "https://app.testudo.umd.edu/soc/search?courseId={course}&sectionId={section}&termId=201808&_openSectionsOnly=on&creditCompare=&credits=&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"
    pass

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
        raise ValueError("You've entered an invalid semester! Run program with flag --help to see all options.")
    pass

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

        # Set boolean flags for each short/longopt
        for opt, arg in opts:
            if opt in ("-t", "--term"):
                term = arg
            elif opt in ("-c", "--course"):
                course = arg
            elif opt in ("-s", "--section"):
                section = arg
            elif opt in ("-h", "--help"):
                # Give user list of commands
                pass
            else:
                raise ValueError("You've entered an invalid argument. Run program with flag --help to see all options.")
        return (term, course, section)
    except getopt.GetoptError as e:
        raise ValueError(e) from None

if __name__ == "__main__":
    main()