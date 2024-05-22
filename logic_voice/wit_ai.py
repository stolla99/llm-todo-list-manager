from string import Template
import requests

wit_api_token = "<place owm api token here>"


def synthesize_speech_from_text(text: str):
    """
    This function synthesizes speech from a given text using the Wit.ai API.

    Args:
        text (str): The text to be synthesized into speech.

    Returns:
        Response: The response from the Wit.ai API. The response body contains the synthesized speech in WAV format.
    """
    url = "https://api.wit.ai/synthesize?v=20240304"
    headers = {
        "Authorization": Template("Bearer $wit_api_token").substitute(wit_api_token=wit_api_token),
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    data = {
        "q": text,
        "voice": "Rebecca",
        "style": "soft",
    }
    response = requests.post(url, headers=headers, json=data)
    return response
