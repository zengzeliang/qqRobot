import asyncio
import json
import os.path
import threading
from typing import Dict, List

import aiohttp
import qqbot

from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.message import MessageEmbed, MessageEmbedField, MessageEmbedThumbnail, CreateDirectMessageRequest, \
    MessageArk, MessageArkKv, MessageArkObj, MessageArkObjKv

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))
async def _message_handler(event, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 根据指令触发不同的推送消息
    content = message.content
    if "/天气" in content:
        # 通过空格区分城市参数
        split = content.split("/天气 ")
        weather_dict = await get_weather(split[1])
        if weather_dict['success'] == '1':
            weather_desc = weather_dict['result']['citynm'] + " " + weather_dict['result']['weather'] + " " + weather_dict['result']['days'] + " " + weather_dict['result']['week']
        elif weather_dict['success'] == '0':
            weather_desc = '您查询的不是城市哦!'
        message_to_send = qqbot.MessageSendRequest(msg_id=message.id, content=weather_desc)
        await msg_api.post_message(message.channel_id, message_to_send)
    elif "/私信天气" in content:
        # 通过空格区分城市参数
        split = content.split("/私信天气 ")
        weather_dict = await get_weather(split[1])
        if weather_dict['success'] == '1':
            await send_weather_embed_direct_message(weather_dict, message.guild_id, message.author.id)
        elif weather_dict['success'] == '0':
            weather_desc = '您查询的不是城市哦!'
            await send_weather_embed_direct_message_excep(weather_desc, message)

async def get_weather(city_name: str) -> Dict:
    """
    获取天气信息
    :return: 返回天气数据的json对象
    返回示例
    {
    "success":"1",
    "result":{
        "weaid":"1",
        "days":"2022-03-04",
        "week":"星期五",
        "cityno":"beijing",
        "citynm":"北京",
        "cityid":"101010100",
        "temperature":"13℃/-1℃",
        "temperature_curr":"10℃",
        "humidity":"17%",
        "aqi":"98",
        "weather":"扬沙转晴",
        "weather_curr":"扬沙",
        "weather_icon":"http://api.k780.com/upload/weather/d/30.gif",
        "weather_icon1":"",
        "wind":"西北风",
        "winp":"4级",
        "temp_high":"13",
        "temp_low":"-1",
        "temp_curr":"10",
        "humi_high":"0",
        "humi_low":"0",
        "weatid":"31",
        "weatid1":"",
        "windid":"7",
        "winpid":"4",
        "weather_iconid":"30"
        }
    }
    """
    weather_api_url = "http://api.k780.com/?app=weather.today&cityNm=" + city_name + "&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=weather_api_url,
                timeout=5,
        ) as resp:
            content = await resp.text()
            content_json_obj = json.loads(content)
            return content_json_obj

async def send_weather_embed_direct_message_excep(weather_desc, message:qqbot.Message):
    dms_api = qqbot.AsyncDmsAPI(t_token, False)
    message_to_send = qqbot.MessageSendRequest(msg_id=message.id, content=weather_desc)
    direct_message_guild = await dms_api.create_direct_message(CreateDirectMessageRequest(message.guild_id, message.author.id))
    await dms_api.post_direct_message(direct_message_guild.guild_id, message_to_send)


async def send_weather_embed_direct_message(weather_dict, guild_id, user_id):
    """
    被动回复-私信推送天气内嵌消息
    :param user_id: 用户ID
    :param weather_dict: 天气数据字典
    :param guild_id: 发送私信需要的源频道ID
    """
    # 构造消息发送请求数据对象
    embed = MessageEmbed()
    embed.title = weather_dict['result']['citynm'] + " " + weather_dict['result']['weather']
    embed.prompt = "天气消息推送"
    # 构造内嵌消息缩略图
    thumbnail = MessageEmbedThumbnail()
    thumbnail.url = weather_dict['result']['weather_icon']
    embed.thumbnail = thumbnail
    # 构造内嵌消息fields
    embed.fields = [MessageEmbedField(name="当日温度区间：" + weather_dict['result']['temperature']),
                    MessageEmbedField(name="当前温度：" + weather_dict['result']['temperature_curr']),
                    MessageEmbedField(name="最高温度：" + weather_dict['result']['temp_high']),
                    MessageEmbedField(name="最低温度：" + weather_dict['result']['temp_low']),
                    MessageEmbedField(name="当前湿度：" + weather_dict['result']['humidity'])]

    # 通过api发送回复消息
    send = qqbot.MessageSendRequest(embed=embed, content="")
    dms_api = qqbot.AsyncDmsAPI(t_token, False)
    direct_message_guild = await dms_api.create_direct_message(CreateDirectMessageRequest(guild_id, user_id))
    await dms_api.post_direct_message(direct_message_guild.guild_id, send)
    qqbot.logger.info("/私信推送天气内嵌消息 成功")



# async的异步接口的使用示例
if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)