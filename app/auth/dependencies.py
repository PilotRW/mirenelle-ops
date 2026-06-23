from collections.abc import Callable

from fastapi import HTTPException, Request, status

from app.auth.permissions import has_permission


def current_user(request: Request) -> dict:
    user = getattr(request.state, "user", None) or request.session.get("user")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


def require_permission(permission: str) -> Callable[[Request], dict]:
    def dependency(request: Request) -> dict:
        user = current_user(request)
        if not has_permission(user.get("permissions", []), permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission}",
            )
        return user

    return dependency
