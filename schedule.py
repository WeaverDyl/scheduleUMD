import json, sys, getopt, argparse, urllib.request
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
        check_class(args.course, args.section)
        return
    except Exception as e: # specify
        print(f"Error: {e}")
        return None

def send_message(message):
    # Sends the user a specified message
    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_num, to=your_number)

def check_class(course, section):
    base_url = "https://bapi.umd.io/v0/courses/sections/"
    url = base_url + course + "-" + section
    try:
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            # Ensures course/section exists
            if data:
                while True:
                    # If there's a seat, alert user and return
                    if int(data["open_seats"]) > 0:
                        print(f"Open seat found for section {section} of {course}! Sending message...")
                        send_message(f"Open seat found for section {section} of {course}!")
                        return
                    else:
                        # Else, sleep for 5 minutes and try again.
                        print(f"No seats at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Checking in 5 minutes...")
                        sleep(300)
    except urllib.error.HTTPError as e:
        print("Error: Invalid course or section")
        return
    except Exception as e: # Gather possibilities
        print(f"Error (unexpected): {e}. Exiting...")
        return

def get_args():
    # Sets up the command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("course", help="Stores course (ENGL101/CMSC131/etc...)")
    parser.add_argument("section", help="Stores section (0101/0102/etc...)")
    return parser.parse_args()

if __name__ == "__main__":
    main()