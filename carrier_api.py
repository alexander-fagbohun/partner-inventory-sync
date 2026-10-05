from fastapi import FastAPI, HTTPException

app = FastAPI(title="Fake Carrier API")

TRIPS = [
    {"trip_id": "T001", "origin": "Berlin", "destination": "Hamburg",
     "departure": "2026-10-10T08:00", "arrival": "2026-10-10T11:15", "price_eur": 19.99},
    {"trip_id": "T002", "origin": "Berlin", "destination": "Leipzig",
     "departure": "2026-10-10T09:30", "arrival": "2026-10-10T11:00", "price_eur": 12.50},
    {"trip_id": "T003", "origin": "Hamburg", "destination": "Bremen",
     "departure": "2026-10-10T14:00", "arrival": "2026-10-10T15:20", "price_eur": 9.99},
    # --- messy data, like a real carrier might send ---
    {"trip_id": "T004", "origin": "Berlin", "destination": "Dresden",
     "departure": "2026-10-10T16:00", "arrival": "2026-10-10T13:00", "price_eur": 14.99},
    {"trip_id": "T005", "origin": "Munich", "destination": "Nuremberg",
     "departure": "2026-10-10T10:00", "arrival": "2026-10-10T11:45", "price_eur": -5.00},
    {"trip_id": "T006", "origin": "Cologne", "destination": "",
     "departure": "2026-10-10T12:00", "arrival": "2026-10-10T13:00", "price_eur": 8.99},
    {"trip_id": "T003", "origin": "Hamburg", "destination": "Kiel",
     "departure": "2026-10-10T18:00", "arrival": "2026-10-10T19:30", "price_eur": 11.99},
]


@app.get("/trips")
def get_trips():
    return TRIPS


# {trip_id} is a "path parameter": whatever is in the URL at that spot
# gets passed into the function as the trip_id variable.
@app.get("/trips/{trip_id}")
def get_trip(trip_id: str):
    # Go through every trip until we find the matching ID.
    for trip in TRIPS:
        if trip["trip_id"] == trip_id:
            return trip
    # If the loop finishes without finding it, send a 404 "not found" error.
    raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")