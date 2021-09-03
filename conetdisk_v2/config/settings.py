""" 存放该项目的配置文件  """
import os

""" 服务器的IP及端口号 """
IP = '127.0.0.1'
PORT = 8001

""" 根地址、数据库地址、用户信息文件地址 """
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_PATH, 'database')
USER_FILE_PATH = os.path.join(DB_PATH, 'user_info.xlsx')

if __name__ == '__main__':
    print('IP，PORT --> ', IP, ' ', PORT)
    print('BASE_PATH --> ', BASE_PATH)
    print('DB_PATH --> ', DB_PATH)
    print('USER_FILE_PATH --> ', USER_FILE_PATH)
