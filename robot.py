import os.path
import qqbot

from qqbot.core.util.yaml_util import YamlUtil

from service.publicWeatherFind import PublicWeatherFind
from service.secretWeatherFind import SecretWeatherFind
from util.encrypt import Encrypt

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))
async def _message_handler(event, message: qqbot.Message):
    # 根据指令触发不同的推送消息
    content = message.content

    if "/天气" in content:
        service = PublicWeatherFind()
        send_content = await service.getSendContent(content)
        msg_api = qqbot.AsyncMessageAPI(t_token, False)
        await service.sendMessage(message, msg_api, content=send_content)
    elif "/私信天气" in content:
        service = SecretWeatherFind()
        send_content = await service.getSendContent(content)
        dms_api = qqbot.AsyncDmsAPI(t_token, False)
        await service.sendMessage(message, dms_api, content=send_content)


# async的异步接口的使用示例
if __name__ == "__main__":
    appidSecr = test_config["token"]["appid"]
    tokenSecr = test_config["token"]["token"]

    t_token = qqbot.Token(Encrypt.decrypt(appidSecr), Encrypt.decrypt(tokenSecr))
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)