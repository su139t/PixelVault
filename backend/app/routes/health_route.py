from flask import Blueprint

from app.controllers.health_controller import (
    db_test_controller,
    health_controller
)


health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.get("/health")
def health():
    return health_controller()


@health_bp.get("/db-test")
def db_test():
    return db_test_controller()
