#'''Hello i am having issues getting an OBS script to work. It should retrieve my gamerscore from OpenXBL every 60 seconds and then update the digits on screen with a randomly selected style, each style has already been made and set in the file path. The documentation is available here: https://xbl.io/docs/account  Here is my current code:'''
import os
import random
import glob
import obspython
import requests
import json
import time
import threading

# Global configuration variables (change these as needed)
GAMERTAG = "<GAMERTAG>"
API_KEY = "<OPENXBL API KEY>"
BASE_FOLDER_PATH = r"<FOLDER PATH>"

def set_image_source_file_path(source_name, file_path):
    source = obspython.obs_get_source_by_name(source_name)
    if source is not None:
        settings = obspython.obs_source_get_settings(source)
        obspython.obs_data_set_string(settings, "file", file_path)
        obspython.obs_source_update(source, settings)
        obspython.obs_data_release(settings)
        obspython.obs_source_release(source)

def get_descriptions(base_folder, folder_name):
    description_files = glob.glob(os.path.join(base_folder, folder_name, "*-0.png"))
    descriptions = [os.path.basename(f).split('-')[0] for f in description_files]
    return descriptions

def set_gamerscore_images(gamerscore):
    # Select a random folder containing number styles.
    folder_names = os.listdir(BASE_FOLDER_PATH)
    folder_name = random.choice(folder_names)

    # Get the descriptions for the number styles in the selected folder.
    description_files = glob.glob(os.path.join(BASE_FOLDER_PATH, folder_name, "*-0.png"))
    descriptions = [os.path.basename(f).split('-')[0] for f in description_files]

    print("descriptions:", descriptions)  # Print the descriptions list

    # Set the image source for each digit in the gamerscore.
    for i, digit in enumerate(gamerscore):
        source_name = f"Digit {i+1}"
        description_index = int(digit) % len(descriptions)  # Ensure index is within the range
        print("description_index:", description_index)  # Print the description_index value
        
        description = descriptions[description_index]
        file_path = os.path.join(BASE_FOLDER_PATH, folder_name, f"{description}-{digit}.png")  # Use digit instead of i+1
        set_image_source_file_path(source_name, file_path)

def update_gamerscore(obs_settings):
    # Make request to Xbox API
    url = "https://xbl.io/api/v2/account"
    headers = {
        "Accept": "application/json",
        "x-authorization": API_KEY
    }
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code != 200:
        print("[Unknown Script] HTTP status code:", response.status_code)
        print("[Unknown Script] JSON response:", response.text)
        print("[Unknown Script] An unexpected error occurred")
        return None

    # Extract gamerscore value from JSON response
    try:
        data = json.loads(response.text)
        gamerscore = data["profileUsers"][0]["settings"]
        gamerscore_value = None
        for setting in gamerscore:
            if setting["id"] == "Gamerscore":
                gamerscore_value = setting["value"]
                break

        if gamerscore_value is None:
            raise ValueError("Gamerscore not found in API response")

        # Update OBS scene item with gamerscore value
        set_gamerscore_images(str(gamerscore_value))

    except Exception as e:
        print("[Unknown Script] Error:", e)
        print("[Unknown Script] The API response is empty, malformed, or gamerscore not found")
        return None

    # Return the sleep time
    return random.randint(60, 90)

def update_thread(obs_settings):
    while True:
        time.sleep(30)  # Ensure app is actually taking a break
        sleep_time = update_gamerscore(obs_settings)
        if sleep_time is not None:
            time.sleep(sleep_time)

def script_description():
    return "Updates your Xbox gamerscore every few minutes and displays it using images of numbers from different folders."

def script_update(settings):
    obs_settings = settings_to_dict(settings)
    update_gamerscore(obs_settings)


def script_defaults(settings):
    obspython.obs_data_set_default_string(settings, "gamertag", GAMERTAG)
    obspython.obs_data_set_default_string(settings, "api_key", API_KEY)

def script_properties():
    props = obspython.obs_properties_create()

    obspython.obs_properties_add_text(props, "gamertag", "Gamertag", obspython.OBS_TEXT_DEFAULT)
    obspython.obs_properties_add_text(props, "api_key", "API Key", obspython.OBS_TEXT_PASSWORD)

    return props

def script_load(settings):
    obs_settings = settings_to_dict(settings)
    thread = threading.Thread(target=update_thread, args=(obs_settings,))
    thread.start()

def settings_to_dict(settings):
    obs_data = obspython.obs_data_create_from_json(obspython.obs_data_get_json(settings))
    settings_dict = {}
    key = obspython.obs_data_first(obs_data)
    while key is not None:
        settings_dict[key] = obspython.obs_data_get_string(obs_data, key)
        key = obspython.obs_data_next(obs_data)

    obspython.obs_data_release(obs_data)
    return settings_dict

