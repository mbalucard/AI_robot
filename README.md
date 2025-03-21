# 项目说明
1. 此项目将飞书机器人与阿里千问自建模型连接，你可以配合阿里的RAG知识库，实现个人助理。
2. 飞书与阿里云百炼相关key及app_id获取方法，请参阅相关官方文档，这里不详细叙述。
3. customer_robot.py 为运行主文件
# 文件说明
1. sql_command为数据库相关操作与查询，这里使用的是mysql数据库
2. library为项目相关手写库，
    - llm使用的模型为千问智能体，可根据需要自行搭建,启动用key相关样例为：
    ```python
    class qanwen_manual:
        """ 千问大模型 """
        API_KEY = "sk-"
        APP_ID = ''
    ```
    - connect_sql为python操作数据库相关内容，需要配合相关数据库相关信息使用，以下为样例：
    ```python
    class MySQL:
        """个人mysql"""
        type = 'MySQL'
        user = ''
        password = r''
        ip = 'localhost:3306'
        database = ''
    ```
3. 启动文件为customer_robot,需要飞书相关机器人的key,设置样例如下
    ```python
    class FeiShu:
        """ 飞书app """
        APP_ID = ''
        APP_SECRET = ''
    ```
4. 调试运行code/debug_robot.py