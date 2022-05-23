import qqbot
from qqbot import MessageEmbed, MessageEmbedThumbnail, MessageEmbedField, CreateDirectMessageRequest

from service.robotService import RobotService
from util.weather import Weather


class SecretWeatherFind(RobotService):
    async def getSendContent(self, content):
        split = content.split("/私信天气")
        send_content = ''

        weather_dict = await Weather.get_weather(split[1].strip())
        if weather_dict['success'] == '0':
            weather_dict = {}
        return weather_dict

    async def sendMessage(self, message: qqbot.Message, dms_api: qqbot.AsyncDmsAPI, content):
        if content == {}:
            content = '您查询的不是城市哦!'
            await self.send_weather_embed_direct_message_default(dms_api, content, message.guild_id, message.author.id)
        else:
            await self.send_weather_embed_direct_message(dms_api, content, message.guild_id, message.author.id)

    async def send_weather_embed_direct_message(self, dms_api: qqbot.AsyncDmsAPI, content, guild_id, user_id):
        """
        被动回复-私信推送天气内嵌消息
        :param user_id: 用户ID
        :param weather_dict: 天气数据字典
        :param guild_id: 发送私信需要的源频道ID
        """
        # 构造消息发送请求数据对象
        embed = MessageEmbed()
        embed.title = content['result']['citynm'] + " " + content['result']['weather']
        embed.prompt = "天气消息推送"
        # 构造内嵌消息缩略图
        thumbnail = MessageEmbedThumbnail()
        thumbnail.url = content['result']['weather_icon']
        embed.thumbnail = thumbnail
        # 构造内嵌消息fields
        embed.fields = [MessageEmbedField(name="当日温度区间：" + content['result']['temperature']),
                        MessageEmbedField(name="当前温度：" + content['result']['temperature_curr']),
                        MessageEmbedField(name="最高温度：" + content['result']['temp_high']),
                        MessageEmbedField(name="最低温度：" + content['result']['temp_low']),
                        MessageEmbedField(name="当前湿度：" + content['result']['humidity'])]

        # 通过api发送回复消息
        send = qqbot.MessageSendRequest(embed=embed, content="")
        direct_message_guild = await dms_api.create_direct_message(CreateDirectMessageRequest(guild_id, user_id))
        await dms_api.post_direct_message(direct_message_guild.guild_id, send)

    async def send_weather_embed_direct_message_default(self, dms_api: qqbot.AsyncDmsAPI, content, guild_id, user_id):
        message_to_send = qqbot.MessageSendRequest(content=content)
        direct_message_guild = await dms_api.create_direct_message(
            CreateDirectMessageRequest(guild_id, user_id))
        await dms_api.post_direct_message(direct_message_guild.guild_id, message_to_send)
