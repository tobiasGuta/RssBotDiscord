import discord
import feedparser
import asyncio
import aiohttp
import logging
from datetime import datetime
from urllib.parse import urlparse

# ===== CONFIGURATION =====
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/REDACTED"
SUCCESS_WEBHOOK_URL = "https://discord.com/api/webhooks/REDACTED"
BOT_TOKEN = 'REDACTED'
RSS_FILE = "rss.txt"
CHECK_INTERVAL = 1200  # 20 minutes
SEND_INTERVAL = 10

# ===== SETUP =====
logging.basicConfig(level=logging.INFO)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
message_queue = asyncio.Queue()
check_started = False  # Global guard for double loop
sent_articles = set()

# ===== UTILITY FUNCTIONS =====
def read_rss_feeds(filename):
    with open(filename, 'r') as file:
        return [url.strip() for url in file.readlines() if url.strip()]

def load_seen_entries():
    try:
        with open("seen_entries.txt", "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_seen_entries(seen):
    with open("seen_entries.txt", "w") as f:
        for item in seen:
            f.write(item + "\n")

def clean_link(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

# ===== DISCORD SEND WORKER =====
async def discord_sender():
    while True:
        title, link = await message_queue.get()
        payload = {'content': f"New entry found: {title} - {link}"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(DISCORD_WEBHOOK_URL, json=payload) as response:
                    if response.status == 204:
                        logging.info(f"✅ Sent: {title}")
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 10))
                        logging.warning(f"⏳ Rate limited. Waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        await message_queue.put((title, link))
                    else:
                        logging.error(f"❌ Failed to send ({response.status})")
            except Exception as e:
                logging.error(f"⚠️ Error sending to Discord: {e}")

        await asyncio.sleep(SEND_INTERVAL)

# ===== SUCCESS NOTIFICATION =====
async def send_success_notification():
    payload = {'content': "Rss Tool run successful: All RSS feeds checked and processed."}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(SUCCESS_WEBHOOK_URL, json=payload) as response:
                if response.status == 204:
                    logging.info("✅ Sent success notification")
                else:
                    logging.error(f"❌ Failed to send success notification ({response.status})")
        except Exception as e:
            logging.error(f"⚠️ Error sending success notification: {e}")

# ===== RSS CHECKER =====
async def check_rss():
    seen = load_seen_entries()
    while True:
        logging.info(f"--- Starting RSS check at {datetime.utcnow()} ---")
        rss_urls = read_rss_feeds(RSS_FILE)
        for url in rss_urls:
            logging.info(f"🔍 Checking RSS: {url}")
            feed = feedparser.parse(url)

            for entry in feed.entries:
                entry_id = (
                    entry.get('id') or
                    clean_link(entry.get('link', '')) or
                    (entry.get('title', '') + entry.get('published', ''))
                )
                unique_key = f"{url}::{entry_id}"
                logging.info(f"🔑 Unique key: {unique_key}")

                if unique_key in seen:
                    continue

                seen.add(unique_key)
                title = entry.get("title", "No Title")
                link = entry.get("link", "No Link")
                logging.info(f"🆕 Queuing: {title}")
                await message_queue.put((title, link))

        save_seen_entries(seen)
        await send_success_notification()
        logging.info(f"🛌 Sleeping for {CHECK_INTERVAL} seconds")
        await asyncio.sleep(CHECK_INTERVAL)

# ===== BOT STARTUP =====
@client.event
async def on_ready():
    global check_started
    if check_started:
        logging.warning("🛑 RSS check already running, skipping duplicate start")
        return
    check_started = True
    logging.info(f"🤖 Logged in as {client.user}")
    await asyncio.gather(check_rss(), discord_sender())

client.run(BOT_TOKEN)
