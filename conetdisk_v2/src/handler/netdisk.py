# 用户功能类
import re
import os
import time
import json
from datetime import datetime
from utils import recv_func, verify, send_func
from config import settings


class PanHandler:
    # 调用时传客户端socket对象
    def __init__(self, conn):
        self.conn = conn
        self.user_name = None
        self.current_path = ''

    @property
    def home_path(self):
        return os.path.join(settings.DB_PATH, self.user_name)

    def send_json_data(self, **kwargs):
        # kwargs={"status": False, 'error': "用户名已存在"}
        send_func.send_data(self.conn, json.dumps(kwargs))

    def execute(self):
        """
        用于处理客户端发送来的请求
        :return: True：继续运行，处理客户端请求。False：断开此次与该客户端的连接
        """
        conn = self.conn
        command = recv_func.recv_data(conn).decode('utf-8')
        # print(command)
        if command.upper() == "Q":
            self.send_json_data(status=True, data="退出")
            print("用户 {} 退出".format(self.user_name))
            return False
        method_map = {
            "register": self.register,
            "login": self.log_in,
            "upload": self.upload,
            "download": self.download,
            "change_directory": self.change_directory,
            "make_dir": self.make_dir,
            "ls": self.ls
        }
        command, *args = re.split(r'\s+', command)
        method = method_map[command]
        method(*args)

        return True

    def register(self, user_name, password):
        verify_result = verify.verify_register(user_name)
        if not verify_result:
            register_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            verify.update_info(user_name, verify.md5_convert(user_name, password), register_time)
            print("用户 {} 注册成功！".format(user_name))
            self.send_json_data(status=True, data="注册成功")
            self.user_name = user_name
            home_path = os.path.join(settings.DB_PATH, self.user_name)
            try:
                os.mkdir(home_path)
            except FileExistsError:
                pass
        else:
            # 发送注册失败，用户名已存在
            self.send_json_data(status=False, error="用户名已存在")

    def log_in(self, user_name, password):
        verify_result = verify.verify(user_name, verify.md5_convert(user_name, password))
        if verify_result:
            # 发送登录成功
            self.user_name = user_name
            self.current_path = self.home_path
            print("用户 {} 登录成功！".format(user_name))
            self.send_json_data(status=True, data="登录成功")
            # 把该次通信的用户名改为改用户的用户名
        else:
            # 发送用户名不存在或密码错误
            self.send_json_data(status=False, error="用户名不存在或密码错误")

    def upload(self, cloud_dir):
        save_path = os.path.join(self.current_path, cloud_dir)
        self.send_json_data(status=True, data="开始上传")
        time.sleep(2)
        recv_func.recv_save_file(self.conn, save_path)
        print("用户 {} 上传文件成功！".format(self.user_name))

    def download(self, cloud_file, has_recv_size=0):
        """
        :param cloud_file: 当前云盘目录下的文件名
        :param has_recv_size: 从哪里开始发送
        :return: 无
        """
        # down_file:拼接所下载文件的相对路径
        down_file = os.path.join(self.current_path, cloud_file)
        if not os.path.exists(down_file):
            self.send_json_data(status=False, error="文件 {} 不存在".format(down_file))
            return
        self.send_json_data(status=True, data="开始下载")
        total_size = os.path.getsize(down_file)
        send_func.send_file_by_seek(self.conn, total_size - has_recv_size, down_file, has_recv_size)
        print("用户 {} 下载文件成功！".format(self.user_name))

    def list_dir(self):
        file_list = os.listdir(self.current_path)
        file_dic = {'dir': [], 'file': []}
        for file_name in file_list:
            path = os.path.join(self.current_path, file_name)
            if os.path.isfile(path):
                file_dic['file'].append(file_name)
            else:
                file_dic['dir'].append(file_name)
        return file_dic

    def make_dir(self, dir_name):
        dir_path = os.path.join(self.current_path, dir_name)
        if os.path.exists(dir_path):
            self.send_json_data(status=False, error="该文件夹已存在！")
            return
        os.mkdir(dir_path)
        self.send_json_data(status=True, data="文件夹 {} 创建成功！".format(dir_name))

    def ls(self):
        file_dict = self.list_dir()
        file_dict = json.dumps(file_dict)
        send_func.send_data(self.conn, file_dict)

    def change_directory(self, cd_dirname):
        path = os.path.join(self.current_path, cd_dirname)
        if not os.path.isdir(path):
            self.send_json_data(status=False, error="该文件夹不存在！！")
            return
        self.current_path = path
        file_dict = self.list_dir()
        file_dict = json.dumps(file_dict)
        send_func.send_data(self.conn, file_dict)
