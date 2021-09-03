import re
import os
import json
import socket
from utils import send_func, recv_func
from config import settings


class Handler:
    def __init__(self):
        self.ip = settings.IP
        self.port = settings.PORT
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def run(self):
        self.conn.connect((self.ip, self.port))
        welcome = """
        注册：register coco 123456
        登录：login coco 123456
        上传文件：upload xx/xxx.mp4(本地文件路径)  (需进入到上传目录内)
        下载文件：download xxx.mp4(当前云盘目录内的文件名) files(本地下载目录)
        进入目录：cd files
        新建目录：makedir video
        显示当前目录下文件：ls
        """
        print(welcome)

        method_map = {
            "register": self.register,
            "login": self.log_in,
            "upload": self.upload,
            "download": self.download,
            "cd": self.change_directory,
            "makedir": self.make_dir,
            "ls": self.ls
        }

        while True:
            hint = "({})>>> ".format(self.username or "未登录")
            info = input(hint).strip()
            if not info:
                print("输入不能为空，请重新输入。")
                continue

            if info.upper() == "Q":
                print("退出成功")
                send_func.send_data(self.conn, "q")
                recv_res = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
                if recv_res['status']:
                    return

            cmd, *arg_list = re.split(r"\s+", info)

            method = method_map.get(cmd)
            if not method:
                print("命令不存在，请重新输入。")
                continue
            method(*arg_list)

        self.conn.close()

    def register(self, *args):
        if len(args) != 2:
            print("格式错误，请重新输入!")
            return
        user_name, password = args
        send_str = "register {} {}".format(user_name, password)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            print("用户 {} 注册成功！".format(user_name))
            return
        else:
            print(reply_dict['error'])

    def log_in(self, *args):
        if len(args) != 2:
            print("格式错误，请重新输入!")
            return
        user_name, password = args
        send_str = "login {} {}".format(user_name, password)
        # 发送注册信息给服务端
        send_func.send_data(self.conn, send_str)
        # 接收服务端对注册的响应信息
        reply_dict = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if reply_dict['status']:
            self.username = user_name
            print("{}，欢迎回来！！".format(user_name))
            return
        else:
            print(reply_dict['error'])

    def upload(self, local_file):
        if self.username is None:
            print("未登陆，请在登录状态下使用!")
            return
        # local_file：本地文件路径
        # 判断本地文件是否存在
        if not os.path.exists(local_file):
            print("文件不存在，请重新输入！")
            return
        # file_name：根据本地文档目录切片分出的文件名
        file_name = local_file.rsplit('/' or '\\')[-1]
        # 发送所需请求格式给服务端
        send_func.send_data(self.conn, "upload {}".format(file_name))
        # 等待服务端回应
        reply = recv_func.recv_data(self.conn).decode('utf-8')
        reply_dict = json.loads(reply)
        # # 如果发送失败的话
        # if not reply_dict['status']:
        #     print(reply_dict['error'])
        #     return
        # 正常开始上传文件
        print("文件 {} {}".format(file_name, reply_dict['data']))  # reply_dict['data']
        # 开始发送文件数据给服务端
        send_func.send_file(self.conn, local_file)
        print("文件 {} 上传成功".format(file_name))

    def download(self, *args):
        if self.username is None:
            print("未登陆，请在登录状态下使用!")
            return
        if len(args) != 2:
            print("输入格式有误，请重试！")
            print("格式：文件下载路径 当前云盘目录下的文件名称")
            return
        # local_directory：文件下载路径 cloud_file：当前云盘目录下的文件名称
        cloud_file, local_directory = args
        if local_directory == 'files':
            local_file_path = os.path.join(settings.DOWNLOAD_FILE_PATH, cloud_file)
        # local_file_path：本地后的文件路径(带文件名)
        else:
            local_file_path = os.path.join(local_directory, cloud_file)
        print(local_file_path)
        # 已接收的文件大小，用于续传
        has_recv_size = 0
        # 文件打开模式，续传则追加，不续传则写入(覆盖)
        open_mode = 'wb'
        # 判断本地下载目录是否已经有下载的该文件了
        print('local_directory>>>', local_directory)
        if os.path.exists(local_file_path):
            choice = int(input("该文件已存在，续传请输入1，否则输入0："))
            if choice == 1 or choice == 0:
                pass
            else:
                print("输入格式有误，请重试！")
                return
            if choice:
                has_recv_size = os.path.getsize(local_file_path)
                send_func.send_data(self.conn, "download {} {}".format(local_file_path, has_recv_size))
                open_mode = 'ab'
        send_func.send_data(self.conn, "download {}".format(cloud_file))
        reply = recv_func.recv_data(self.conn).decode("utf-8")
        reply_dict = json.loads(reply)
        if not reply_dict['status']:
            print(reply_dict['error'])
        else:
            print("文件 {} 开始下载".format(cloud_file))  # print(reply_dict['data'])
            recv_func.recv_save_file_with_progress(self.conn, local_file_path, open_mode, seek=has_recv_size)
            print("文件 {} 下载完毕".format(cloud_file))

    def ls(self):
        if self.username is None:
            print("未登陆，请在登录状态下使用!")
            return
        send_func.send_data(self.conn, "ls")
        result = recv_func.recv_data(self.conn).decode('utf-8')
        ls_dict = json.loads(result)
        # result : b'{"dir": ["files"], "file": []}'
        self.show_file(ls_dict)

    @staticmethod
    def show_file(dir_dict):
        print('>>该目录下有文件夹：')
        for index, name in enumerate(dir_dict['dir'], 1):
            print(index, name, end='   ')
        print('\n>>该目录下有文件：')
        for index, name in enumerate(dir_dict['file'], 1):
            print(index, name, end='   ')

    def make_dir(self, dir_name):
        if self.username is None:
            print("未登陆，请在登录状态下使用!")
            return
        send_func.send_data(self.conn, "make_dir {}".format(dir_name))
        recv_result = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        if recv_result['status']:
            print(recv_result['data'])
        else:
            print(recv_result['error'])

    def change_directory(self, cd_dirname):
        if self.username is None:
            print("未登陆，请在登录状态下使用!")
            return
        send_func.send_data(self.conn, "change_directory {}".format(cd_dirname))
        recv_result = json.loads(recv_func.recv_data(self.conn).decode('utf-8'))
        self.show_file(recv_result)


if __name__ == '__main__':
    text = 'register coco 181221'
    command, args = re.split(r"\s+", text)
    print(command)
    print(*args)
