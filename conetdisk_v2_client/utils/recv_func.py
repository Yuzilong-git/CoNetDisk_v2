import struct
import time


def recv_data(conn, chunk_size=1024):
    # 获取头部信息：数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        has_read_size += len(chunk)
        bytes_list.append(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    # 获取数据
    data_list = []
    has_read_data_size = 0
    while has_read_data_size < data_length:
        size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
        chunk = conn.recv(size)
        data_list.append(chunk)
        has_read_data_size += len(chunk)

    data = b"".join(data_list)

    return data


def recv_save_file_with_progress(conn, save_file_path, mode, chunk_size=1024, seek=0):
    # 获取头部信息：数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        bytes_list.append(chunk)
        has_read_size += len(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    # 获取数据
    file_object = open(save_file_path, mode=mode)
    file_object.seek(seek)

    has_read_data_size = 0
    while has_read_data_size < data_length:
        size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
        chunk = conn.recv(size)
        file_object.write(chunk)
        file_object.flush()
        has_read_data_size += len(chunk)

        percent = "\r{}%".format(int(has_read_data_size * 100 / data_length))
        print(percent, end="")
        time.sleep(0.5)

    print("")
    file_object.close()
