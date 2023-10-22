import uvicorn
from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.postgres.database import setup_database
from src.routers.service import service_router
from src.routers.dashboard import dashboard_router
from src.routers.metrics import metrics_router
from src.utils.metrics import update_metrics


def get_app() -> FastAPI:
    setup_database()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(service_router)
    app.include_router(dashboard_router)
    app.include_router(metrics_router)

    update_metrics()

    return app


app = get_app()


def main():
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
