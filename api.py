import cloudscraper
import re
import requests
from flask import Flask, request

app = Flask(__name__)

sent_files = set()

@app.route('/send_to_telegram', methods=['GET'])
def send_to_telegram():
    TELEGRAM_BOT_TOKEN = request.args.get('token')
    TELEGRAM_CHAT_ID = request.args.get('chat_id')

    scraper = cloudscraper.create_scraper()
    a = scraper.get(request.args.get('url')).text

    search = re.findall(r'href="(.*?)"',a,re.DOTALL)

    for link in search:
        if link.startswith('https://pastpapers.papacambridge.com') and link.endswith('.pdf'):
            file_url = link
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "document": file_url
            }
            try:
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"File sent to Telegram successfully: {file_url}")
                    sent_files.add(file_url)
                else:
                    print(f"Failed to send file to Telegram: {response.text}")
            except Exception as e:
                print(f"Failed to send file to Telegram: {e}")

    return "Process completed."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# Infinite loop to keep the app running

