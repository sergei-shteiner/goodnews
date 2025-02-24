from dotenv import load_dotenv, find_dotenv
import os
from openai import OpenAI
from datetime import datetime
import pytz
from weather import get_weather

from prompts import NEWS_PROMPT, LOCATION_PROMPT, WEATHER_PROMPT


_ = load_dotenv(find_dotenv())
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

model="gpt-4o-mini"
tempreture=0.8
max_tokens=100
topic=""

def generate_news():
    current_date = datetime.now(pytz.timezone('Europe/Berlin')).strftime("%d.%m.%Y")
    current_time = datetime.now(pytz.timezone('Europe/Berlin')).strftime("%H:%M")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein Journalist, der Deutsch fließend beherrscht."},
            {
                "role": "user",
                "content": NEWS_PROMPT.format(time=current_time, date=current_date),
            }
        ]
    )

    news = completion.choices[0].message.content.replace("\\n", "\n")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": LOCATION_PROMPT.format(text=news),
            }
        ]
    )

    location = completion.choices[0].message.content.replace("\\n", "\n")

    weather = get_weather(location)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": WEATHER_PROMPT.format(location=location, weather=weather),
            }
        ]
    )

    weather_report = completion.choices[0].message.content.replace("\\n", "\n")

    message = f"{news}\n\n{weather_report}"
    return message

if __name__ == "__main__":
    print(generate_news())