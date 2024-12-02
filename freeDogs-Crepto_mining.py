import requests
from urllib.parse import urlparse, parse_qs
import hashlib
import time

# Display custom ASCII banner
def display_banner():
    banner = """
╔══════════════════════════════════╗
║                                  ║
║        CM Scripts BOT          ║
║       AUTOMATION EXPERT          ║
║                                  ║
║   FAST - RELIABLE - SECURE       ║
║   MULTI-SESSION SUPPORTED        ║
║                                  ║
╚══════════════════════════════════╝
"""
    print(banner)
    print("\nStarting the coin collection process...\n")

# Generate MD5 hash for authentication
def compute_md5(amount: str, seq: int) -> str:
    secret = "7be2a16a82054ee58398c5edb7ac4a5a"
    hash_input = f"{amount}{seq}{secret}"
    return hashlib.md5(hash_input.encode()).hexdigest()

# Extract initialization data from URL
def parse_init_data(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.fragment)
        init_data = query_params.get("tgWebAppData", [None])[0]
        if not init_data:
            raise ValueError("Invalid session link")
        return init_data
    except Exception as e:
        print(f"Error parsing session link: {e}")
        return None

# Authenticate and retrieve token
def authenticate(init_data: str, headers: dict) -> str:
    auth_url = "https://api.freedogs.bot/miniapps/api/user/telegram_auth"
    data = {"invitationCode": "", "initData": init_data}
    
    try:
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        if 'data' in response_data and 'token' in response_data['data']:
            return response_data['data']['token']
        else:
            print("Authentication failed:", response_data)
            return None
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

# Retrieve game information
def get_game_info(headers: dict) -> dict:
    game_info_url = "https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo"
    try:
        response = requests.get(game_info_url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error retrieving game info: {e}")
        return None

# Collect coins
def collect_coins(headers: dict, seq: int, amount: str = "100000") -> dict:
    collect_url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin"
    hash_code = compute_md5(amount, seq)
    params = {
        "collectAmount": amount,
        "hashCode": hash_code,
        "collectSeqNo": str(seq),
    }
    try:
        response = requests.post(collect_url, headers=headers, data=params)
        return response.json()
    except Exception as e:
        print(f"Error collecting coins: {e}")
        return None

# Main execution function
def process_session(session_link: str):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "x-requested-with": "org.telegram.messenger",
    }

    init_data = parse_init_data(session_link)
    if not init_data:
        print("Skipping invalid session link.")
        return

    token = authenticate(init_data, headers)
    if not token:
        print("Authentication failed. Skipping session.")
        return

    headers["authorization"] = f"Bearer {token}"
    game_info = get_game_info(headers)

    if not game_info or "data" not in game_info or "collectSeqNo" not in game_info["data"]:
        print("Failed to retrieve game info. Skipping session.")
        return

    seq = game_info["data"]["collectSeqNo"]
    collect_response = collect_coins(headers, seq)

    print("Collection Result:", collect_response)

# Entry point
if __name__ == "__main__":
    display_banner()
    
    # Add your session links here
    session_links = [
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGK************************************************", #add your own complete session links here
          
        # Add session links here as before
    ]

    while True:  # Infinite loop to repeat the process
        for session_link in session_links:
            process_session(session_link)
            time.sleep(5)  # Optional delay between sessions (in seconds)
