from fastapi import APIRouter
from fastapi import Request, Response
from prometheus_client.exposition import generate_latest, CONTENT_TYPE_LATEST

metrics_router = APIRouter()


@metrics_router.get("/metrics")
def metrics(request: Request) -> Response:
    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})
