import pandas as pd
import os

FOLDER = r"C:\Users\inder\Downloads\google_transit"

files = [
    "agency.txt",
    "calendar.txt",
    "calendar_dates.txt",
    "direction_names_exceptions.txt",
    "directions.txt",
    "feed_info.txt",
    "route_names_exceptions.txt",
    "routes.txt",
    "shapes.txt",
    "signup_periods.txt",
    "stop_order_exceptions.txt",
    "stop_times.txt",
    "stops.txt",
    "transfers.txt",
    "translations.txt",
    "trips.txt"
]

for f in files:
    path = os.path.join(FOLDER, f)
    if os.path.exists(path):
        df = pd.read_csv(path, dtype=str, nrows=5)
        print("=" * 60)
        print(f"FILE: {f}")
        print(f"Columns: {list(df.columns)}")
        print()
        print(df.to_string(index=False))
        print()
    else:
        print("=" * 60)
        print(f"FILE: {f} — NOT FOUND")
        print()

print("=" * 60)
print("DONE")