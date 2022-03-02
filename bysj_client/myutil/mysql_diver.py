import pymysql


class mysql_diver:
    """
    - 具有增删改查的功能
    - 首先看 self.status 是否为 True ,是的话表示连接数据库成功
    - 增：add_one(sql_str, value_list)
    - 增：add_many(sql_str, value_list)
    - 删和改:update_or_delete_one(sql_str, value_list)
    - 查：get_find_list(sql_str, value_list)
    """

    def __init__(self, host, port, user, password, database="sys"):
        """
        :param host:  str host
        :param port:  int port
        :param user:  str user
        :param password:  str password
        :param database:  str database
        """
        self.host = str(host)
        self.port = int(port)
        self.user = str(user)
        self.password = str(password)
        self.database = str(database)
        self.charset = 'utf8'
        self.status = False
        self.__test_connect()

    def __test_connect(self):
        res = self.get_find_list(sql_str='show tables;')
        if len(res) != 0:
            try:
                if res[0]['info'] == 'error':
                    self.status = False
            except:
                self.status = True
        self.status = True

    def __get_conn(self):
        return pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset=self.charset)

    def add_one(self, sql_str, value_list):
        """
        :param sql_str: 例如 -> "INSERT INTO USER1(name, age) VALUES (%s, %s);"
        :param value_list: 例如 -> ["Alex", 18]
        :return: 获取刚插入的数据的ID 或者 'error'
        """
        # 连接database
        conn = self.__get_conn()
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql_str, value_list)
            # 提交事务
            conn.commit()
            # 提交之后，获取刚插入的数据的ID
            last_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return last_id
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
            cursor.close()
            conn.close()
            return 'error'

    def add_many(self, sql_str, value_list_tuple):
        """
        :param sql_str: 例如 -> "INSERT INTO USER1(name, age) VALUES (%s, %s);"
        :param value_list_tuple: 例如 -> [("Alex", 18), ("Egon", 20), ("Yuan", 21)]
        :return: True or Flase
        """
        # 连接database
        conn = self.__get_conn()
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.executemany(sql_str, value_list_tuple)
            # 提交事务
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
            cursor.close()
            conn.close()
            return False

    def update_or_delete_one(self, sql_str, value_list):
        """
        :param sql_str: 例如 -> "DELETE FROM tsglxt_config_info WHERE info_id=%s and data=%s;"
        :param value_list: 例如 -> [10,'a']
        :return: True or Flase
        """
        # 连接database
        conn = self.__get_conn()
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql_str, value_list)
            # 提交事务
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
            cursor.close()
            conn.close()
            return False

    def get_find_list(self, sql_str):
        """
        :param sql_str: 例如 -> "select * from tsglxt_config_info where info_id=50"
        :return: 列表包字典 或者 [{'info': 'error'}]
        """
        # 连接database
        conn = self.__get_conn()
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 查询数据的SQL语句
        sql = sql_str
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取多条查询数据
            ret = cursor.fetchall()
            cursor.close()
            conn.close()
            return ret
        except:
            return [{'info': 'error'}]
