import json
import os
import struct


# 直接发送bytes数据
def send_data(conn, content):
    data = content.encode('utf-8')
    header = struct.pack('i', len(data))
    conn.sendall(header)
    conn.sendall(data)


def send_file(conn, file_path):
    file_size = os.stat(file_path).st_size
    header = struct.pack('i', file_size)
    conn.sendall(header)

    has_send_size = 0
    file_object = open(file_path, mode='rb')
    while has_send_size < file_size:
        chunk = file_object.read(2048)
        conn.sendall(chunk)
        has_send_size += len(chunk)
    file_object.close()
