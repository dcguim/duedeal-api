from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
import httpx
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
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
    Validate the Google access token with Google's /tokeninfo endpoint.
    """
    url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}"
    response = requests.get(url)
#    async with httpx.AsyncClient() as client:
#        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return response.json()

def create_jwt_access_token(data: dict):
    """Create an access token."""
    to_encode = data.copy()
    expire = (datetime.utcnow()
              + timedelta(minutes=load_dotenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode,
                      load_dotenv("JWT_SECRET_KEY"),
                      algorithm=load_dotenv("ALGORITHM"))

def decode_jwt_token(token: str):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token,
                             load_dotenv("JWT_SECRET_KEY"),
                             algorithms=load_dotenv("ALGORITHM"))
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


http_bearer = HTTPBearer()

async def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """
    Authenticate a user via a Google access token or an internal JWT.
    """
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only 'Bearer' authentication scheme is supported",
        )
    token = credentials.credentials
    # First, attempt Google access token validation
    try:
        google_user = await validate_google_access_token(token)
        return {
            "auth_type": "google",
            "user_id": google_user["sub"],  # Google user ID
            "email": google_user["email"],
        }
    except HTTPException:
        pass  # If Google validation fails, fall back to internal JWT

    # Attempt internal JWT validation
    payload = decode_jwt_token(token)
    return {
        "auth_type": "internal",
        "user_id": payload.get("sub"),  # Internal user ID
        "email": payload.get("email"),
    }
