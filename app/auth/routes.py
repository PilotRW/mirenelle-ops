from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.auth.middleware import build_dev_user
from app.auth.permissions import normalize_roles, permissions_for_roles
from app.config.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def oidc_client(request: Request):
    from authlib.integrations.starlette_client import OAuth

    if not all([settings.AUTH_ISSUER, settings.AUTH_CLIENT_ID, settings.AUTH_CLIENT_SECRET]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OIDC auth is enabled but issuer/client settings are incomplete",
        )

    oauth = OAuth()
    oauth.register(
        name="oidc",
        client_id=settings.AUTH_CLIENT_ID,
        client_secret=settings.AUTH_CLIENT_SECRET,
        server_metadata_url=f"{settings.AUTH_ISSUER.rstrip('/')}/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile groups"},
    )
    return oauth.create_client("oidc")


def user_from_claims(claims: dict) -> dict:
    groups = claims.get(settings.AUTH_GROUPS_CLAIM, []) or []
    if isinstance(groups, str):
        groups = [groups]
    roles = normalize_roles(groups)
    return {
        "email": claims.get("email") or claims.get("preferred_username") or claims.get("sub"),
        "name": claims.get("name") or claims.get("email") or claims.get("preferred_username"),
        "roles": roles,
        "permissions": permissions_for_roles(roles),
        "auth_mode": "oidc",
    }


@router.get("/login")
async def login(request: Request):
    if not settings.AUTH_ENABLED:
        return RedirectResponse(url="/ui/", status_code=303)

    client = oidc_client(request)
    redirect_uri = settings.AUTH_REDIRECT_URI or str(request.url_for("auth_callback"))
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="auth_callback")
async def callback(request: Request):
    if not settings.AUTH_ENABLED:
        return RedirectResponse(url="/ui/", status_code=303)

    client = oidc_client(request)
    token = await client.authorize_access_token(request)
    claims = token.get("userinfo") or await client.userinfo(token=token)
    user = user_from_claims(dict(claims))
    if not user["roles"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No authorized Mirenelle role found in OIDC groups",
        )
    request.session["user"] = user
    return RedirectResponse(url="/ui/", status_code=303)


@router.post("/logout")
async def logout(request: Request):
    if not settings.AUTH_ENABLED:
        return RedirectResponse(url="/auth/login", status_code=303)

    request.session.clear()
    query = urlencode({"post_logout_redirect_uri": str(request.url_for("login"))})
    return RedirectResponse(
        url=f"{settings.AUTH_ISSUER.rstrip('/')}/end-session/?{query}",
        status_code=303,
    )


@router.get("/me")
async def me(request: Request):
    if not settings.AUTH_ENABLED:
        return build_dev_user()

    user = request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user
