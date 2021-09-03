""" 网盘项目入口程序 """
from src.handler.netdisk import PanHandler
from src.server import SelectServer

if __name__ == '__main__':
    server = SelectServer()
    server.run(PanHandler)
