import sys
import pygame
import pickle
import socket
from player import Player
from random import randint


class GameWindow:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.window = self.init_window()

        self.pic = pygame.image.load("C:/Users/wanga/Documents/BPCE/PlayerWalk/PlayerWalk/pics/walk.png")
        frame_width = self.pic.get_width() // 4
        frame_height = self.pic.get_height() // 4

        self.player = Player(p_id=None,
                             x=randint(0, self.width-frame_width),
                             y=randint(0, self.height-frame_height),
                             frame_width=frame_width,
                             frame_height=frame_height)

        self.port = 5000
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()

    def init_window(self):
        pygame.init()
        pygame.display.set_caption('移动方块')
        return pygame.display.set_mode((self.width, self.height))

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(2048).decode("utf-8")

    def send_player_data(self):
        data = {
            "id": self.player.id,
            "player": self.player
        }
        self.sock.send(pickle.dumps(data))
        return self.sock.recv(2048)

    def update_window(self):
        self.window.fill((255, 255, 255))

        self.player.move()
        self.player.draw(self.window, self.pic)

        other_players_data = pickle.loads(self.send_player_data())
        self.update_other_players_data(other_players_data)

        pygame.display.update()

    def update_other_players_data(self, data):
        for player in data.values():
            player.draw(self.window, self.pic)

    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_window()


if __name__ == '__main__':
    game = GameWindow()
    game.start()
