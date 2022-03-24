from typing import Optional

from fastapi import Depends, HTTPException, Header, Request, status
import hmac
import hashlib
from gcp_fastapi_gh_webhooks.constants import WEBHOOK_SECRET

from gcp_fastapi_gh_webhooks.types import RequestHeaders


def get_headers(
    x_gitHub_event: Optional[str] = Header(None),
    x_github_delivery: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
):
    if x_hub_signature_256:
        x_hub_signature_256 = x_hub_signature_256.strip("sha256=")
    return RequestHeaders(
        event_name=x_gitHub_event,
        delivery_guid=x_github_delivery,
        secret_hash=x_hub_signature_256,
    )


async def auth_with_secret(
    request: Request,
    headers: RequestHeaders = Depends(get_headers),
):
    """
    Authenticate the webhook request using the webhook's secret
    """
    if not headers.secret_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing secret hash",
        )

    body = await request.body()
    signature = hmac.new(
        WEBHOOK_SECRET,
        msg=body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if (signature.lower() != headers.secret_hash.lower()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret hash",
        )
