from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os

class GoogleOAuthFlow:
    def __init__(self):
        load_dotenv()
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
        authorization_url, _ = self.flow.authorization_url(prompt="consent", access_type="offline")
        return authorization_url

    def exchange_code_for_tokens(self, code):
        """Exchange the authorization code for access and refresh tokens."""
        self.flow.fetch_token(code=code)
        return self.flow.credentials
