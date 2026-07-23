# goodnews

Flask app that generates a German good-news story and appends current weather for
the generated location.

## Environment

Create a `.env` file with:

```dotenv
OPEN_AI_API_KEY=...
OPENWEATHERMAP_API_KEY=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=...
```

## Telegram channel publishing

The `/` route only renders a generated news item. The `/publish` route generates
a news item, publishes it to Telegram, and renders it.

To publish generated news items to Telegram:

1. Create a Telegram channel.
2. Create a bot via `@BotFather` and copy its token to `TELEGRAM_BOT_TOKEN`.
3. Add the bot to the channel as an administrator with permission to post
   messages.
4. Set `TELEGRAM_CHANNEL_ID` to the channel username, for example
   `@gute_nachrichten`, or to the numeric channel id for a private channel.

If Telegram is not configured or posting fails, the website still renders the
generated news and logs a warning.

## Exhibition print queue

The `/publish` route also adds the generated news item to a short-lived print
queue. A local laptop near the printer can fetch fresh jobs and save them as
PDFs:

```bash
python print_agent.py --once
python print_agent.py --output-dir output/pdf
```

The agent fetches `/print/jobs`, writes one PDF per fresh job, then marks each
job done with `/print/jobs/<id>/done`. Jobs older than 120 seconds are expired
and skipped, so stale exhibition prints do not pile up if the laptop sleeps.

## Diversity data

German place names are generated from the GeoNames Germany dump. To rebuild the
local JSON after downloading and unpacking `DE.zip`:

```bash
python scripts/build_german_places.py /path/to/DE.txt data/german_places.json
```

First names are generated from `firstname-database`, with weights enriched from
Onomaverse where names overlap. Surnames are generated from `gecko-data`, with
additional German entries from Onomaverse. To
rebuild the local JSON files after downloading those CSV files:

```bash
python scripts/build_names.py \
  /path/to/firstnames.csv \
  /path/to/onomaverse-given-name-frequency.csv \
  /path/to/gecko-last-name.csv \
  /path/to/onomaverse-surname-frequency.csv \
  data
```

The runtime samples gender 50:50 first, then samples a first name from the
selected gender bucket and a surname from the surname corpus.

Activity fields are maintained in `data/activity_fields.json`.
