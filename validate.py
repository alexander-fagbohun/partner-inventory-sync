import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000/trips"


def fetch_trips():
    """Ask the carrier API for all trips and return them as a Python list."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()  # stop with an error if the API didn't answer 200
    return response.json()


def check_trip(trip):
    """Check ONE trip against our rules. Return a list of problems (empty = OK)."""
    problems = []

    if not trip.get("origin"):
        problems.append("missing origin")
    if not trip.get("destination"):
        problems.append("missing destination")

    price = trip.get("price_eur")
    if price is None or price <= 0:
        problems.append(f"invalid price: {price}")

    departure = datetime.fromisoformat(trip["departure"])
    arrival = datetime.fromisoformat(trip["arrival"])
    if arrival <= departure:
        problems.append("arrival is not after departure")

    return problems


def find_duplicate_ids(trips):
    """Compare trips AGAINST EACH OTHER to find IDs used more than once."""
    seen = set()
    duplicates = set()
    for trip in trips:
        trip_id = trip["trip_id"]
        if trip_id in seen:
            duplicates.add(trip_id)
        else:
            seen.add(trip_id)
    return duplicates


def main():
    trips = fetch_trips()
    duplicates = find_duplicate_ids(trips)

    valid = []
    rejected = []

    for trip in trips:
        problems = check_trip(trip)
        if trip["trip_id"] in duplicates:
            problems.append("duplicate trip_id")

        if problems:
            rejected.append((trip, problems))
        else:
            valid.append(trip)

    print(f"Checked {len(trips)} trips: {len(valid)} valid, {len(rejected)} rejected\n")
    for trip, problems in rejected:
        route = f"{trip.get('origin')} -> {trip.get('destination') or '???'}"
        print(f"REJECTED {trip['trip_id']} ({route}): {', '.join(problems)}")


if __name__ == "__main__":
    main()