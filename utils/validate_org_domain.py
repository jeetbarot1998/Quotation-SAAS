from functools import wraps
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import Optional, Callable

from auth.security import verify_token
from database.dependencies import get_db
from models import Organization
from schemas.user import TokenData


def validate_org_domain():
    """
    Decorator that wraps endpoints to validate organization domain against token.
    Must be used after token verification.
    """

    # TODO: use request.state instead of extracting the host again and DB call.
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
                request: Request,
                token_data: TokenData = Depends(verify_token),
                db: Session = Depends(get_db),
                *args,
                **kwargs
        ):
            try:
                # Get user organization from database by org id in token
                organization = db.query(Organization).filter_by(id=token_data.org_id).first()
                if not organization:
                    raise HTTPException(
                        status_code=401,
                        detail="Organization not found"
                    )

                # Get and validate subdomain from request
                # host = request.headers.get('host', '')
                # request_subdomain = get_subdomain(host)
                #
                # if not request_subdomain:
                #     raise HTTPException(
                #         status_code=400,
                #         detail="Invalid subdomain"
                #     )

                # Verify subdomain matches organization
                # if request_subdomain != organization.subdomain:
                #     raise HTTPException(
                #         status_code=401,
                #         detail="Organization mismatch"
                #     )

                # verify if the user who is requesting has the same or id
                # as the org id of the subdomain set in the state of the request
                # in the middleware
                if organization.id != request.state.org_id:
                    raise HTTPException(
                        status_code=401,
                        detail="Organization mismatch"
                    )

                # If all validations pass, call the original function
                return await func(request=request, token_data=token_data, db=db, *args, **kwargs)

            except Exception as e:
                raise HTTPException(
                    status_code=401,
                    detail=str(e)
                )

        return wrapper

    return decorator


def get_subdomain(host: str):
    try:
        # Handle localhost
        if 'localhost' in host:
            host = host.split(':')[0]
            parts = host.split('.')
            if parts[0] == 'localhost':
                return 'default'  # Use 'default' for localhost without subdomain
            return parts[0] if len(parts) > 1 else None

        # Handle production domain
        parts = host.split('.')
        if len(parts) > 2:
            return parts[0]
        elif len(parts) == 2:
            return 'default'  # Use 'default' for main domain without subdomain

        return None

    except Exception as e:
        print(f"Error parsing subdomain: {e}")  # Add logging
        return None