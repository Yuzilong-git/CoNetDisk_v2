import os
import json
import struct
import hashlib


def send_data(conn, content):
    """ 发送数据 """
    data = content.encode('utf-8')
    header = struct.pack('i', len(data))
    conn.sendall(header)
    conn.sendall(data)


def send_file_by_seek(conn, file_size, file_path, has_recv_size=0):
    """ 读取并发送文件（支持从指定字节位置开始读取）"""
    header = struct.pack('i', file_size)
    conn.sendall(header)

    has_send_size = 0
    file_object = open(file_path, mode='rb')
    if has_recv_size:
        file_object.seek(has_recv_size)
    while has_send_size < file_size:
        chunk = file_object.read(2048)
        conn.sendall(chunk)
        has_send_size += len(chunk)
    file_object.close()

