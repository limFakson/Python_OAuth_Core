# OAuth_Core_Lib
A Python library for handling OAuth authentication, designed for use in third-party applications. This package simplifies the process of obtaining authorization from Google, exchanging authorization codes for access tokens, refreshing access tokens, and retrieving user information.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
  - [Create a JSON Secrets File]
  - [Set Up Environment Variables]
- [Usage](#usage)
  - [Initialize the GoogleOauth Class](#initialize-the-googleoauth-class)
  - [Authorize URL](#authorize-url)
  - [Exchange Authorization Code](#exchange-authorization-code)
  - [Check Access Token](#check-access-token)
  - [Refresh Access Token](#refresh-access-token)
  - [Get User Information](#get-user-information)
- [Contribution](#contributing)
- [License](#license)

## Installation

To install the library, run:

```bash
pip install oauth-core-lib
```

## Setup

Create a JSON Secrets File and add the following:

```json
{
  "core": {
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "redirect_uris": "your_redirect_uri"
  }
}
````

Set Up Environment Variables
Create a .env file in your project root directory with the following contents, the package will get the variables needed itself.
```text
GOOGLE_KEY=your_client_id
GOOGLE_SECRET=your_client_secret
GOOGLE_TOKEN_INFO=google_token_info_api
GOOGLE_API=google_api
```

## Usage

# Initialize the GoogleOauth Class
```python
from core.google_oauth_google import GoogleOauth

secrets_file = Path('your_json_file.json')
oauth = GoogleOauth(secrets_file)
```

# Authorize URL
Generate the URL to redirect users to Google for authorization

```python 
auth_url = oauth.authorise()
```
- Returns: A URL string where users will be redirected to authorize your application

# Exchange Authorization Code
Once the user is redirected back to your application, capture the query parameters (which include the authorization code) and exchange them for an access token (it takes in only dict)

```python
query_params = {'code': 'authorization_code', 'state': 'your_state'} # query gotten from the redirect uri converted to dictionary
tokens = oauth.exchange_code(query_params)
```
- Returns: A dictionary containing:
  `access_token`: The token to authenticate API requests.
  `expires_in`: The remaining lifetime of the access token (in seconds).
  `refresh_token`: A token to obtain a new access token when the current one expires.
  `scope`: The scope of access granted by the user.
  `token_type`: The type of token issued (typically "Bearer").

# Check Access Token(optional)
Check if the access token is still valid

```python
token_info = oauth.check_access_token(tokens['access_token'])
```
- Returns: A dictionary containing:
  `aud`: The client ID to which the token was issued.
  `user_id`: The unique ID of the authenticated user.
  `scope`: The scope associated with the token.
  `expires_in`: The number of seconds remaining before the token expires.

# Refresh Access Token
If the access token has expired, use the refresh token to get a new one
note: refreash token does not come the second time

```python
refreshed_tokens = oauth.refresh_token(tokens['refresh_token'])
```
- Returns: A dictionary similar to the one returned by `exchange_code`, but without a new `refreash_token`.

# Get User Information
Retrieve the authenticated user's information using the access token

```python
user_info = oauth.do_auth(tokens['access_token'])
```

- Returns: A dictionary containing:
  `id`: The user's Google ID.
  `email`: The user's email address.
  `verified_email`: A boolean indicating whether the email address is verified.
  `name`: The user's full name.
  `given_name`: The user's first name.
  `family_name`: The user's last name.
  `picture`: The URL of the user's profile picture.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bug fixes or enhancements.

## License

This project is licensed under the MIT License.