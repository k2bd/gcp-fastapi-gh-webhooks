import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gcp_fastapi_gh_webhooks.dependencies import auth_with_secret

from gcp_fastapi_gh_webhooks.types import ExampleResponse

logger = logging.getLogger(__name__)

app = FastAPI(dependencies=[Depends(auth_with_secret)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/example/{exampleValue}", response_model=ExampleResponse)
async def say_hello(exampleValue: str):
    logger.info(f"GET /example/{exampleValue}")
    return ExampleResponse(response_value=exampleValue.upper())
