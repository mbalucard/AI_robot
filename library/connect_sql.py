import pandas as pd
from sqlalchemy import create_engine, text

pd.set_option('display.unicode.east_asian_width', True)


def read_sql_language(sql_path):
    """
    读取路径下文件内容
    :param sql_path: 文件路径
    :return: 文本格式命令
    """
    with open(sql_path, 'r', encoding='utf-8') as open_file:
        sql_language = open_file.read()
    return sql_language


class CallSQL:
    """
    调用SQLServer数据库
    """

    def __init__(self, server):
        """
        :param server: 服务器连接方式,类型class
        """
        self.sql = server
        method = 'mssql+pymssql'
        self.conn_parameter = f"{method}://{self.sql.user}:{self.sql.password}@{self.sql.ip}/{self.sql.database}?charset=utf8"

    def get_data(self, sql_command):
        """
        根据语句获取数据
        :param sql_command: 数据库执行命令
        :return DataFrame
        """
        engine = create_engine(self.conn_parameter, echo=False)
        with engine.connect() as conn:
            data = pd.read_sql(text(sql_command), con=conn)  # 这里使用text方法，用来去除命令当中特殊符号的影响
        return data

    def implement(self, sql_command):
        """
        根据语句对数据库进行操作
        :param sql_command: 数据库执行命令
        """
        engine = create_engine(self.conn_parameter, echo=False)
        with engine.connect() as con:
            con.execute(sql_command)
        print('Mission accomplished!')

    def to_sql(self, data_frame, table_name, exists='fail', size=None):
        """
        将DataFrame插入至数据库
        :param data_frame: 传入数据表，DataFrame格式数据
        :param table_name: 库表名称
        :parameter exists: 如果表名称存在则报错(fail)，可改为：replace替换、append追加
        :parameter size: 一次传入的行数，默认是None为所有行
        :return: sql data
        """
        engine = create_engine(self.conn_parameter, echo=False)
        data_frame.to_sql(table_name, engine, index=False, if_exists=exists, chunksize=size)
        # print(f'{table_name} 表已添加至 {self.sql.database}')


# 用继承法继承CallSQL
class CallMySQL(CallSQL):
    """
    调用MySQL数据库
    """

    def __init__(self, server):
        """
        :param server: 服务器连接方式
        """
        super().__init__(server)
        method = 'mysql+pymysql'
        self.conn_parameter = f"{method}://{self.sql.user}:{self.sql.password}@{self.sql.ip}/{self.sql.database}?charset=utf8"


if __name__ == '__main__':
    from users.user import MySQL

    sql_command = """select message_id from feishu_chat
    where DATE_FORMAT(STR_TO_DATE(create_time, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d') = DATE_FORMAT(NOW(), '%Y-%m-%d');"""

    server = CallMySQL(MySQL)
    data = server.get_data(sql_command)
    print(data)
