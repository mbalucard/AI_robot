import lark_oapi as lark
import json
from lark_oapi.api.im.v1 import *
from cachetools import TTLCache
from users.user import FeiShu, MySQL
from library.connect_sql import CallMySQL
from library.tools import messages_id_query, to_table
from library.llm import qanwen

app = FeiShu
server = MySQL

cache = TTLCache(maxsize=300, ttl=600)
service = CallMySQL(server)
table_name = "feishu_chat"


# 注册接收消息事件，处理接收到的消息。
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    res_content = ""
    if data.event.message.message_type == "text":
        res_content = json.loads(data.event.message.content)["text"]  # 获取问题内容

        mes_id = data.event.message.message_id  # 确定聊天ID
        open_id = data.event.sender.sender_id.open_id  # 确定用户
        time_con = data.header.create_time  # 确定创建时间
        # 判断是否重复请求
        # 利用缓存去重
        if mes_id in cache:
            print(f"{mes_id}缓存重复请求被忽略")
            return
        cache[mes_id] = True  # 将该组合加入缓存
        # 利用数据库表去重
        mes_list = messages_id_query(service)
        if mes_id in mes_list:
            print(f"{mes_id}数据库重复请求被忽略")
            return
        # 调取模型回复
        result = qanwen(res_content)
        # 消息存表
        session_record = to_table(res_content, result, time_con, open_id, mes_id)
        service.to_sql(session_record, table_name, exists="append")
    else:
        result = "解析消息失败，请发送文本消息\nparse message failed, please send text message"
    # 编辑回复格式
    content = json.dumps(
        {"text": "收到你发送的消息：" + res_content
                 + "\n回复:" + result}
    )

    # 如果是单聊（p2p），则调用发送消息接口向对应用户发送消息
    if data.event.message.chat_type == "p2p":
        request: CreateMessageRequest = (
            CreateMessageRequest.builder()
            .receive_id_type("chat_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(data.event.message.chat_id)
                .msg_type("text")
                .content(content)
                .build()
            )
            .build()
        )
        # 使用OpenAPI发送消息
        response: CreateChatResponse = client.im.v1.chat.create(request)

        if not response.success():
            raise Exception(
                f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )
    # 如果是群聊，则调用回复消息接口，回复用户在群组内 @机器人的消息
    else:
        request: ReplyMessageRequest = (
            ReplyMessageRequest.builder()
            .message_id(data.event.message.message_id)
            .request_body(
                ReplyMessageRequestBody.builder()
                .content(content)
                .msg_type("text")
                .build()
            )
            .build()
        )
        # 使用OpenAPI回复消息
        response: ReplyMessageResponse = client.im.v1.message.reply(request)
        if not response.success():
            raise Exception(
                f"client.im.v1.message.reply failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )


# 注册事件回调
event_handler = (
    lark.EventDispatcherHandler.builder("", "")  # 加密密钥，验证令牌
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)

# 创建 LarkClient 对象，用于请求OpenAPI, 并创建 LarkWSClient 对象，用于使用长连接接收事件。
client = lark.Client.builder().app_id(app.APP_ID).app_secret(app.APP_SECRET).build()
wsClient = lark.ws.Client(
    app.APP_ID,
    app.APP_SECRET,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)


def main():
    #  启动长连接，并注册事件处理器。
    #  Start long connection and register event handler.
    wsClient.start()


if __name__ == "__main__":
    main()
