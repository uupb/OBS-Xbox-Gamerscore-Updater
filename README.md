# OBS-Xbox-Gamerscore-Updater
This script is designed for OBS Studio to fetch and display your Xbox gamerscore with a randomly selected style. It updates the gamerscore every minute or so.


## Prerequisites

- OBS Studio
- An Xbox account with a valid API Key from OpenXBL (https://xbl.io/)

## Usage

1. Download the script `OBS_Xbox_Gamerscore.py`.
2. In OBS Studio, go to `Tools` > `Scripts`, click the `+` button and select the downloaded script file.
3. Set your Xbox `Gamertag` and `API Key` from OpenXBL in the script properties.

**Note:** You'll need to set up your image sources for the individual digits in your OBS scene (named "Digit 1", "Digit 2", and so on) and create the folders containing the number style images with names formatted as "{description}-{digit}.png" (e.g., "Style1-0.png").

## How it works

The script sends an API request to OpenXBL to fetch your Xbox gamerscore. It then randomly selects a style from the pre-configured folders and updates the image sources in your OBS scene with the corresponding digit images.

The script uses the Python `obspython` module to interact with OBS Studio and the `requests` module to make API calls to OpenXBL. It also employs threading to update the gamerscore in the background without affecting the OBS Studio performance.

## Customization

You can customize the following global variables in the script:

- `GAMERTAG`: Your Xbox gamertag.
- `API_KEY`: Your OpenXBL API key.
- `BASE_FOLDER_PATH`: The folder path containing the number style images.

## License

This script is provided under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify it as you see fit.
