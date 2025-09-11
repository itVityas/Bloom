from django.conf import settings
import requests


def get_1c_declaration_data(number: str = None, date: str = None) -> list:
    """get list of declaration data from 1c by declaration and date

    Args:
        number (str): number of declaration.
        date (str): date of declaration (yyyymmdd)
"""
    payload = {
        "declarations": [
            {
                "number": number,
                "date": date
            }
        ]
    }

    response = requests.get(
            settings.API_1C_URL_GTD,
            json=payload,
            auth=(settings.API_USERNAME, settings.API_PASSWORD),
            timeout=30
        )
    response.raise_for_status()

    try:
        data = response.json()
        return data
    except Exception as e:
        print(e)
        return None
