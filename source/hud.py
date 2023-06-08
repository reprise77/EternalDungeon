import pygame as pg
import os
from textures import Textures_Hud_Sound


class Hud:
    def __init__(self):
        self.textures = Textures_Hud_Sound()
        self.heal_bar = self.textures.hud
        self.hp_bar = self.heal_bar["hp_bar_11"]
        self.direct_bg = os.path.join(os.getcwd(), "assets", "material", "Hud")
        self.button_screen_mode = self.textures.hud["Fullscreen"]
        self.button_screen_mode_rect = self.button_screen_mode.get_rect()
        self.font = pg.font.Font("ThaleahFat.ttf", 60)
        self.score = 0

    def heal_idicate(self, hero_hp, width, height, window):
        if hero_hp <= 1:
            hero_hp = 1
        self.hp_bar = self.heal_bar[f"hp_bar_{hero_hp}"]
        self.hp_bar = pg.transform.scale(self.hp_bar, (width * (249 / 800), height * (4 / 75)))
        window.blit(self.hp_bar, (width * pow(116, -1), height * pow(30, -1)))

    def game_over_player_move(self, player, weapon, width, height):
        player.rect.centerx = width // 2 - (player.new_width / 2)
        player.rect.centery = height // 2 - (player.new_height / 2)
        center = weapon.image.get_rect().center
        weapon.image_center = weapon.rotated_image.get_rect(center=center)
        weapon.image_rect = player.rect.copy()
        weapon.image_rect.x += weapon.image_center.x - center[0] + (player.new_width / 2) + (
                player.new_width / 6)  # Центральные координаты спрайта игрока
        weapon.image_rect.y += weapon.image_center.y - center[1] + (player.new_height / 2) + (player.new_height / 6)

    def screen_mode(self, fullscreen, window, width):
        if fullscreen:
            self.button_screen_mode = self.textures.hud["Windowed"]
        else:
            self.button_screen_mode = self.textures.hud["Fullscreen"]
        self.button_screen_mode_rect.x = width - 74
        self.button_screen_mode_rect.y = 10
        window.blit(self.button_screen_mode, self.button_screen_mode_rect)

    def screen_mode_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.button_screen_mode_rect.collidepoint(event.pos):
            return True
        return False

    def score_converter(self):
        score = str(self.score)
        while len(score) != 14:
            score = "0" + score
        return score

    def score_bar(self, window):
        score = self.score_converter()
        text_surface = self.font.render(score, True, (255, 255, 255))
        window.blit(text_surface, (1100, 8))

