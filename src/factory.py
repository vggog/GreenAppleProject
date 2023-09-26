from fastapi import FastAPI

from src.view import router


class AppFactory:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI()
        cls._append_routes(app)
        return app

    @staticmethod
    def _append_routes(app: FastAPI):
        app.include_router(router)
