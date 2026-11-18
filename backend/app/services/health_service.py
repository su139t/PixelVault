from app.repositories.health_repository import get_database_details


def check_database_connection():
    result = get_database_details()

    return {
        "database": result[0],
        "user": result[1],
        "postgresql_version": result[2]
    }
