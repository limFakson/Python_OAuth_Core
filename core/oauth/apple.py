import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import parse_qsl, urlencode

load_dotenv()


"""
Module for Apple OAUTH python package for third party application
"""


class AppleOauth:
    def __init__(self, secrets_file: dict[str, str]):
        self.secrets = secrets_file["apple"]
