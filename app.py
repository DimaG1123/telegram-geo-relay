from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Unified chat for all briefs
UNIFIED_CHAT_ID = "-1002666505819"

# Map agent names to the unified chat
AGENT_CHAT_MAP = {
    "african_geo_brief": UNIFIED_CHAT_ID,
    "us_geo_brief": UNIFIED_CHAT_ID,
    "asia_geo_brief": UNIFIED_CHAT_ID,
    "daily_gmena_brief": UNIFIED_CHAT_ID,
    "weekly_tech_culture": UNIFIED_CHAT_ID
    # latam_geo_brief, internship_tracker, job_tracker are intentionally excluded
}

def send_to_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/dispatch/<agent>', methods=['POST'])
def dispatch(agent):
    data = request.get_json()
    if agent not in AGENT_CHAT_MAP:
        return jsonify({"error": "Agent not supported"}), 400

    chat_id = AGENT_CHAT_MAP[agent]
    title = data.get("title", f"{agent.replace('_', ' ').title()} Update")
    content = data.get("content", "")
    timestamp = data.get("timestamp", "")

    message = f"*{title}*\n\n{content}\n\n_Time: {timestamp}_"
    result = send_to_telegram(chat_id, message)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)

