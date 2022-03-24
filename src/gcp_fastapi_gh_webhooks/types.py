from enum import Enum
from typing import Optional
from pydantic import BaseModel


class RequestHeaders(BaseModel):
    """
    Headers sent by GitHub
    """

    #: Name of the event that triggered the delivery
    event_name: Optional[str]

    #: A GUID to identify the delivery
    delivery_guid: Optional[str]

    #: This header is sent if the webhook is configured with a secret.
    #: This is the HMAC hex digest of the request body, and is generated using
    #: the SHA-256 hash function and the secret as the HMAC key
    secret_hash: Optional[str]


class ActionType(str, Enum):
    CREATED = "created"

    EDITED = "edited"

    DELTED = "deleted"


class BranchProtectionRule(BaseModel):
    """
    Activity related to a branch protection rule.
    """

    #: The action performed
    action: ActionType


