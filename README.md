# RssBotDiscord

<img src="https://github.com/user-attachments/assets/4343078a-fee8-4cec-ac10-bed67f2e92d8" width="500" />

RSS Feed to Discord Bot
This Python-based tool monitors multiple RSS feeds and sends notifications to Discord channels when new entries are found. The bot checks the RSS feeds at regular intervals, queues the new entries, and sends them to your Discord channel while handling rate limits to ensure smooth operation.

The tool can also send a success notification to a separate Discord channel once all feeds have been successfully processed.

## Features:
RSS Feed Monitoring: Checks a list of RSS feeds for new entries at configurable intervals.

Discord Notifications: Sends new feed entries to a Discord channel using a webhook.

Rate-Limiting Handling: Automatically handles rate limits from Discord by retrying failed messages after a delay.

Success Notification: Sends a success message to a separate webhook indicating that all feeds have been checked and processed.

Persistent State: Keeps track of processed RSS feed entries, ensuring that duplicate notifications are not sent.

Configurable: Easily configure the interval for checking RSS feeds and sending messages.

## How It Works:
RSS Feed Checking: The bot reads the RSS feed URLs from a file (rss.txt) and periodically checks for new entries.

Duplicate Handling: It keeps track of previously processed entries to avoid sending duplicate notifications.

Discord Notifications: When a new feed entry is found, the bot sends a message to the configured Discord webhook.

Success Notification: After checking all the feeds, the bot sends a success message to a secondary Discord webhook.

Rate Limiting: If the bot encounters rate-limiting from Discord (HTTP 429), it waits for the specified amount of time before retrying the failed message.

## Configuration:
DISCORD_WEBHOOK_URL: The webhook URL for sending new RSS entries to your Discord channel.

SUCCESS_WEBHOOK_URL: A separate webhook URL for sending a success message after processing all RSS feeds.

BOT_TOKEN: The token for your Discord bot.

RSS_FILE: The file containing a list of RSS feed URLs (one per line).

CHECK_INTERVAL: How often the bot checks the RSS feeds (in seconds).

SEND_INTERVAL: How often the bot sends a message to Discord (in seconds).

## Setup Instructions:

1. Create Your Discord Bot:
To use this tool, you’ll first need to create a Discord bot and get its token. Follow these steps:

Go to the Discord Developer Portal.

Click on New Application and give your bot a name.

Under the Bot tab, click Add Bot to create the bot.

Once your bot is created, you’ll see the Token under the bot settings. Copy this token; you’ll need it for the BOT_TOKEN in the configuration file.

In the OAuth2 section, set the bot’s permissions (you may need to add permissions like Send Messages).

Use the generated URL to invite the bot to your Discord server.

## 2. Clone the Repository:

```bash
git clone https://github.com/tobiasGuta/RssBotDiscord.git
```

## 3. Install Dependencies:
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 4. Configure the Bot:
rss.txt: Create a file called rss.txt and add the URLs of the RSS feeds you want to monitor, one URL per line.

DISCORD_WEBHOOK_URL: Replace this with your actual Discord webhook URL for sending new RSS entries to your channel.

SUCCESS_WEBHOOK_URL: Replace this with a separate Discord webhook URL for sending a success message after processing all RSS feeds.

BOT_TOKEN: Paste the bot token you copied from the Discord Developer Portal into this field.

## 5. Run the Bot:
To start the bot and monitor the RSS feeds, run the following command:
```bash
python rss.py
```
The bot will now start checking your RSS feeds and sending new entries to your Discord channel. It will also send a success message to the secondary webhook once all the feeds have been processed.

## Example Output:
```bash
INFO:root:Checking RSS: https://example.com/rss
INFO:root:🆕 Queuing: New Entry - Title
INFO:root:✅ Sent: New Entry - Title
INFO:root:✅ Sent success notification
```

