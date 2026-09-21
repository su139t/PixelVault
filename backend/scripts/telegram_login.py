import asyncio

from app.services.telegram_service import login


async def main():
    client = await login()
    me = await client.get_me()
    print(me)


if __name__ == "__main__":
    asyncio.run(main())
