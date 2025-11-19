
🚌 BKK Real-Time Tram Monitor
Stay on top of Budapest's tram schedule in real-time with this Python-based tool! This program fetches live data from the BKK GTFS-RT API to display a BKK-style timetable for any chosen stop. It shows the tram number, direction, arrival time, and time-to-arrival, updated every 30 seconds.

🚀 Features
Monitors in Real Time: Fetches live tram arrivals for stops in Budapest.
Customizable Stops: Easily search for specific stops to monitor (e.g., "Zsigmond tér").
Clear Timetable: Displays tram numbers, destinations, and accurate time-to-arrival details.
Fast and Refreshing: Updates every 30 seconds to display the latest tram info.

🧩 Prerequisites
Before using the tool, ensure you have the following:

Python 3.9+ installed.
You can download Python here: Python Downloads .
BKK GTFS-RT API Key:
You can request an API key via the BKK Developer Portal . This key will give you access to real-time tram arrival data.
GTFS Static Files (routes.txt, stops.txt):
Download the GTFS feed from BKK GTFS Feed to access static information about routes and stops.

 Project Structure
Here’s what the project directory looks like after setup:

      bkk-tram-monitor/
      ├── bkk_tram.py        # Main Python script
      ├── requirements.txt   # Python dependencies
      ├── README.md          # Documentation for the project
      ├── routes.txt         # GTFS routes file
      ├── stops.txt          # GTFS stops file

⚙️ Installation
Follow these steps to set up the tool:

Step 1: Clone the Repository
Clone this repository using Git:

    git clone https://github.com/yourusername/bkk-tram-monitor.git
    cd bkk-tram-monitor

Step 2: Set Up a Virtual Environment
It’s recommended to use a virtual environment to manage dependencies:

    python3 -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows

Step 3: Install Dependencies

    pip install -r requirements.txt


Step 4: Add Static GTFS Files

    Download the GTFS Static Feed from the official BKK GTFS feed .
    Extract the ZIP file and locate these two files:
    routes.txt
    stops.txt
    Copy these files into the project directory.

Step 5: Input Your BKK API Key

    Edit the bkk_tram.py file and replace the API_KEY placeholder with your actual key:
    API_KEY = "your_actual_API_key"



🏃 Usage
To start the real-time tram monitor, run the main Python script:

    python bkk_tram.py


You'll be prompted to input a stop name. For example:  Enter a stop name to search (e.g., Zsigmond tér): Zsigmond tér

    The program will search for all stops matching your input.
    If multiple matching stops (or directions) exist, it will monitor all of them.
    

⏳ Real-Time Timetable Output
Once running, the program will display a live timetable in your terminal:

    Real-Time Tram Timetable for Stops: Zsigmond tér (Next 5 Minutes):

    ╒═══════════════╤══════════════════════════════════════════╤═══════════════╤═════════════════╕
    │ Tram Number   │ Direction                                │ Arrival Time  │ Time to Arrival │
    ╞═══════════════╪══════════════════════════════════════════╪═══════════════╪═════════════════╡
    │ 41            │ Bécsi út / Vörösvári út                  │ 17:00:23      │ 00:01:32        │
    │ 17            │ Outbound (Savoya Park, etc.)             │ 17:03:33      │ 00:04:42        │
    ╘═══════════════╧══════════════════════════════════════════╧═══════════════╧═════════════════╛

    If no trams are scheduled to arrive:


    Real-Time Tram Timetable for Stops: Zsigmond tér (Next 5 Minutes):
    No trams arriving within the next 5 minutes.


🛠️ Configuration
Customizing Stops
    To monitor a specific stop (or set of stops):

    Enter the stop name when prompted (e.g., "Deák Ferenc tér").
    The program will search for matching stop names in the stops.txt file and confirm the selected stops.


 ⚡ Troubleshooting
 
    Issue: "No stops found matching your query"
    Ensure the correct spelling of the stop name.
    E.g., type Deák Ferenc tér instead of Deak.
    Make sure stops.txt is in the project directory.
    Issue: "No trams arriving"
    Check if there are any trams scheduled to arrive at the time.
    Ensure your BKK API Key is functioning and has permission to access the GTFS-RT feed.
    You can test this by accessing:
    https://go.bkk.hu/api/query/v1/ws/gtfs-rt/full/TripUpdates.pb .
    Issue: Missing Tram Numbers
    If tram numbers (route_short_name) don’t display:

    Ensure routes.txt is correctly placed and matches BKK's GTFS data.

    
🎯 Future Features
    Web Integration: Display live tram boards on a web dashboard (e.g., via Flask or Django).
    Full Transport Monitoring: Support stops across multiple BKK modes (bus, metro, etc.).
    Delay Notifications: Highlight delays or early arrivals by comparing static schedules to actual times.
