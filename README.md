# qqRobot
# 方案设计

### 功能介绍

本项目在qq机器人背景下开发简易天气查询系统，可以在聊天频道使用指令/天气 + 城市 或者/私信天气 + 城市实现天气查询功能。

其中私信天气，可以让机器人解析到指令之后私发消息给消息发送者。

### 方案设计

使用qqbot.Handler()监听AT_MESSAGE_EVENT_HANDLER事件，完成@指令解析回调函数。其中指令回调函数使用简单工厂方法设计模式，方便对后续指令扩展。另外机器人私发消息使用embed消息模板，可以使用现成的消息样式模板。

系统整体流程图如图所示。

![image-20220524003039225](/Users/admin/Library/Application Support/typora-user-images/image-20220524003039225.png)

### 使用说明

1. 安装项目依赖

   ```python
   pip install qq-bot ，pip install pyyaml等模块运行项目
   
   python robot.py
   ```

2. 加入频道

   ```python
   https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=1W4DX25&businessType=9&nickName=Time&from=246610&biz=ka
   ```

3. 使用机器人

   ```pyt
   在频道聊天 | 交友子频道中@机器人或者输入指令 /天气或者/私信天气 唤醒机器人
   之后输入指令 /天气 城市名
   
   例如@问答机器人 /天气 深圳 完成天气查询
   ```

   

