from service.robotService import RobotService
from util.weather import Weather
import qqbot

class PublicWeatherFind(RobotService):
    async def getSendContent(self, content):
        split = content.split("/天气")
        send_content = ''

        weather_dict = await Weather.get_weather(split[1].strip())
        if weather_dict['success'] == '1':
            send_content = weather_dict['result']['citynm'] + " " + weather_dict['result']['weather'] + " " + \
                           weather_dict['result']['days'] + " " + weather_dict['result']['week']
        elif weather_dict['success'] == '0':
            send_content = '您输入的不是城市城市名字哦!'
        return send_content

    async def sendMessage(self, message: qqbot.Message, msg_api: qqbot.AsyncMessageAPI, content):
        message_to_send = qqbot.MessageSendRequest(msg_id = message.id, content = content)
        await msg_api.post_message(message.channel_id, message_to_send)

