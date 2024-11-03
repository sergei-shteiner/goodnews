from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import random
import pytz
from telegram import send_news

# Определяем часовой пояс Берлина
berlin_tz = pytz.timezone('Europe/Berlin')

def job():
    send_news()
    schedule_random_job()

scheduler = BlockingScheduler(timezone=berlin_tz)

def schedule_random_job():
    # Случайное время на следующий день по Берлинскому времени
    now = datetime.now(berlin_tz)
    next_day = now + timedelta(days=1)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    run_time = next_day.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)

    scheduler.add_job(job, 'date', run_date=run_time)
    print(f"Next task scheduled at {run_time} (Berlin time).")

# Планируем первую задачу
schedule_random_job()

# Запускаем планировщик
scheduler.start()