import os
from typing import Optional

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
