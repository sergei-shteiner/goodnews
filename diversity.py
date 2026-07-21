import json
import random
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
PLACES_PATH = DATA_DIR / "german_places.json"
FIELDS_PATH = DATA_DIR / "activity_fields.json"
FIRST_NAMES_PATH = DATA_DIR / "german_first_names.json"
SURNAMES_PATH = DATA_DIR / "german_surnames.json"

DEFAULT_POPULATION_BY_FEATURE_CODE = {
    "PPLC": 500_000,
    "PPLA": 75_000,
    "PPLA2": 35_000,
    "PPLA3": 20_000,
    "PPLA4": 5_000,
    "PPL": 500,
    "PPLX": 250,
}


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
def load_place_weights():
    return [_estimated_population(place) for place in load_places()]


def choose_place():
    places = load_places()
    return random.choices(places, weights=load_place_weights(), k=1)[0]


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


def _estimated_population(place):
    if place["population"] > 0:
        return place["population"]
    return DEFAULT_POPULATION_BY_FEATURE_CODE.get(place["feature_code"], 500)


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
