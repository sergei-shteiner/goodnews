import json
import sys
from pathlib import Path


ADMIN1_NAMES = {
    "01": "Baden-Württemberg",
    "02": "Bayern",
    "03": "Bremen",
    "04": "Hamburg",
    "05": "Hessen",
    "06": "Niedersachsen",
    "07": "Nordrhein-Westfalen",
    "08": "Rheinland-Pfalz",
    "09": "Saarland",
    "10": "Schleswig-Holstein",
    "11": "Brandenburg",
    "12": "Mecklenburg-Vorpommern",
    "13": "Sachsen",
    "14": "Sachsen-Anhalt",
    "15": "Thüringen",
    "16": "Berlin",
}

FEATURE_WEIGHTS = {
    "PPL": 5,
    "PPLA4": 4,
    "PPLA3": 3,
    "PPLA2": 2,
    "PPLA": 1,
    "PPLC": 1,
    "PPLX": 2,
}

BLOCKED_NAME_PARTS = (
    "siedlung",
    "bahnhof",
    "haltepunkt",
    "gewerbegebiet",
    "industriegebiet",
    "flugplatz",
    "kasernen",
    "kaserne",
)


def is_usable_name(name):
    normalized = name.casefold()
    if len(name) < 3 or len(name) > 45:
        return False
    if any(part in normalized for part in BLOCKED_NAME_PARTS):
        return False
    if any(char.isdigit() for char in name):
        return False
    return True


def build_places(source_path):
    by_key = {}
    with source_path.open(encoding="utf-8") as source:
        for line in source:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 19:
                continue

            name = cols[1]
            feature_class = cols[6]
            feature_code = cols[7]
            admin1 = cols[10]
            population = int(cols[14] or 0)

            if feature_class != "P" or feature_code not in FEATURE_WEIGHTS:
                continue
            if admin1 not in ADMIN1_NAMES or not is_usable_name(name):
                continue

            key = (name, admin1)
            item = {
                "name": name,
                "state": ADMIN1_NAMES[admin1],
                "feature_code": feature_code,
                "population": population,
                "lat": float(cols[4]),
                "lon": float(cols[5]),
                "weight": FEATURE_WEIGHTS[feature_code],
            }

            current = by_key.get(key)
            if current is None:
                by_key[key] = item
                continue

            if population > current["population"]:
                by_key[key] = item

    places = sorted(by_key.values(), key=lambda item: (item["state"], item["name"]))
    return places


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: build_german_places.py <geonames_DE.txt> <output_json>")

    source_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    places = build_places(source_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(places, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(places)} places to {output_path}")


if __name__ == "__main__":
    main()
