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
