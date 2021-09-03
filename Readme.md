#  Introduction

本项目是一个基于socket、select模块的FTP网盘系统

可以实现注册、登录、上传文件、下载文件、目录管理等功能

具有md5加密及文件完整性校验功能，拥有断点续传、多并发的优点，旨在打造一个快速全面的网盘系统

#  开发环境

Python 3.9

#  启动项目

- 运行服务端

  启动服务端项目目录下main文件即可运行服务端

  服务端运行效果如下：

<img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607141619245.png" alt="image-20210607141619245"  />

- 运行客户端

  启动conetdisk_v2_client项目下client_main.py程序即可运行客户端

  客户端运行效果如下：

  ![image-20210607142010864](/Users/coco/Library/Application Support/typora-user-images/image-20210607142010864.png)



#  项目结构图

- 服务端项目目录

<img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607143001320.png" alt="image-20210607143001320" style="zoom:67%;" />        <img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607143637218.png" alt="image-20210607143637218" style="zoom: 67%;" />



- 客户端项目目录

  <img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607144203981.png" alt="image-20210607144203981" style="zoom:90%;" style=""/><img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607144111763.png" alt="image-20210607144111763" style="float: right;zoom:73%;"  />



#  主要功能

##  用户注册

客户端程序启动后，输入

```python
register 用户名 密码
```

回车进行注册，若注册成功会返回注册成功，注册失败会返回注册失败

如图所示

- 注册成功

![image-20210607145711690](/Users/coco/Library/Application Support/typora-user-images/image-20210607145711690.png)

成功后会服务端提醒且在用户信息文件中更新信息

<img src="/Users/coco/Library/Application Support/typora-user-images/image-20210607150148208.png" alt="image-20210607150148208" style="zoom: 67%;" />

- 注册失败

  ![image-20210607145852212](/Users/coco/Library/Application Support/typora-user-images/image-20210607145852212.png)

## 用户登录

注册成功后，输入

```py
login 用户名 密码
```

进行登录，登录成功返回登录成功，失败返回登录失败

- 登录成功

![image-20210607145741969](/Users/coco/Library/Application Support/typora-user-images/image-20210607145741969.png)

- 登录失败

  ![image-20210607145923111](/Users/coco/Library/Application Support/typora-user-images/image-20210607145923111.png)

##  显示当前路径下文件及文件夹

输入

```python
ls
```

即可获取云盘中当前路径下的所有文件及文件夹，并以固定格式返回

![image-20210607150335665](/Users/coco/Library/Application Support/typora-user-images/image-20210607150335665.png)

##  在当前目录下创建文件夹

输入

```python
makedir 文件夹名
```

即可在云盘当前路径下新建文件夹

![image-20210607150502783](/Users/coco/Library/Application Support/typora-user-images/image-20210607150502783.png)

##  进入当前目录下指定目录

输入

```python
cd 文件夹名
```

即可进入当前目录下的下级目录

![image-20210607150619410](/Users/coco/Library/Application Support/typora-user-images/image-20210607150619410.png)

##  上传文件

输入

```python
upload 上传文件在本地的地址
```

即可将指定文件传入当前云盘目录

![image-20210607150754330](/Users/coco/Library/Application Support/typora-user-images/image-20210607150754330.png)

##  下载文件

输入

```python
download (当前云盘目录下文件名) (本地文件保存地址)
```

即可将云盘文件下载到本地指定目录下

![image-20210607151343993](/Users/coco/Library/Application Support/typora-user-images/image-20210607151343993.png)





