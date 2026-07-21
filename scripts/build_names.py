import csv
import json
import math
import sys
import unicodedata
from pathlib import Path


GENDER_MAP = {
    "F": "female",
    "?F": "female",
    "1F": "female",
    "M": "male",
    "?M": "male",
    "1M": "male",
}


def is_latin_name(value):
    allowed = {" ", "-", "'", "’", "."}
    for char in value:
        if char in allowed:
            continue
        if not char.isalpha():
            return False
        if "LATIN" not in unicodedata.name(char, ""):
            return False
    return True


def is_usable_name(value):
    return 2 <= len(value) <= 45 and is_latin_name(value)


def merge_weight(bucket, name, weight):
    current = bucket.get(name)
    if current is None or weight > current:
        bucket[name] = weight


def parse_firstname_database(path):
    names = {"female": {}, "male": {}}
    with path.open(encoding="utf-8") as source:
        reader = csv.DictReader(source, delimiter=";")
        for row in reader:
            name = row["name"].strip()
            gender = GENDER_MAP.get(row["gender"])
            germany_bucket = row["Germany"].strip()

            if gender is None or not germany_bucket or not is_usable_name(name):
                continue

            frequency_bucket = int(germany_bucket)
            weight = max(1, 2 ** (frequency_bucket + 8))
            merge_weight(names[gender], name, weight)
    return names


def add_onomaverse_firstnames(names, path):
    with path.open(encoding="utf-8") as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["country_code"] != "DE":
                continue
            gender = GENDER_MAP.get(row["gender"])
            name = row["name"].strip()

            if gender is None or not is_usable_name(name):
                continue
            if name not in names[gender]:
                continue

            weight = max(1, round(math.sqrt(int(row["count"]))))
            merge_weight(names[gender], name, weight)


def parse_gecko_surnames(path):
    surnames = {}
    with path.open(encoding="utf-8") as source:
        reader = csv.DictReader(source)
        for row in reader:
            name = row["last_name"].strip()
            if not is_usable_name(name):
                continue
            weight = max(1, round(math.sqrt(int(row["count"]))))
            merge_weight(surnames, name, weight)
    return surnames


def add_onomaverse_surnames(surnames, path):
    with path.open(encoding="utf-8") as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["country_code"] != "DE":
                continue
            name = row["name"].strip()
            if not is_usable_name(name):
                continue
            weight = max(1, round(math.sqrt(int(row["count"]))))
            merge_weight(surnames, name, weight)


def as_weighted_list(values):
    return [
        {"name": name, "weight": weight}
        for name, weight in sorted(values.items(), key=lambda item: item[0])
    ]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    if len(sys.argv) != 6:
        raise SystemExit(
            "Usage: build_names.py <firstname_db_csv> <onomaverse_given_csv> "
            "<gecko_surnames_csv> <onomaverse_surnames_csv> <output_dir>"
        )

    firstname_db_path = Path(sys.argv[1])
    onomaverse_given_path = Path(sys.argv[2])
    gecko_surnames_path = Path(sys.argv[3])
    onomaverse_surnames_path = Path(sys.argv[4])
    output_dir = Path(sys.argv[5])

    first_names = parse_firstname_database(firstname_db_path)
    add_onomaverse_firstnames(first_names, onomaverse_given_path)

    surnames = parse_gecko_surnames(gecko_surnames_path)
    add_onomaverse_surnames(surnames, onomaverse_surnames_path)

    first_names_output = {
        "female": as_weighted_list(first_names["female"]),
        "male": as_weighted_list(first_names["male"]),
    }
    surnames_output = as_weighted_list(surnames)

    write_json(output_dir / "german_first_names.json", first_names_output)
    write_json(output_dir / "german_surnames.json", surnames_output)

    print(
        "Wrote "
        f"{len(first_names_output['female'])} female first names, "
        f"{len(first_names_output['male'])} male first names, "
        f"{len(surnames_output)} surnames."
    )


if __name__ == "__main__":
    main()
