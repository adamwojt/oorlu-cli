"""Main module."""
import requests

OORLU_API = "https://oor.lu/api/urls/"


def get_short_url(long_url, limit=None):
    data = {"long_url": long_url}
    if limit:
        data.update({"click_limit": limit})
    res = requests.post(OORLU_API, json=data)
    res.raise_for_status()
    return res.json()
