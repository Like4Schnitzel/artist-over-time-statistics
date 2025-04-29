from auth import init_auth
from datetime import datetime
import time
import matplotlib.pyplot as plt
import requests
import argparse

def parse_date(date_str):
    """
    Parses a date string in the format YYYY-MM-DD and returns a UNIX timestamp.
    """
    try:
        return int(time.mktime(datetime.strptime(date_str, '%Y-%m-%d').timetuple()))
    except:
        raise ValueError(f"Invalid date format '{date_str}'. Please use 'YYYY-MM-DD'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="artist-over-time-statistics",
        description="Shows you how much you've listened to an artist over a period of time."
    )
    parser.add_argument(
        "artistname",
        type=str,
        help="The name of the artist you want to get statistics for."
    )
    parser.add_argument(
        "username",
        type=str,
        help="Username whose listens you want to fetch."
    )
    parser.add_argument(
        "-m", "--min",
        type=int,
        help="Minimum number of listens to display the date. Default: 1."
    )
    parser.add_argument(
        "-s", "--start",
        type=str,
        help="Inclusive start date in YYYY-MM-DD format. Default: 30 days before the end date."
    )
    parser.add_argument(
        "-e", "--end",
        type=str,
        help="Exclusive end date in YYYY-MM-DD format. Default: Current time."
    )

    args = parser.parse_args()

    api_key = init_auth()
    username = args.username
    get_tracks_url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={api_key}&limit=200&format=json'

    if args.end:
        end_time = parse_date(args.end)
    else:
        end_time = int(time.mktime(datetime.now().timetuple()))
    if args.start:
        start_time = parse_date(args.start)
    else:
        # If no start date is provided, set it to a month before the end date
        start_time = end_time - 60 * 60 * 24 * 30

    get_tracks_url += f'&from={start_time}&to={end_time}'

    page_number = 1
    statistics = {} # date as key, count of listens on that day as value
    tracks = []
    total_pages = "?"
    while True:
        print(f"Fetching page {page_number}/{total_pages}...\r", end="")
        response_json = requests.get(get_tracks_url + f'&page={page_number}').json()
        if 'error' in response_json:
            print(f"Error {response_json['error']}: {response_json['message']}")
            if args.username and response_json['error'] == 17:
                print(f"This is likely caused by {username} having their tracks set to private.")
            break

        total_pages = int(response_json['recenttracks']['@attr']['totalPages'])
        tracks = response_json['recenttracks']['track']

        for track in tracks:
            if track['artist']['#text'] != args.artistname:
                continue

            # Currently playing tracks don't have a date attribute.
            # We could add them to the current day instead of skipping but they appear on every page which would inflate the count.
            if '@attr' in track and 'nowplaying' in track['@attr']:
                continue

            date = datetime.fromtimestamp(int(track['date']['uts'])).strftime('%Y-%m-%d')

            if date not in statistics:
                statistics[date] = 0
            statistics[date] += 1

        page_number += 1
        if page_number > total_pages:
            break
    if args.min:
        for date in list(statistics.keys()):
            if statistics[date] < args.min:
                del statistics[date]
    if len(statistics.keys()) > 0:
        plt.bar(statistics.keys(), statistics.values())
        plt.title(f"{args.artistname} listens by {username}")
        plt.ylabel("Number of listens")
        plt.show()
    print("\nDone!")
