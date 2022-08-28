import json

import aiohttp


async def get_questions():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/questions/') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            raw = await response.text()
            return json.loads(raw)


async def set_questions(title: str, answer: str, user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/api/questions/',
                                json={"title": title, "answer": answer, "user_id": user_id},
                                ) as response:
            return await response.text()


async def get_data_by_id(id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/questions/{id}/') as response:
            raw = await response.text()
            return json.loads(raw)
