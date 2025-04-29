import json
from auth import init_auth
from datetime import datetime
from urllib.parse import urlparse
import sys
import time
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
        "-s", "--start",
        type=str,
        help="Inclusive start date in YYYY-MM-DD format."
    )
    parser.add_argument(
        "-e", "--end",
        type=str,
        help="Exclusive end date in YYYY-MM-DD format."
    )

    args = parser.parse_args()

    api_key, secret, session_key, username = init_auth()
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
    tracks = []
    total_pages = "?"
    while True:
        print(f"Fetching page {page_number}/{total_pages}...\r", end="")
        response = requests.get(get_tracks_url + f'&page={page_number}')
        total_pages = int(response.json()['recenttracks']['@attr']['totalPages'])
        tracks = response.json()['recenttracks']['track']

        page_number += 1
        if page_number > total_pages:
            break
    print("Done!")
