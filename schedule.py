import urllib.request
import json
import sys
import getopt
import datetime

def main():
    try:
        args = semester, course, section, begin, end, days = get_args() # Grab command-line args    

        (result, message) = validate_args(args)
        if result:
            print("all good so far")
            find_class(args)
            pass # THEN??
            # ^ class = find_class(args) --- might be a list??? multiple sections may appear
            # give user numbered list, ask them to choose their ideal section if applicable
            # ask user for email/phone#
        else:
            print(f"Error: {message}") # from validate_args()

    except Exception as e: # specify
        print(f"ERROR: {e}") # from getargs??
        return None

def find_class(args):
    semester, course, section, begin, end, days = args
    pass

def format_semester():
    # Returns the current semester based on the current date
    
    pass

def validate_args(args):
    # Checks to see if the required arguments were received
    term, course, section, begin, end, days = args

    # Must specify a specific semester (fall, spring, winter, summer)
    if not term:
        return (False, "You must specify a semester.")
    # Must specify a course
    if not course:
        return (False, "You must specify a course.")
    # Must specify a section
    if not section:
        return (False, "You must specify a section.")
    # Must have a start and end time if any time is specified
    if begin and not end or end and not begin:
        # find better exception / make own exception
        return (False, "You must either set a beginning and end time or no time at all.")
        #                       ^^^^^^^^^^^^^^^^^ REPHRASE THIS ^^^^^^^^^^^^^^^^^
    return (True, "Successful!")

def get_args():
    try:
        term, course, section, begin, end, days = None, None, None, None, None, None
        #course_set, section_set, begin_set, end_set, days_set = False, False, False, False, False
        opts, _ = getopt.getopt(sys.argv[1:], "t:c:s:b:e:d:h", ["term=", "course=", "section=", "begin=", "end=", "days=", "help"])                           

        # Set boolean flags for each short/longopt
        for opt, arg in opts:
            if opt in ("-t", "--term"):
                term = arg
            elif opt in ("-c", "--course"):
                course = arg
            elif opt in ("-s", "--section"):
                section = arg
            elif opt in ("-b", "--begin"):
                begin = arg
            elif opt in ("-e", "--end"):
                end = arg
            elif opt in ("-d", "--days"):
                days = arg
            elif opt in ("-h", "--help"):
                # Give user list of commands
                pass
            else:
                pass
                # user gave unspecified arg
        return (term, course, section, begin, end, days)
    except getopt.GetoptError as e:
        print(f"GETOPT ERROR: {e}")
        sys.exit(-1) # right thing to do, or is there a better way?
    except Exception as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()