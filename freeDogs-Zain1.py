import requests
from urllib.parse import urlparse, parse_qs
import hashlib
import time

# Display custom ASCII banner
def display_banner():
    banner = """
╔══════════════════════════════════╗
║                                  ║
║       CREPTO_MINING BOT          ║
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
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAGR_EQxAgAAAJH8RDGKwieY%26user%3D%257B%2522id%2522%253A5121571985%252C%2522first_name%2522%253A%2522Crepto%2522%252C%2522last_name%2522%253A%2522Mining%2522%252C%2522username%2522%253A%2522Crepto_Mining1%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252FNAr0Q0NI9tk7PUEbBkXAfmqkFzHJOnBI25EZTsvy1jZVQ1icL6GFiNeiBtlGY9rj.svg%2522%257D%26auth_date%3D1733132158%26signature%3D6ua1_abNHrkYnSAPtuXBe-8OR4Fo9pAflce4kTZ1dpFdJJm98kUe41ooQTsBYjUGYXO89FGwsNNY5PbVzFqgBA%26hash%3D216c103b4176bccadc8fd99fa2965c72838b93cc77a706f3e3ff1cf73acb58bb&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAE4l5QDAwAAADiXlAMcuEA0%26user%3D%257B%2522id%2522%253A6502520632%252C%2522first_name%2522%253A%2522Wo%2522%252C%2522last_name%2522%253A%2522lf%2522%252C%2522username%2522%253A%2522Wo_lf_0%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252FEoerCqsizcxe11kUriTd8w7tVJth2eXP2Q1Hd6ggmQT_YjF-NQnLD5xsPHe4RzQW.svg%2522%257D%26auth_date%3D1733135084%26signature%3DUrjsMQHS7UOiSWMukKsnN53BwkeIry70oc7BMLx7zfOVX17-lf6aCKoq7PUxbAt-kNqVa61PHFbBeS4j9RO4DA%26hash%3Dcef1ceb234e0b7e4dd52526198ede553305cc14bcafa2f465bf4aff7f000962c&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAE3Nh5KAgAAADc2HkrR6OL0%26user%3D%257B%2522id%2522%253A5538461239%252C%2522first_name%2522%253A%2522Black%2522%252C%2522last_name%2522%253A%2522Pearl%2520%25E2%2596%25AA%25EF%25B8%258F%2522%252C%2522username%2522%253A%2522loone_wolf%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252Fzt_LA_vFjBy2MPDBh-0savwkXZ1M_Uhg2GUG5N5QFYG3Mx9xcx-PGewJrO6mZ57T.svg%2522%257D%26auth_date%3D1733136034%26signature%3D9oH6_8y-PRUmROPNFyLCH2CZBor1TpxfHiioiK2PH0GRZDxXZZllTfE745Aw8az00dHruP7Ck-1YYm9uA7nbCQ%26hash%3D24bd13dd80c850f2a8300a317033dbaad997e461ff6f2e84c929e56b2660e498&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAEklAgFAwAAACSUCAUWQlO9%26user%3D%257B%2522id%2522%253A6526899236%252C%2522first_name%2522%253A%2522Sultan%2522%252C%2522last_name%2522%253A%2522Mehmed%2520%25E2%2596%25AA%25EF%25B8%258F%2522%252C%2522username%2522%253A%2522Wo_lf391%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252FG4LFTb-A6y5nam1Sq_dC8F0MgZ5EedDpMJ0MsYQSdqGSGPXS6SeV9a4MrRK9fdJs.svg%2522%257D%26auth_date%3D1733136114%26signature%3DshF8SQWL8wbJ8lMfQYmGfUVCTeMoJqoiZivozAfJmNdib5oEsUNXP6YkGrMPdc3Hbp5oYyQ3_ykY2ea6M9ClAQ%26hash%3D76f74ec027250b6907803712257acd068a4b9a5acfc6c7ca5a841ca0749c377f&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAE48hw4AwAAADjyHDjHpoH4%26user%3D%257B%2522id%2522%253A7383872056%252C%2522first_name%2522%253A%2522Sheikh%2522%252C%2522last_name%2522%253A%2522Aqib%2520%25E2%2596%25AA%25EF%25B8%258F%2522%252C%2522username%2522%253A%2522sheikhaqib400%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252Fs3w8jLhIgv8HSKsSaKIeqH4mnfrqQzARRTvsXFgTHy4AN8fqVaSAP8CMEKEhXIWb.svg%2522%257D%26auth_date%3D1733136227%26signature%3DzzcsW7dC6CYwM9fTvHzDkK-J0sYnGTCneKKgNo2_JSshlvFxiQuUCPPYchY92DeFfz717bWgKkOKerx63sm2Aw%26hash%3D46a9349517b0c1e3f6966cb06a388fa5b5c37f625ff5317feca31e486a218689&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
        "https://app.freedogs.bot/#tgWebAppData=query_id%3DAAFccVkmAwAAAFxxWSYFpU7r%26user%3D%257B%2522id%2522%253A7085846876%252C%2522first_name%2522%253A%2522The%2520Black%2522%252C%2522last_name%2522%253A%2522Pearl%2520%25E2%2596%25AA%25EF%25B8%258F%2522%252C%2522username%2522%253A%2522blackpearl400%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252FC72ucbXY8ZSkQZL4T0UJmQAmeodRpn-Lg32hwwfrn9XDfFPJ86hkEoja9N96MHaH.svg%2522%257D%26auth_date%3D1733136330%26signature%3DJ9NnI4MxmdOqTDqftk5q-GTapFAhrmEWe-yXMNgbv_xwOrybWzbVX0iLnQgzJDtluho8u63_xdLTIvX7cpQqAQ%26hash%3Dcca0f1691135c670aff79bbcfd6c95db6b8bbed972ce411bca47b6fbdbd2dbc1&tgWebAppVersion=8.0&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D",
          
                   # Add session links here as before
    ]

    while True:  # Infinite loop to repeat the process
        for session_link in session_links:
            process_session(session_link)
            time.sleep(5)  # Optional delay between sessions (in seconds)
