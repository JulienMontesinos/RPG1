import pygame


class Player:
    def __init__(self, p_id, x, y, frame_width, frame_height):
        self.id = p_id
        self.dis = 3
        self.x = x
        self.y = y

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_num = 0
        self.frame_rect = (self.frame_num * self.frame_width, 0 * self.frame_height,
                           self.frame_width, self.frame_height)

        self.current_dir = "下"
        self.last_dir = self.current_dir

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.dis
            self.current_dir = "左"
            self.set_frame_rect(1)

        elif keys[pygame.K_RIGHT]:
            self.x += self.dis
            self.current_dir = "右"
            self.set_frame_rect(2)

        elif keys[pygame.K_UP]:
            self.y -= self.dis
            self.current_dir = "上"
            self.set_frame_rect(3)

        elif keys[pygame.K_DOWN]:
            self.y += self.dis
            self.current_dir = "下"
            self.set_frame_rect(0)

        self.last_dir = self.current_dir

    def set_frame_rect(self, pic_row):
        self.frame_num += 1
        if self.current_dir != self.last_dir or self.frame_num > 3:
            self.frame_num = 0

        self.frame_rect = (self.frame_num * self.frame_width, pic_row * self.frame_height,
                           self.frame_width, self.frame_height)

    def draw(self, win, pic):
        win.blit(pic, (self.x, self.y), self.frame_rect)