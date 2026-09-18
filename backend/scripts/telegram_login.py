from app.services.telegram_service import login


if __name__ == "__main__":
    client = login()
    print(client.get_me())
