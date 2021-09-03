""" 存放该项目的配置文件  """
import os

""" 服务器的IP及端口号 """
IP = '127.0.0.1'
PORT = 8001

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DOWNLOAD_FILE_PATH = os.path.join(BASE_PATH, 'files')

if __name__ == '__main__':
    print('IP，PORT --> ', IP, ' ', PORT)
    print("BASE_PATH>>>", BASE_PATH)
    print("DOWNLOAD_FILE_PATH>>>", DOWNLOAD_FILE_PATH)
