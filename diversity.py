import json
import random
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
PLACES_PATH = DATA_DIR / "german_places.json"
FIELDS_PATH = DATA_DIR / "activity_fields.json"
FIRST_NAMES_PATH = DATA_DIR / "german_first_names.json"
SURNAMES_PATH = DATA_DIR / "german_surnames.json"


@lru_cache(maxsize=1)
def load_places():
    return json.loads(PLACES_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_activity_fields():
    return json.loads(FIELDS_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_first_names():
    return json.loads(FIRST_NAMES_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_surnames():
    return json.loads(SURNAMES_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_place_buckets():
    buckets = {
        "village": [],
        "town": [],
        "city": [],
    }

    for place in load_places():
        population = place["population"]
        feature_code = place["feature_code"]

        if population >= 50_000 or feature_code in {"PPLC", "PPLA", "PPLA2", "PPLA3"}:
            buckets["city"].append(place)
        elif population >= 1_000 or feature_code == "PPLA4":
            buckets["town"].append(place)
        else:
            buckets["village"].append(place)

    return buckets


def _place_weight(place):
    population = place["population"]
    base_weight = place.get("weight", 1)

    if population == 0:
        population_weight = 4
    elif population < 500:
        population_weight = 5
    elif population < 5_000:
        population_weight = 4
    elif population < 50_000:
        population_weight = 3
    elif population < 250_000:
        population_weight = 2
    else:
        population_weight = 1

    return base_weight * population_weight


def choose_place():
    buckets = load_place_buckets()
    bucket_name = random.choices(
        ["village", "town", "city"],
        weights=[55, 35, 10],
        k=1,
    )[0]
    places = buckets[bucket_name]
    weights = [_place_weight(place) for place in places]
    return random.choices(places, weights=weights, k=1)[0]


def choose_activity_field():
    return random.choice(load_activity_fields())


def _choose_weighted(items):
    weights = [item.get("weight", 1) for item in items]
    return random.choices(items, weights=weights, k=1)[0]


def choose_person():
    gender = random.choice(["female", "male"])
    first_name = _choose_weighted(load_first_names()[gender])
    surname = _choose_weighted(load_surnames())

    return {
        "gender": gender,
        "gender_de": "weiblich" if gender == "female" else "männlich",
        "first_name": first_name["name"],
        "last_name": surname["name"],
    }


def _place_type(place):
    population = place["population"]
    feature_code = place["feature_code"]

    if feature_code == "PPLC" or population >= 500_000:
        return "Großstadt"
    if feature_code in {"PPLA", "PPLA2", "PPLA3"} or population >= 100_000:
        return "Stadt oder Verwaltungssitz"
    if population >= 20_000:
        return "Stadt"
    if population >= 5_000:
        return "Kleinstadt oder größere Gemeinde"
    if population >= 1_000 or feature_code == "PPLA4":
        return "Gemeinde oder kleiner Ort"
    return "kleines Dorf oder kleine Ortschaft"


def _population_note(place):
    population = place["population"]
    if population <= 0:
        return "keine zuverlässige Einwohnerzahl in der Quelle"
    return f"ungefähr {population:,}".replace(",", ".")


def get_place_context(place):
    return {
        "place_name": place["name"],
        "place_state": place["state"],
        "place_type": _place_type(place),
        "place_population": _population_note(place),
    }
