import requests

def send_alert():
    TOKEN = "8837972883:AAG55-uwkm72yklahipTYHhngzswSWB1Nk"
    CHAT_ID = "8729011687"
    message = "[*] Mobile automation routine completed successfully."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

if __name__ == "__main__":
    send_alert()
