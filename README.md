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
