import requests
from gtfs_realtime_pb2 import FeedMessage
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate  # For tabular display
import time

# BKK API Key and URL for GTFS-RT feed
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
URL = f"https://go.bkk.hu/api/query/v1/ws/gtfs-rt/full/TripUpdates.pb?key={API_KEY}"

# Static GTFS Files
ROUTES_FILE = "routes.txt"  # Path to routes.txt
STOPS_FILE = "stops.txt"    # Path to stops.txt
TRIPS_FILE = "trips.txt"    # Path to trips.txt

# Time window for arrivals (in minutes)
TIME_WINDOW_MINUTES = 10


def load_gtfs_static_files(routes_file, stops_file, trips_file):
    """Load routes, stops, and trips from static GTFS files."""
    # Load routes.txt to map route_id -> route_short_name (vehicle number)
    routes_df = pd.read_csv(routes_file)
    routes_mapping = routes_df.set_index("route_id")["route_short_name"].to_dict()

    # Load stops.txt to map stop names and stop IDs
    stops_df = pd.read_csv(stops_file)
    stops_mapping = stops_df.set_index("stop_id").to_dict(orient="index")

    # Load trips.txt to map trip_id -> direction_id and trip_headsign
    trips_df = pd.read_csv(trips_file)
    trips_mapping = trips_df.set_index("trip_id")[["direction_id", "trip_headsign"]].to_dict(orient="index")

    return routes_mapping, stops_mapping, trips_mapping


def fetch_gtfs_rt_feed(url):
    """Fetch and parse the GTFS-RT feed."""
    response = requests.get(url)
    feed = FeedMessage()
    feed.ParseFromString(response.content)
    return feed


def find_stops_by_name(stops_mapping, stop_name_query):
    """Find stops matching a given name query."""
    selected_stops = {stop_id: details for stop_id, details in stops_mapping.items()
                      if stop_name_query.lower() in details["stop_name"].lower()}
    return selected_stops


def get_incoming_trams(feed, routes_mapping, selected_stops, trips_mapping, current_time):
    """Get a list of trams arriving at selected stops within the time window."""
    incoming_trams = []
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            trip_update = entity.trip_update
            for stop_time in trip_update.stop_time_update:
                stop_id = stop_time.stop_id
                # Only process relevant stops
                if stop_id in selected_stops and stop_time.arrival.HasField("time"):
                    arrival_time = datetime.fromtimestamp(stop_time.arrival.time)
                    time_to_arrival = arrival_time - current_time
                    # Only include vehicles in the defined time window
                    if timedelta(seconds=0) <= time_to_arrival <= timedelta(minutes=TIME_WINDOW_MINUTES):
                        route_id = trip_update.trip.route_id if trip_update.trip.route_id else "Unknown Route"
                        vehicle_number = routes_mapping.get(route_id, "Unknown")  # Get vehicle number

                        # Get trip_id to derive direction and destination
                        trip_id = trip_update.trip.trip_id
                        trip_info = trips_mapping.get(trip_id, {"direction_id": -1, "trip_headsign": "Unknown"})
                        destination = trip_info["trip_headsign"]  # Final stop/destination
                        
                        # Append details of this tram to the list
                        headsign = selected_stops[stop_id]["stop_name"]
                        incoming_trams.append({
                            "vehicle_number": vehicle_number,  # Vehicle number
                            "route_id": route_id,  # Internal route ID
                            "stop_name": headsign,  # Stop name
                            "arrival_time": arrival_time.strftime("%H:%M:%S"),  # Predicted time
                            "time_to_arrival": str(time_to_arrival).split(".")[0],  # Time to arrival
                            "destination": destination  # Final destination
                        })
    return incoming_trams


def display_real_time_board(trams):
    """Display the real-time timetable in tabular format."""
    if not trams:
        print("No vehicles arriving within the next 10 minutes.")
        return

    # Sort trams by time-to-arrival
    sorted_trams = sorted(trams, key=lambda x: x["time_to_arrival"])

    # Create a unified table with both directions combined
    table = [[
        tram["vehicle_number"],
        tram["destination"],
        tram["stop_name"],
        tram["arrival_time"],
        tram["time_to_arrival"]
    ] for tram in sorted_trams]

    # Define headers for the table
    headers = ["Vehicle Number", "Destination", "Stop Name", "Arrival Time", "Time to Arrival"]

    # Print the table
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def main():
    """Main function to allow real-time monitoring of custom stops."""
    print("Loading BKK GTFS static data...\n")
    routes_mapping, stops_mapping, trips_mapping = load_gtfs_static_files(ROUTES_FILE, STOPS_FILE, TRIPS_FILE)

    # Ask user for stop search query
    stop_name_query = input("Enter a stop name to search : ").strip()
    selected_stops = find_stops_by_name(stops_mapping, stop_name_query)

    # If no stops are found
    if not selected_stops:
        print(f"No stops found matching '{stop_name_query}'. Please try again.")
        return

    # Display selected stops
    print(f"\nFound {len(selected_stops)} stop(s) for '{stop_name_query}':")
    for stop_id, details in selected_stops.items():
        print(f"- Stop ID: {stop_id}, Stop Name: {details['stop_name']}")

    # Start the real-time monitoring
    while True:
        # Get the current time
        current_time = datetime.now()

        # Fetch GTFS-RT feed
        print("\nFetching real-time data...")
        feed = fetch_gtfs_rt_feed(URL)

        # Find incoming vehicles for the selected stops
        trams = get_incoming_trams(feed, routes_mapping, selected_stops, trips_mapping, current_time)

        # Clear the screen for a clean refresh
        print("\033[H\033[J")

        # Display the real-time timetable
        stop_names = ", ".join(details["stop_name"] for details in selected_stops.values())
        print(f"Real-Time Vehicle Timetable for Stops: {stop_names} (Next {TIME_WINDOW_MINUTES} Minutes):\n")
        if trams:
            display_real_time_board(trams)
        else:
            print("No vehicles arriving within the next 10 minutes.")

        # Wait before refreshing
        time.sleep(30)  # Refresh every 30 seconds


if __name__ == "__main__":
    main()
