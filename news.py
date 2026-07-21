from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI
from datetime import datetime
import pytz
from diversity import choose_activity_field, choose_person, choose_place, get_place_context
from weather import get_weather_by_coordinates

from prompts import NEWS_PROMPT, WEATHER_PROMPT


_ = load_dotenv(find_dotenv())
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

NEWS_MODEL = "gpt-5.5"
WEATHER_MODEL = "gpt-5.5"

def generate_news():
    current_date = datetime.now(pytz.timezone('Europe/Berlin')).strftime("%d.%m.%Y")
    current_time = datetime.now(pytz.timezone('Europe/Berlin')).strftime("%H:%M")
    place = choose_place()
    place_context = get_place_context(place)
    weather_place = place["name"]
    activity_field = choose_activity_field()
    person = choose_person()

    completion = client.chat.completions.create(
        model=NEWS_MODEL,
        messages=[
            {"role": "system", "content": "Du bist ein Journalist, der Deutsch fließend beherrscht."},
            {
                "role": "user",
                "content": NEWS_PROMPT.format(
                    time=current_time,
                    date=current_date,
                    activity_field=activity_field,
                    first_name=person["first_name"],
                    last_name=person["last_name"],
                    gender=person["gender_de"],
                    **place_context,
                ),
            }
        ]
    )

    news = completion.choices[0].message.content.replace("\\n", "\n")

    weather = get_weather_by_coordinates(place["lat"], place["lon"])

    completion = client.chat.completions.create(
        model=WEATHER_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": WEATHER_PROMPT.format(location=weather_place, weather=weather),
            }
        ]
    )

    weather_report = completion.choices[0].message.content.replace("\\n", "\n")

    message = f"{news}\n\n{weather_report}"
    return message

if __name__ == "__main__":
    print(generate_news())
