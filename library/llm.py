# 自定义模型调用
from http import HTTPStatus
from dashscope import Application
from users.user import qanwen_manual

qwen = qanwen_manual


def qanwen(massages: str):
    """
    通过阿里千问大模型，反馈结果
    :param massages: 问题
    :return:
    """
    response = Application.call(
        # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        api_key=qwen.API_KEY,
        app_id=qwen.APP_ID,
        prompt=massages)

    if response.status_code != HTTPStatus.OK:  # 调用失败的情况
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        return response.message
    else:  # 调用成功的情况
        # print(response.output.text)
        return response.output.text


if __name__ == '__main__':
    mas = '你是谁？'
    result = qanwen(mas)
    print(result)
