import socket  # 导入socket库用于网络连接
import pickle  # 导入pickle库用于对象的序列化和反序列化
from player import Player  # 假设从player模块导入Player类，用于表示玩家（尽管这个脚本并未直接使用Player类）
from threading import Thread  # 从threading模块导入Thread类，用于多线程

class Server:
    def __init__(self):
        self.port = 5000  # 服务器监听的端口号
        self.host = "127.0.0.1"  # 服务器的主机地址，这里是本地地址
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个TCP套接字
        self.players_data = {}  # 用于存储所有玩家的数据，键是玩家的ID，值是玩家的数据

    def start(self):
        self.get_socket_ready()  # 准备socket，包括绑定地址和监听端口
        self.handle_connection()  # 开始接受和处理客户端连接

    def get_socket_ready(self):
        self.sock.bind((self.host, self.port))  # 绑定到指定的主机和端口上
        self.sock.listen()  # 开始监听端口
        print("服务器已准备接收客户端连接")  # 打印信息表示服务器准备就绪

    def handle_connection(self):
        while True:  # 无限循环，持续接受客户端的连接
            conn, addr = self.sock.accept()  # 接受一个客户端连接
            print(f"接收到来自{addr}的连接")  # 打印出接受到的连接信息
            conn.send(str(id(conn)).encode("utf-8"))  # 发送连接的唯一ID给客户端
            Thread(target=self.handle_message, args=(conn, )).start()  # 为每个客户端创建一个新线程来处理消息

    def handle_message(self, conn):
        while True:  # 无限循环，持续监听客户端消息
            try:
                data = conn.recv(2048)  # 接受客户端发送的数据，最大为2048字节
                if not data:  # 如果没有数据，说明连接可能已关闭
                    print("未接收到数据，关闭连接")
                    self.players_data.pop(str(id(conn)))  # 从玩家数据中移除对应的玩家信息
                    conn.close()  # 关闭连接
                    break  # 跳出循环
                else:
                    data = pickle.loads(data)  # 反序列化接收到的数据
                    self.update_one_player_data(data)  # 更新接收到的玩家数据
                    conn.sendall(pickle.dumps(self.get_other_players_data(data["id"])))  # 发送除了当前玩家外的所有玩家数据
            except Exception as e:
                print(repr(e))  # 打印出现的异常
                break  # 发生异常时跳出循环

    def update_one_player_data(self, data):
        key = data["id"]  # 玩家的唯一标识符
        value = data["player"]  # 玩家的数据
        self.players_data[key] = value  # 更新或添加玩家数据

    def get_other_players_data(self, current_player_id):
        data = {}  # 创建一个新字典用于存储其他玩家的数据
        for key, value in self.players_data.items():  # 遍历所有玩家数据
            if key != current_player_id:  # 如果不是当前玩家的数据
                data[key] = value  # 添加到字典中
        return data  # 返回其他玩家的数据

if __name__ == '__main__':
    server = Server()  # 创建Server实例
    server.start()  # 启动服务器



