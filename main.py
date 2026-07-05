import os
import requests
import json
import time

def get_currency_codes():
    currency = input("Enter the first currency code (e.g., USD, EUR, GBP): ").upper().strip()
    currency2 = input("Enter the second currency code (e.g., USD, EUR, GBP): ").upper().strip()
    return [currency, currency2]


def fetch_data(codes):
    response = requests.get(f"https://open.er-api.com/v6/latest/{codes[0]}", timeout=(5))
    response.raise_for_status()
    data = response.json()
    if data["result"] == "error":
        return {"error": data["error-type"]}
    else:
        return data


def save_local_data(data, codes):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{codes[0]}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_local_data(codes, is_offline):
    local_data = os.listdir("data")
    for file in local_data:
        if file == f"{codes[0]}.json":
            with open(f"data/{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
                if data["time_next_update_unix"] > int(time.time()):
                    return data
                elif is_offline:
                    return data
    else:
        return False
            

def get_rates():
    try:
        codes = get_currency_codes()
        data = load_local_data(codes, False) or fetch_data(codes)

        if "error" in data:
            print("These currency rates are not supported.")
            return

        print(round(data["rates"][codes[1]], 2))
        save_local_data(data, codes)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        print("You don't seem to be online")
        data = load_local_data(codes, True)
        if data:
            print(f"Outdated data loaded: {round(data["rates"][codes[1]], 2)}")
            print(f"Last update time:{data["time_last_update_utc"]}")

get_rates()