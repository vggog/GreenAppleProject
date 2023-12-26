from fastapi import FastAPI

from src.customer.views import router as customer_router
from src.admin.views import router as admin_router
from src.master.view import router as master_router


class AppFactory:

    @classmethod
    def create_app(cls) -> FastAPI:
        app = FastAPI()
        cls._append_routes(app)
        return app

    @staticmethod
    def _append_routes(app: FastAPI):
        app.include_router(customer_router)
        app.include_router(admin_router)
        app.include_router(master_router)


