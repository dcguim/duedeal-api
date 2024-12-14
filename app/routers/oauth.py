# routes/auth.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.utils.auth_flow_manager import GoogleOAuthFlow

router = APIRouter(
    prefix="/oauth2",
    tags=["oauth2"]
)
oauth_flow = GoogleOAuthFlow()

@router.get("/auth-url")
def get_auth_url():
    """
    Endpoint to generate and return the Google OAuth authorization URL.
    """
    try:
        auth_url = oauth_flow.get_authorization_url()
        return JSONResponse(status_code=200, content={"auth_url": auth_url})
    except Exception as e:
        # Log the error (use a logging library in production)
        print(f"Error generating auth URL: {str(e)}")
        return JSONResponse({"error": "Failed to generate authorization URL. Please try again later."},
                            status_code=500)

@router.get("/callback")
async def callback(request: Request):
    """
    Google OAuth callback endpoint to handle redirection after authentication.
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")
    try:
        credentials = oauth_flow.exchange_code_for_tokens(code)
        # Optionally, serialize and save the credentials
        tokens = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_in": credentials.expiry.isoformat(),
        }
        return JSONResponse({"tokens": tokens})
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
