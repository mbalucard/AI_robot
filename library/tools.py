import datetime
import pandas as pd



def time_conversion(time_str: str):
    """
    将给定的时间戳字符串转换为格式化的日期时间字符串。

    :param time_str: 需要转换的时间戳字符串
    :type time_str: str
    :returns: 格式化后的日期时间字符串，格式为 '%Y-%m-%d %H:%M:%S'
    :rtype: str
    :raises ValueError: 如果输入的字符串无法转换为整数
    """
    second = int(time_str) / 1000.0
    formatted_time = datetime.datetime.fromtimestamp(second).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def to_table(user_content: str, assistant_content: str, millisecond: str, open_id: str, message_id: str):
    """
    将用户和助手的对话内容、时间戳等信息转换为Pandas DataFrame格式。

    :param user_content: 用户发送的内容，类型为str
    :param assistant_content: 助手回复的内容，类型为str
    :param millisecond: 毫秒级时间戳，类型为str
    :param open_id: 用户唯一标识符，类型为str
    :param message_id: 消息唯一标识符，类型为str
    :returns: 包含对话信息的Pandas DataFrame
    :rtype: pd.DataFrame
    """
    date_time = time_conversion(millisecond)
    massage = {"open_id": open_id, "message_id": message_id, "user": user_content, "assistant": assistant_content,
               "create_time": date_time}
    df = pd.DataFrame([massage])
    return df


def messages_id_query(service):
    """ 查询今天所有消息的message_id """
    sql_command = """select message_id from feishu_chat
where DATE_FORMAT(STR_TO_DATE(create_time, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d') = DATE_FORMAT(NOW(), '%Y-%m-%d');"""
    mes_list = service.get_data(sql_command)
    return mes_list['message_id'].tolist()
