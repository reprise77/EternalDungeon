import random

import pygame as pg
from map import Map
from textures import Textures_Hud_Sound
from textures import Textures_tile
from object import Items


class Map_generator:
    def __init__(self, width, height, window):
        self.PLATFORM_WIDTH = width * (1 / 25)
        self.PLATFORM_HEIGHT = height * (1 / 15)
        self.ROOM_WIDTH = width
        self.ROOM_HEIGHT = height
        self.items = Items()
        self.index = 0
        self.back_rooms = {
            0: self.index}
        self.lobby = Map(window, width, height, self.back_rooms[self.index], 10)
        self.rooms = {
            "room_0": self.lobby}
        self.sound = Textures_Hud_Sound()
        self.textures = Textures_tile()
        self.teleport_up = pg.Rect(self.PLATFORM_WIDTH * 12, 0, self.PLATFORM_WIDTH * 3, self.PLATFORM_HEIGHT)
        self.teleport_left = pg.Rect(self.PLATFORM_WIDTH * 2, self.PLATFORM_HEIGHT * 6, self.PLATFORM_WIDTH,
                                     self.PLATFORM_HEIGHT * 3)
        self.teleport_right = pg.Rect(self.PLATFORM_WIDTH * 22, self.PLATFORM_HEIGHT * 6, self.PLATFORM_WIDTH,
                                      self.PLATFORM_HEIGHT * 3)
        self.teleport_down = pg.Rect(self.PLATFORM_WIDTH * 12, self.PLATFORM_HEIGHT * 13, self.PLATFORM_WIDTH * 3,
                                     self.PLATFORM_HEIGHT)
        self.wall_positions = []
        self.sound_arrow_wall = self.sound.sound["arrow_wall"]
        self.sound_arrow_wall.set_volume(0.5)
        self.tileData = self.textures.tileData
        self.clear_room = -1
        self.clear = False
        self.sound_vzhooh = self.sound.sound["vzhooh"]
        self.sound_wall = self.sound.sound["destruction_wall"]
        self.sound_flag = False
        self.sound_vzhooh.set_volume(0.7)
        self.prev_rect = pg.Rect(0, 0, 0, 0)
        self.side_up = self.textures.texture_room["side_lock_up"].convert_alpha()
        self.side_up = pg.transform.scale(self.side_up, (256, 109))
        self.side_down = self.textures.texture_room["side_lock_down"].convert_alpha()
        self.side_left = self.textures.texture_room["side_lock_left"].convert_alpha()
        self.side_right = self.textures.texture_room["side_lock_right"].convert_alpha()
        self.up_collisian = pg.Rect(self.PLATFORM_WIDTH * 12, self.PLATFORM_HEIGHT, self.PLATFORM_WIDTH * 3,
                                    self.PLATFORM_HEIGHT)
        self.left_collisian = pg.Rect(self.PLATFORM_WIDTH * 3, self.PLATFORM_HEIGHT * 6, self.PLATFORM_WIDTH,
                                      self.PLATFORM_HEIGHT * 3)
        self.right_collisian = pg.Rect(self.PLATFORM_WIDTH * 21, self.PLATFORM_HEIGHT * 6, self.PLATFORM_WIDTH,
                                       self.PLATFORM_HEIGHT * 3)
        self.down_collisian = pg.Rect(self.PLATFORM_WIDTH * 12, self.PLATFORM_HEIGHT * 12, self.PLATFORM_WIDTH * 3,
                                      self.PLATFORM_HEIGHT)
        self.bonus_counter = 0

    def generate_world(self, window, character_rect, player, enemy, prev_rect):
        if f"room_{self.index}" not in self.rooms:
            self.rooms[f"room_{self.index}"] = Map(window, self.ROOM_WIDTH, self.ROOM_HEIGHT,
                                                   self.back_rooms[self.index], random.randint(1, 10))
        self.rooms[f"room_{self.index}"].map_build(window)
        self.bonus_room(window, character_rect, player, enemy)
        self.wall_positions = self.rooms[f"room_{self.index}"].wall_positions
        self.lock_room(enemy, window, player, prev_rect)
        self.rooms[f"room_{self.index}"].stage_clear(enemy, self.index)
        if self.index == 0:
            self.teleport_return = ""
        if character_rect.colliderect(self.teleport_up):
            self.sound_vzhooh.play()
            if self.back_rooms[self.index] == "up":
                self.index -= 1
                player.rect.y += 550
            else:
                self.index += 1
                player.rect.y += 550
                if self.index not in self.back_rooms:
                    self.back_rooms[self.index] = "down"
        elif character_rect.colliderect(self.teleport_down):
            self.sound_vzhooh.play()
            if self.back_rooms[self.index] == "down":
                self.index -= 1
                player.rect.y -= 550
            else:
                self.index += 1
                player.rect.y -= 550
                if self.index not in self.back_rooms:
                    self.back_rooms[self.index] = "up"
        elif character_rect.colliderect(self.teleport_left):
            self.sound_vzhooh.play()
            if self.back_rooms[self.index] == "left":
                self.index -= 1
                player.rect.x += 1050
            else:
                self.index += 1
                player.rect.x += 1050
                if self.index not in self.back_rooms:
                    self.back_rooms[self.index] = "right"
        elif character_rect.colliderect(self.teleport_right):
            self.sound_vzhooh.play()
            if self.back_rooms[self.index] == "right":
                self.index -= 1
                player.rect.x -= 1050
            else:
                self.index += 1
                player.rect.x -= 1050
                if self.index not in self.back_rooms:
                    self.back_rooms[self.index] = "left"
        text = "room: ({})".format(self.index)
        font = pg.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.ROOM_WIDTH - 90, 50)
        self.cleared_room(enemy)
        room_cleared = pg.font.Font(None, 36).render("Clear: " + str(int(self.clear_room)), True, pg.Color('white'))
        window.blit(room_cleared, (1450, 200))
        window.blit(text_surface, text_rect)

    def check_collision(self, character_rect):  # Устанавливает коллизии на края
        for wall_rect in self.wall_positions:
            if character_rect.colliderect(wall_rect):
                return True
        return False

    def enemy_collide_wall(self, enemys):
        for wall_rect in self.wall_positions:
            for enemy in enemys.enemies:
                if enemy.rect.colliderect(wall_rect):
                    enemy.rect = enemy.pre_rect

    def arrow_collide_wall(self, bullеt):
        for wall_rect in self.wall_positions:
            for arrow in bullеt.arrows:
                if arrow.rect.colliderect(wall_rect):
                    self.sound_arrow_wall.play()
                    bullеt.arrows.remove(arrow)

    def cleared_room(self, enemy):
        if not enemy.enemies:
            if not self.clear:
                self.clear_room += 1
                self.clear = True
        else:
            self.clear = False

    def lock_room(self, enemy, window, player, prev_rect):
        if enemy.enemies:
            self.sound_flag = True
            character_rect = pg.Rect(player.rect.x + 30, player.rect.y + 10, 69, 84)
            if self.rooms[f"room_{self.index}"].rand_side == "up" or self.back_rooms[self.index] == "up":
                window.blit(self.side_up, (64 * 11, 101))
                if self.up_collisian.colliderect(character_rect):
                    player.rect = prev_rect
            if self.rooms[f"room_{self.index}"].rand_side == "down" or self.back_rooms[self.index] == "down":
                window.blit(self.side_down, (64 * 11, 60 * 12))
                if self.down_collisian.colliderect(character_rect):
                    player.rect = prev_rect
            if self.rooms[f"room_{self.index}"].rand_side == "left" or self.back_rooms[self.index] == "left":
                window.blit(self.side_left, (64 * 4 - 20, 60 * 5))
                if self.left_collisian.colliderect(character_rect):
                    player.rect = prev_rect
            if self.rooms[f"room_{self.index}"].rand_side == "right" or self.back_rooms[self.index] == "right":
                window.blit(self.side_right, (64 * 21, 60 * 5))
                if self.right_collisian.colliderect(character_rect):
                    player.rect = prev_rect
        else:
            if self.sound_flag:
                self.sound_wall.play()
                self.sound_flag = False

    def bonus_room(self, window, character, player, enemy):
        self.rooms[f"room_{self.index}"].item_pick_up = self.pick_up(character, player, enemy)
        if self.rooms[f"room_{self.index}"].bonus == 1 and self.rooms[f"room_{self.index}"].item_pick_up == False:
            self.items.healing_potion(window, character)
        elif self.rooms[f"room_{self.index}"].bonus <=4 and self.rooms[f"room_{self.index}"].item_pick_up == False:
            self.items.attack_up(window, character, self.rooms[f"room_{self.index}"].random_attack_percent)

    def pick_up(self, character, player, enemy):
        keys = pg.key.get_pressed()
        if character.colliderect(self.items.potion_rect) and keys[pg.K_f] and self.rooms[f"room_{self.index}"].get_pressed == False:
            if self.rooms[f"room_{self.index}"].bonus == 1:
                player.player_hp += 3
                if player.player_hp > 11:
                    player.player_hp = 11
            self.rooms[f"room_{self.index}"].get_pressed = True
            return True
        if character.colliderect(self.items.attack_rect) and keys[pg.K_f] and self.rooms[f"room_{self.index}"].get_pressed == False:
            if self.rooms[f"room_{self.index}"].bonus <= 4:
                enemy.percent_damage += 0.25
            self.rooms[f"room_{self.index}"].get_pressed = True
            return True
        elif self.rooms[f"room_{self.index}"].get_pressed == False :
            return False

