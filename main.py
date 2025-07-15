import requests, feedparser, os
from config import FACEBOOK_PAGE_TOKEN, FACEBOOK_PAGE_ID

FEED_URL = "https://alerts.weather.gov/cap/wwaatmget.php?x=OKC071&y=0"
LAST_ALERT_FILE = "/opt/nws-alert-bot/last_alert_id.txt"

def get_last_id():
    if os.path.exists(LAST_ALERT_FILE):
        with open(LAST_ALERT_FILE, "r") as f:
            return f.read().strip()
    return ""

def set_last_id(alert_id):
    with open(LAST_ALERT_FILE, "w") as f:
        f.write(alert_id)

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/photos"
    icon_path = "/opt/nws-alert-bot/icons/default.png"
    files = {'source': open(icon_path, 'rb')}
    data = {'caption': message, 'access_token': FACEBOOK_PAGE_TOKEN}
    response = requests.post(url, files=files, data=data)
    print("Facebook response:", response.status_code, response.text)

def main():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return
    latest = feed.entries[0]
    if latest.id == get_last_id():
        return
    message = f"🚨 {latest.title}

{latest.summary}

🔗 {latest.link}"
    post_to_facebook(message)
    set_last_id(latest.id)

if __name__ == "__main__":
    main()
