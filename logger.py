"""Minimal roast curve logger for Riverstone Coffee Roasters."""
import argparse
import csv
import json
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Log a roast curve")
    parser.add_argument("--roast", required=True, help="Roast name, e.g. 'Holiday Blend B'")
    parser.add_argument("--batch-kg", type=float, default=5.0)
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)
    start = time.time()
    readings, first_crack = [], None

    while True:
        entry = input("bean temp (C), 'fc' or 'q': ").strip().lower()
        elapsed = round(time.time() - start)
        if entry == "q":
            break
        if entry == "fc":
            first_crack = elapsed
            continue
        readings.append((elapsed, float(entry)))

    stem = args.roast.lower().replace(" ", "-") + time.strftime("-%Y%m%d-%H%M")
    with open(f"logs/{stem}.csv", "w", newline="") as f:
        csv.writer(f).writerows([("seconds", "bean_temp_c"), *readings])

    total = readings[-1][0] if readings else 0
    summary = {
        "roast": args.roast,
        "batch_kg": args.batch_kg,
        "total_seconds": total,
        "first_crack_seconds": first_crack,
        "development_seconds": total - first_crack if first_crack else None,
    }
    Path(f"logs/{stem}.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
