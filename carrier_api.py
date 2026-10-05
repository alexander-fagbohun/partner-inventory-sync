from fastapi import FastAPI

# Create the API app. The title shows up in the auto-generated docs page.
app = FastAPI(title="Fake Carrier API")

# Our pretend bus company's inventory: a list of trips.
# Each trip is a dictionary (key: value pairs).
TRIPS = [
    {"trip_id": "T001", "origin": "Berlin", "destination": "Hamburg",
     "departure": "2026-10-10T08:00", "arrival": "2026-10-10T11:15", "price_eur": 19.99},
    {"trip_id": "T002", "origin": "Berlin", "destination": "Leipzig",
     "departure": "2026-10-10T09:30", "arrival": "2026-10-10T11:00", "price_eur": 12.50},
    {"trip_id": "T003", "origin": "Hamburg", "destination": "Bremen",
     "departure": "2026-10-10T14:00", "arrival": "2026-10-10T15:20", "price_eur": 9.99},
]

# When someone visits /trips, run this function and send back the list.
@app.get("/trips")
def get_trips():
    return TRIPS