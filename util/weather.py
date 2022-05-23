import aiohttp
from typing import Dict
import json


class Weather:
    @staticmethod
    async def get_weather(city_name: str) -> Dict:
        weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=weather_api_url,
                    timeout=5,
            ) as resp:
                content = await resp.text()
                content_json_obj = json.loads(content)
                return content_json_obj
