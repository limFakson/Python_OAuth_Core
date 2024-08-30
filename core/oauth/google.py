import os
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import parse_qsl, urlencode

# Load environment variables from a .env file
load_dotenv()

"""
Module for Google OAUTH python package for third party application
"""

class GoogleOauth:

    def __init__(self, secrets_file: dict[str,str]):
        """
        Initialize the GoogleOauth class with a secrets file containing Google API credentials.

        :param secrets_file: A dictionary containing Google API credentials
        """

        self.SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
        self.secrets = secrets_file["google"]
        self.state = hashlib.sha256(os.urandom(1024)).hexdigest()
        self.port = 8000
        self.redirect_uri = f'{self.secrets['redirect_uris']}'


    """
    Gives back url for google authorisation
    """
    def authorise(self)->dict[str, str]:
        """
        Generate a URL for Google authorization.

        :return: A dictionary containing the authorization URL
        """
         
        PARAMS = {
            "response_type":"code",
            "client_id": os.getenv('GOOGLE_KEY'),
            "redirect_uri":self.redirect_uri,
            "scope":" ".join(self.SCOPES),
            "state": self.state,
            "access_type":"offline",
        }
        if "status" in self.secrets and self.secrets["status"] == "test":
            PARAMS["prompt"] = "consent"

        url = f"{self.secrets['auth_uri']}?{urlencode(PARAMS)}"

        return url


    def exchange_code(self, query:dict[str, str]):
        """
        Exchange the authorization code for an access token.

        :param query: A dictionary containing the authorization code and state
        :return: A dictionary containing the access token
        """
        
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
    

    def get_request(self, url: str) -> dict:
        """
        Send a GET request to the specified URL.

        :param url: The URL to send the GET request to
        :return: A dictionary containing the response
        """
        with requests.get(url) as response:
            if response.status_code != 200:
                raise RuntimeError("Request failed")
            return response.json()
    

    def post_request(self, url: str, params: dict) -> dict:
        """
        Send a POST request to the specified URL with the specified parameters.

        :param url: The URL to send the POST request to
        :param params: A dictionary containing the request parameters
        :return: A dictionary containing the response
        """
        with requests.post(
            url, data=params, headers={"Content-type": "application/x-www-form-urlencoded"}
        ) as response:
            if response.status_code != 200:
                raise RuntimeError('Request failed')
            return response.json()


    def check_access_token(self, access_token: str)->dict[str, str]:
        """
        Check the access token and retrieve user information.

        :param access_token: The access token to check
        :return: A dictionary containing the user information
        """

        url = f'{os.getenv("GOOGLE_TOKEN_INFO")}?access_token={access_token}'
        return self.get_request(url)


    def refresh_token(self, refresh_token: str)->dict[str, str]:
        """
        Refresh the access token using the refresh token.
        """
        params = {
            "grant_type": "refresh_token",
            "client_id": os.getenv('GOOGLE_KEY'),
            "client_secret": os.getenv('GOOGLE_SECRET'),
            "refresh_token": refresh_token
        }
        return self.post_request(self.secrets["token_uri"], params)


    def do_auth(self, access_token: str)->dict[str, str]:
        """
        Get users credentials and info for authentication into your application
        """
        url = f"{os.getenv("GOOGLE_API")}?alt=json&access_token={access_token}"
            
        return self.get_request(url)

