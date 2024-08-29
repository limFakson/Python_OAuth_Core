import os
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import parse_qsl, urlencode

load_dotenv()

"""
Module for Google OAUTH python library for third party apps
"""

class GoogleOauth:

    def __init__(self, secrets_file: str):
        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
        self.secrets = self.load_secrets(secrets_file)
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.port = 8000
        self.redirect_uri = f'{self.secrets['redirect_uris']}'


    def load_secrets(self, secrets_file: str) -> dict[str: str]:
        return json.loads(secrets_file.read_text())["installed"]


    """
    Gives back url for google authorisation
    """
    def authorise(self)->dict[str, str]:

        PARAMS = {
            "response_type":"code",
            "client_id": os.getenv('GOOGLE_KEY'),
            "redirect_uri":self.redirect_uri,
            "scope":" ".join(self.SCOPES),
            "state": self.state,
            "access_type":"offline",
        }

        url = f"{self.secrets['auth_uri']}?{urlencode(PARAMS)}"

        return url


    """
    Exchanges the autorization code for a access token to access the resource
    """
    def exchange_code(self, query:dict[str, str]):
        
        processed_query = self.process_query(query)

        if self.state != processed_query['state']:
            raise RuntimeError("Invalid state")
        
        code = processed_query['code']

        params = {
            "grant_type": "authorization_code",
            "client_id": os.getenv('GOOGLE_KEY'),
            "client_secret": os.getenv('GOOGLE_SECRET'),
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        url = self.secrets["token_uri"]
            
        return self.post_request(url, params)


    """
    Convert's query to dict and check for state and code
    """
    def process_query(self, query:dict[str, str])->dict[str: str]:
        process = query
        if 'state' not in process or 'code' not in process:
            raise ValueError("Invalid query parameters")
        return process
    

    """
    Get request function for every request
    """
    def get_request(self, url: str) -> dict:
        with requests.get(url) as response:
            if response.status_code != 200:
                raise RuntimeError("Request failed")
            return response.json()
    

    """
    Post request function for every request
    """
    def post_request(self, url: str, params: dict) -> dict:
        with requests.post(
            url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"}
        ) as response:
            if response.status_code != 200:
                raise RuntimeError('Request failed')
            return response.json()


    """
    Get's the info on the access token
    """
    def check_access_token(self, access_token: str)->dict[str, str]:
        url = f'{os.getenv("GOOGLE_TOKEN_INFO")}?access_token={access_token}'
        return self.get_request(url)


    """
    Get's new access token using the refreash token
    """
    def refresh_token(self, refresh_token: str)->dict[str, str]:
        params = {
            "grant_type": "refresh_token",
            "client_id": os.getenv('GOOGLE_KEY'),
            "client_secret": os.getenv('GOOGLE_SECRET'),
            "refresh_token": refresh_token
        }
        return self.post_request(self.secrets["token_uri"], params)


    """
    Function to get users credentials and info
    """
    def do_auth(self, access_token: str)->dict[str, str]:
        url = f"{os.getenv("GOOGLE_API")}?alt=json&access_token={access_token}"
            
        return self.get_request(url)

