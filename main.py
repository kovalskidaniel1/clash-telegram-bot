import requests
import time

# === CONFIG ===
CR_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjRlMmRhYzRiLWE2MmItNGY4My05ZGM3LTRhZThhMWU3Y2M1NSIsImlhdCI6MTc2MTAzOTU5Nywic3ViIjoiZGV2ZWxvcGVyL2ViYWVkNjhjLWFlODItOGY4Mi1iN2Q1LTJkZGRiNGY2MjFkMiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIwLjAuMC4wIiwiOTQuMjI1LjQ5LjEyMyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.JtWazI7tZiXMLW455HOeAkjWoYCAhAuLTuXT4MOugT8rV71LVrtkIHXYpbHIEbpIgIeBrUy8DgoqtIG4Iznmcw"
CLAN_TAG = "#QJYQ0G2U"
TG_BOT_TOKEN = "8495391473:AAGR46V8SayFLEL3GOm49y4RyPc80LTNUus"
CHAT_ID = "-4892135927"

# === HEADERS ===
headers = {"Authorization": f"Bearer {CR_API_KEY}"}

def get_clan():
    url = f"https://api.clashroyale.com/v1/clans/{CLAN_TAG.replace('#', '%23')}"
    return requests.get(url, headers=headers).json()

def send_message(text):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

previous_members = set()

while True:
    clan = get_clan()
    members = {m["tag"]: m for m in clan.get("memberList", [])}

    # Detect joins/leaves
    joined = [m["name"] for t, m in members.items() if t not in previous_members]
    left = [t for t in previous_members if t not in members]

    if joined:
        send_message("👋 Joined clan: " + ", ".join(joined))
    if left:
        send_message("🚪 Left clan: " + ", ".join(left))

    previous_members = set(members.keys())
    time.sleep(300)  # refresh every 5 minutes

