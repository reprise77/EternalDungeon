import pygame as pg
from textures import Textures_Hud_Sound
from hud import Hud
import random


class Menu:
    def __init__(self):
        self.textures = Textures_Hud_Sound()
        self.start_button = self.textures.hud["start"]
        self.exit_button = self.textures.hud["exit"]
        self.width, self.height = 1600, 900
        self.rect = self.start_button.get_rect()
        self.exit = self.exit_button.get_rect()
        self.rect.x, self.rect.y = self.width // 2, self.height // 2
        self.exit.x, self.exit.y = self.rect.x, self.rect.y + 100
        self.window = pg.display.set_mode((self.width, self.height))
        self.fill_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.bg_color = pg.Color(38, 30, 51, 150)
        self.fill_surface.fill((self.bg_color.r, self.bg_color.g, self.bg_color.b, self.bg_color.a))
        self.hud = Hud()
        self.font = pg.font.Font(None, 28)
        self.clock = pg.time.Clock()
        self.stars = []
        self.sound = Textures_Hud_Sound()
        self.sound_button = self.sound.sound["button"]
        self.sound_button.set_volume(0.5)
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            speed = random.randint(1, 3)
            self.stars.append((x, y, speed))

    def update(self, width, height, pause):
        self.rect.x, self.rect.y = width // 2 - ((width * 0.06) / 2), height // 3
        self.exit.x, self.exit.y = self.rect.x, self.rect.y + 100
        if pause == True:
            self.start_button = self.textures.hud["continue"]
            self.rect.x -= 13
        else:
            self.start_button = self.textures.hud["start"]

    def render(self, pause):  # Выводит все на экран
        if pause == False:
            self.window.fill(self.bg_color)
        else:
            self.window.blit(self.fill_surface, (0, 0))
        self.window.blit(self.start_button, self.rect)
        self.window.blit(self.exit_button, self.exit)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False

    def exit_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.exit.collidepoint(event.pos):
            return True
        return False

    def wallpaper(self, dt, player):
        for i in range(len(self.stars)):
            x, y, speed = self.stars[i]
            if player.player_hp > 1:
                x -= speed * dt * 40
                y += speed * dt * 40
            else:
                x -= speed * dt * 10
                y += speed * dt * 10
            if x < 0 or y > self.height:
                x = random.randint(0, self.width, )
                y = random.randint(-400, self.height)
                speed = random.randint(1, 3)  # Генерация новой случайной скорости
            self.stars[i] = (x, y, speed)
