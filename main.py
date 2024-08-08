import requests
import time
from datetime import datetime, timedelta

def send_pushover_notification(token, user, message, title=""):
    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": token,
            "user": user,
            "message": message,
            "title": title
        })
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Pushover notification: {e}")

# Replace with your credentials
pushover_token = "act5hndjmohgytw4bebnpxji375ujn"
user_key = "uyyi4pbm5m9mazds8ja7xz89iusxiz"

url = "https://live.trading212.com/api/v0/equity/pies"

headers = {"Authorization": "21448836ZeOEhktWaSAFMWgLEtjIUXbgjyTTH"}

def dividends(data):
    for item in data:
        if item.get("id") == 2589470:
            progress = item.get("progress", 0)
            details = item.get("dividendDetails", {})
            value = item.get("result", {}).get("investedValue", 0)
            change = item.get("result", {}).get("value", 0)

            return f"Value in investment £{change:.2f}, increase of: £{change - value:.2f}, progress to £3,000: {progress}, Dividend Details: {details}"
    return "Dividend data not found"

def house(data):
    for item in data:
        if item.get("id") == 2589451:
            progress = item.get("progress", 0)
            value = item.get("result", {}).get("investedValue", 0)
            change = item.get("result", {}).get("value", 0)

            return f"Value in investment £{change:.2f}, increase of: £{change - value:.2f}, progress to £3,000: {progress}"
    return "House data not found"

def main():
    while True:
        response = requests.get(url, headers=headers)

        try:
            if response.status_code == 200:
                data = response.json()

                dividend_info = dividends(data)
                house_info = house(data)

                message = f"Extracted data from Trading212 response: \n\n {dividend_info}\n\n {house_info}"
                send_pushover_notification(pushover_token, user_key, message, "Trading212 Update")
            else:
                message = f"An error occurred while fetching data: API status code {response.status_code}"
                send_pushover_notification(pushover_token, user_key, message, "Trading212 Results Error")

        except Exception as e:
            message = f"An error occurred: {e}"
            send_pushover_notification(pushover_token, user_key, message, "Trading212 Results Error")

       #run every 8 hours 
        time.sleep(8 * 60 * 60)

if __name__ == "__main__":
    main()
