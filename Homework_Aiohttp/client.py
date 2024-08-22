import asyncio
import aiohttp


async def get_request():
    session = aiohttp.ClientSession()
    response = await session.get(
        "http://127.0.0.1:7000/ad/1/",)

    print(response.status)
    print(await response.json())
    await session.close()


async def post_request():
    session = aiohttp.ClientSession()
    response = await session.post(
        "http://127.0.0.1:7000/ad/",
        json={'title': 'title_1', 'description': 'description_1', 'owner': 'user_1', },

    )
    print(response.status)
    print(await response.json())
    await session.close()


async def update_request():
    session = aiohttp.ClientSession()
    response = await session.patch(
        "http://127.0.0.1:7000/ad/1/",
        json={'title': 'new_title_1', 'description': 'new_description_1', 'owner': 'new_user_1', },

    )
    print(response.status)
    print(await response.json())
    await session.close()


async def delete_request():
    session = aiohttp.ClientSession()
    response = await session.delete(
        "http://127.0.0.1:7000/ad/1/",


    )
    print(response.status)
    print(await response.json())
    await session.close()

asyncio.run(post_request())
asyncio.run(get_request())
asyncio.run(update_request())
asyncio.run(delete_request())
