import argparse
import csv
from datetime import datetime

import requests

API_URL = "http://127.0.0.1:8000/trips"


def fetch_trips_from_api():
    """Integration mode 1: pull trips from the carrier's API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def load_trips_from_csv(path):
    """Integration mode 2: read trips from a CSV file the carrier uploaded."""
    trips = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # each row becomes a dict, keyed by the header line
        for row in reader:
            trips.append(row)
    return trips


def parse_price(value):
    """Turn a price into a number. Return None if it isn't one."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def check_trip(trip):
    """Check ONE trip against our rules. Return a list of problems (empty = OK)."""
    problems = []

    if not trip.get("trip_id"):
        problems.append("missing trip_id")
    if not trip.get("origin"):
        problems.append("missing origin")
    if not trip.get("destination"):
        problems.append("missing destination")

    price = parse_price(trip.get("price_eur"))
    if price is None:
        problems.append(f"price is not a number: {trip.get('price_eur')!r}")
    elif price <= 0:
        problems.append(f"invalid price: {price}")

    try:
        departure = datetime.fromisoformat(trip["departure"])
        arrival = datetime.fromisoformat(trip["arrival"])
        if arrival <= departure:
            problems.append("arrival is not after departure")
    except (KeyError, TypeError, ValueError):
        problems.append("departure/arrival is not a valid date-time")

    return problems


def find_duplicate_ids(trips):
    """Compare trips AGAINST EACH OTHER to find IDs used more than once."""
    seen = set()
    duplicates = set()
    for trip in trips:
        trip_id = trip.get("trip_id")
        if not trip_id:
            continue  # missing IDs are already caught by check_trip
        if trip_id in seen:
            duplicates.add(trip_id)
        else:
            seen.add(trip_id)
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Validate carrier trip inventory.")
    parser.add_argument("--csv", help="Path to a carrier CSV file. Leave out to pull from the API.")
    args = parser.parse_args()

    if args.csv:
        trips = load_trips_from_csv(args.csv)
        source = args.csv
    else:
        trips = fetch_trips_from_api()
        source = API_URL

    duplicates = find_duplicate_ids(trips)
    valid = []
    rejected = []

    for trip in trips:
        problems = check_trip(trip)
        if trip.get("trip_id") in duplicates:
            problems.append("duplicate trip_id")

        if problems:
            rejected.append((trip, problems))
        else:
            valid.append(trip)

    print(f"Source: {source}")
    print(f"Checked {len(trips)} trips: {len(valid)} valid, {len(rejected)} rejected\n")
    for trip, problems in rejected:
        route = f"{trip.get('origin') or '???'} -> {trip.get('destination') or '???'}"
        print(f"REJECTED {trip.get('trip_id') or '???'} ({route}): {', '.join(problems)}")


if __name__ == "__main__":
    main()