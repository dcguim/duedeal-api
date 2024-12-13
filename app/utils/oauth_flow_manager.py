from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import requests
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

load_dotenv()

class GoogleOAuthFlow:
    def __init__(self):        
        self.flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "redirect_uris": [os.getenv("REDIRECT_URI")],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid"
            ]
        )
        self.flow.redirect_uri = os.getenv("REDIRECT_URI")

    def get_authorization_url(self):
        """Generate the Google OAuth authorization URL."""
        authorization_url, _ = self.flow.authorization_url(prompt="consent",
                                                           access_type="offline")
        return authorization_url

    def exchange_code_for_tokens(self, code):
        """Exchange the authorization code for access and refresh tokens."""
        try:
            self.flow.fetch_token(code=code)
            return self.flow.credentials
        except Exception as e:
            raise ValueError(f"Token exchange failed: {str(e)}")

async def validate_google_access_token(access_token: str):
    """
    Validate the access token with Google's tokeninfo endpoint
    """
    url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token"
        )
    token_info = response.json()
    return token_info

http_bearer = HTTPBearer()

async def get_user_creds(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """
    Utility function for extracting the credentials and ensuring bearer
    """
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only 'Bearer' authentication scheme is supported",
        )
    token = credentials.credentials  # Extract the Bearer token
    token_info = await validate_google_access_token(token)
    if not token_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return token_info
