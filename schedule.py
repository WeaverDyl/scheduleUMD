import urllib.request, json

if __name__ == "__main__":
    course = input("What class are you trying to get in to? ")
    section = input(f"What section of {course} are you trying to get in to? ")
    base_url = "https://api.umd.io/v0/courses/sections/%s-%s" % (course,section)

    try:
        with urllib.request.urlopen(base_url) as url:
            data = json.loads(url.read().decode())
            try:
                print(data["open_seats"])
            except KeyError:
                print("no open_seats param???")
    except urllib.error.HTTPError as e:
        if e.getcode() == 400:
            print("bad course/section combo")
        if e.getcode() == 404:
            print("dev error - wrong params")