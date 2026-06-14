import pandas as pd
import os

# ── CONFIGURATION ──────────────────────────────────────────
FOLDER = r"C:\translink_test"

# ── STEP 1: CHECK FILES ARE THERE ──────────────────────────
print("=" * 50)
print("STEP 1 — Checking files exist")
print("=" * 50)

files_needed = ["routes.txt", "trips.txt", "calendar.txt", "stop_times.txt"]

for f in files_needed:
    path = os.path.join(FOLDER, f)
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"  FOUND: {f} ({size_mb:.2f} MB)")
    else:
        print(f"  MISSING: {f} — please copy this file into C:\\translink_test")

# ── STEP 2: LOAD ROUTES ─────────────────────────────────────
print()
print("=" * 50)
print("STEP 2 — Loading routes.txt")
print("=" * 50)

routes = pd.read_csv(
    os.path.join(FOLDER, "routes.txt"),
    dtype=str
)

print(f"  Total routes found: {len(routes)}")
print(f"  Columns: {list(routes.columns)}")
print()
print("  Sample of first 5 routes:")
print(routes[["route_short_name", "route_long_name", "route_type"]].head(5).to_string(index=False))

# ── STEP 3: LOAD CALENDAR ───────────────────────────────────
print()
print("=" * 50)
print("STEP 3 — Loading calendar.txt")
print("=" * 50)

calendar = pd.read_csv(
    os.path.join(FOLDER, "calendar.txt"),
    dtype=str
)

print(f"  Total service patterns found: {len(calendar)}")
print(f"  Columns: {list(calendar.columns)}")
print()

# Find sunday services
sunday_services = calendar[calendar["sunday"] == "1"]
print(f"  Service patterns that run on Sundays: {len(sunday_services)}")

# ── STEP 4: LOAD TRIPS ──────────────────────────────────────
print()
print("=" * 50)
print("STEP 4 — Loading trips.txt")
print("=" * 50)

trips = pd.read_csv(
    os.path.join(FOLDER, "trips.txt"),
    dtype=str
)

print(f"  Total scheduled trips found: {len(trips)}")
print(f"  Columns: {list(trips.columns)}")

# ── STEP 5: FIND SUNDAY TRIPS ON R6 ─────────────────────────
print()
print("=" * 50)
print("STEP 5 — Finding Sunday trips on Route R6")
print("=" * 50)

# Get R6 route id
r6 = routes[routes["route_short_name"] == "R6"]

if len(r6) == 0:
    print("  R6 not found — trying 596 (RapidBus equivalent)...")
    r6 = routes[routes["route_short_name"] == "596"]

if len(r6) == 0:
    print("  Could not find R6 — printing all RapidBus routes instead:")
    rapid = routes[routes["route_long_name"].str.contains("RAPID", na=False)]
    print(rapid[["route_short_name", "route_long_name"]].to_string(index=False))
else:
    r6_id = r6.iloc[0]["route_id"]
    r6_name = r6.iloc[0]["route_long_name"]
    print(f"  Found: {r6_name} (route_id: {r6_id})")

    # Get sunday service IDs
    sunday_service_ids = sunday_services["service_id"].tolist()

    # Get R6 trips that run on Sundays
    r6_trips = trips[
        (trips["route_id"] == r6_id) &
        (trips["service_id"].isin(sunday_service_ids))
    ]
    print(f"  Total R6 trips on Sundays: {len(r6_trips)}")

# ── STEP 6: PEEK AT STOP TIMES ──────────────────────────────
print()
print("=" * 50)
print("STEP 6 — Peeking at stop_times.txt (first 5 rows only)")
print("=" * 50)

stop_times_peek = pd.read_csv(
    os.path.join(FOLDER, "stop_times.txt"),
    dtype=str,
    nrows=5  # Only read 5 rows — safe for any file size
)

print(f"  Columns in stop_times.txt: {list(stop_times_peek.columns)}")
print()
print("  First 5 rows:")
print(stop_times_peek.to_string(index=False))

# ── DONE ────────────────────────────────────────────────────
print()
print("=" * 50)
print("TEST COMPLETE")
print("If you see real route names and numbers above — the data works.")
print("=" * 50)