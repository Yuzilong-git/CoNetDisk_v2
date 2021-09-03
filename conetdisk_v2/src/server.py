import socket
import select
from config import settings


class SelectServer:
    def __init__(self):
        self.ip = settings.IP
        self.port = settings.PORT
        # 用于存放服务端和客户端的socket对象
        self.socket_list = []
        self.conn_dict = {}

    # 启动服务端
    def run(self, handler):
        server_boj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_boj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_boj.setblocking(True)

        server_boj.bind((self.ip, self.port))
        server_boj.listen(5)
        self.socket_list.append(server_boj)

        while True:
            r, w, e = select.select(self.socket_list, [], [], 0.05)
            for sock in r:
                try:
                    # 新连接到来，执行 handler的 __init__ 方法
                    if sock == server_boj:
                        print("新客户端来连接")
                        conn, addr = server_boj.accept()
                        self.socket_list.append(conn)
                        # 实例化handler类，即：类(conn)
                        self.conn_dict[conn] = handler(conn)
                        continue

                    # 新数据到来，执行 handler的 __call__ 方法
                    handler_object = self.conn_dict[sock]
                    # 执行handler类对象的 execute 方法，如果返回False，则意味关闭服务端与客户端的连接
                    result = handler_object.execute()
                    # print(result)
                    if not result:
                        self.socket_list.remove(sock)
                        del self.conn_dict[sock]
                except Exception as e:
                    print(e)
                    sock.close()



