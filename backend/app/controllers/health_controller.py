from app.services.health_service import check_database_connection
from app.utils.responses import success_response


def health_controller():
    return success_response({
        "project": "PixelVault"
    })


def db_test_controller():
    return success_response(check_database_connection())
