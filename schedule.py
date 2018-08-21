import urllib.request
import json
import sys
import getopt

def main():
    try:
        args = course, section, begin, end, days = get_args() # Grab command-line args    

        try:
            validate_args(args)
            # find_class(args)
        except Exception as e:
            print("Exception from validate")
            print(e)

    except Exception as e: # specify
        print(f"ERROR: {e}")
        return None

def validate_args(args):
    course, section, begin, end, days = args

    # Must specify a course
    if not course:
        raise Exception("You must specify a course")
    # Must have a start and end time if any time is specified
    if begin and not end or end and not begin:
        # find better exception / make own exception
        raise Exception("You must either set a beginning and end time or no time at all.")
        #                       ^^^^^^^^^^^^^^^^^ REPHRASE THIS ^^^^^^^^^^^^^^^^^

def get_args():
    try:
        course, section, begin, end, days = None, None, None, None, None
        #course_set, section_set, begin_set, end_set, days_set = False, False, False, False, False
        opts, _ = getopt.getopt(sys.argv[1:], "c:s:b:e:d", ["course", "section", "begin", "end", "days"])                           

        # Set boolean flags for each short/longopt
        for opt, arg in opts:
            if opt in ("-c", "--course"):
                course = arg
            elif opt in ("-s", "--section"):
                section = arg
            elif opt in ("-b", "--begin"):
                begin = arg
            elif opt in ("-e", "--end"):
                end = arg
            elif opt in ("-d", "--days"):
                days = arg

        return(course, section, begin, end, days)
    except getopt.GetoptError as e:
        print(f"GETOPT ERROR: {e}")
        sys.exit(-1) # right thing to do, or is there a better way?
    except Exception as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()