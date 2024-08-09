import asyncio
from app import create_app


async def main():
    app = await create_app()
    app.run(debug=True, port=5001)


if __name__ == "__main__":
    asyncio.run(main())

