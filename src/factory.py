from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.customer.views import router as customer_router
from src.admin.views import router as admin_router
from src.master.view import router as master_router

from src.core.config import load_config


class AppFactory:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI()
        cls._append_routes(app)
        cls._append_origins(app)
        return app

    @staticmethod
    def _append_routes(app: FastAPI):
        app.include_router(customer_router)
        app.include_router(admin_router)
        app.include_router(master_router)

    @staticmethod
    def _append_origins(app: FastAPI):
        origins = load_config().project_setup.origins

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
