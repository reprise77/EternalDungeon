import pygame as pg
from textures import Textures_tile
import random


class Map:
    def __init__(self, window, width, height, back_room, bonus):
        self.window = window
        self.PLATFORM_WIDTH = width * (1 / 25)
        self.PLATFORM_HEIGHT = height * (1 / 15)
        self.textures = Textures_tile()  # Загрузка всех текстур
        self.tileData = self.textures.tileData  #
        self.texture_room = self.textures.texture_room  #
        self.wall_positions = []  # Коллизии
        self.clear = False
        self.room_sides = {
            1: "up",
            2: "left",
            3: "right",
            4: "down",
        }
        self.bonus = bonus
        self.rand_side = self.room_sides[random.randint(1, 4)]
        self.generate_room(self.tileData, back_room)
        self.generate_floor(self.tileData)
        self.last_tick = pg.time.get_ticks()
        self.count_enemy_current = random.randint(3, 6)
        self.count_enemy = 0
        self.count_flag = False
        self.next_room = ""
        self.item_pick_up = False
        self.get_pressed = False
        self.random_attack_percent = random.randint(1, 3)

    def map_build(self, surface):  # Отображает все тайлы: текстуры
        self.wall_positions = []
        self.i = self.PLATFORM_WIDTH * 3
        self.j = self.PLATFORM_HEIGHT
        for row in self.tileData:
            for col in row:
                if col == "U":  # Стена фон
                    pf = self.textures.texture_room["wall"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "1":  # Пол фон
                    pf = self.textures.texture_room[f"floor_1"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "2":  # Пол фон
                    pf = self.textures.texture_room[f"floor_2"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "3":  # Пол фон
                    pf = self.textures.texture_room[f"floor_3"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "4":  # Пол фон
                    pf = self.textures.texture_room[f"floor_4"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "5":  # Пол фон
                    pf = self.textures.texture_room[f"floor_5"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                elif col == "d":  # Нижний край коллизия
                    pf = self.textures.texture_room[f"border_up_1"]
                    pf = pg.transform.rotate(pf, 180)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "g":  # Верхий край коллизия
                    pf = self.textures.texture_room[f"border_up_1"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "lg":  # Левый край коллизия
                    pf = self.textures.texture_room[f"border_up_1"]
                    pf = pg.transform.rotate(pf, 90)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "rg":  # Правый край коллизия
                    pf = self.textures.texture_room[f"border_up_1"]
                    pf = pg.transform.rotate(pf, -90)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    surface.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "l1":  # левый верхний угол коллизия
                    pf = self.textures.texture_room["angle_1"]
                    pf = pg.transform.flip(pf, True, False)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "r1":  # верхний правый угол коллизия
                    pf = self.textures.texture_room["angle_1"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "l2":  # Левый нижний угол коллизия
                    pf = self.textures.texture_room["angle_2"]
                    pf = pg.transform.flip(pf, True, False)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "r2":  # Правый нижний угол коллизия
                    pf = self.textures.texture_room["angle_2"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                elif col == "s1":  # Пол тень от двух стены фон
                    pf = self.textures.texture_room["floor_side_1"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s2":  # Пол тень от левой стены фон
                    pf = self.textures.texture_room["floor_side_2"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s3":  # Пол тень внутреннего угла стен фон
                    pf = self.textures.texture_room["floor_side_3"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s4":  # Пол тень от верхней стены фон
                    pf = self.textures.texture_room["floor_side_up"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s5":  # Пол медленно появляющаяся тень от верхней стены фон
                    pf = self.textures.texture_room["floor_side_continue"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s6":  # Пол медленно появляющаяся тень от верхней стены фон
                    pf = self.textures.texture_room["floor_side_continue"]
                    pf = pg.transform.flip(pf, False, True)
                    pf = pg.transform.rotate(pf, -90)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "s7":  # Пол тень от левой стены фон
                    pf = self.textures.texture_room["floor_side_up"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    pf = pg.transform.rotate(pf, 90)
                    self.window.blit(pf, (self.i, self.j))
                elif col == "c1":  # Угол краёф карты вне зоны игрока
                    pf = self.textures.texture_room["border_corner"]
                    pf = pg.transform.rotate(pf, 180)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "c2":  # Угол краёф карты вне зоны игрока
                    pf = self.textures.texture_room["border_corner"]
                    pf = pg.transform.rotate(pf, -90)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "c3":  # Угол краёф карты вне зоны игрока
                    pf = self.textures.texture_room["border_corner"]
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                elif col == "c4":  # Угол краёф карты вне зоны игрока
                    pf = self.textures.texture_room["border_corner"]
                    pf = pg.transform.rotate(pf, 90)
                    pf = pg.transform.scale(pf, (self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                    self.window.blit(pf, (self.i, self.j))
                    self.wall_positions.append(pg.Rect(self.i, self.j, self.PLATFORM_WIDTH, self.PLATFORM_HEIGHT))
                self.i += self.PLATFORM_WIDTH
            self.j += self.PLATFORM_HEIGHT
            self.i = self.PLATFORM_WIDTH * 3

    def generate_floor(self, tilemap):
        for i in range(len(tilemap)):
            for j in range(len(tilemap[i])):
                if tilemap[i][j] == ' ':
                    weights = [70, 5, 2, 1, 3]
                    rand = random.choices(range(1, 6), weights=weights)[0]
                    tilemap[i][j] = str(rand)

    def generate_room(self, tilemap, back_room):
        self.rand_side = self.room_sides[random.randint(1, 4)]
        if self.rand_side == back_room:
            while self.rand_side == back_room:
                self.rand_side = self.room_sides[random.randint(1, 4)]
        self.side_room(tilemap, self.rand_side, back_room)

    def stage_clear(self, enemy, index):
        if self.count_flag == False:
            self.count_enemy_current = random.randint(3, 6)
            self.count_flag = True
        if index != 0 and self.clear == False and self.count_enemy <= self.count_enemy_current:
            current_time = pg.time.get_ticks()
            if current_time - self.last_tick > 300 and self.bonus > 4 :
                enemy.spawn_enemy()
                self.count_enemy += 1
                self.last_tick = pg.time.get_ticks()

    def side_room(self, tilemap, next_room, back_room):
        if next_room == "up" or back_room == "up":
            tilemap[0][7] = 'l1'
            tilemap[0][8] = 's2'
            tilemap[0][9] = ' '
            tilemap[0][10] = ' '
            tilemap[0][11] = 'r1'
            tilemap[1][8] = 's2'
            tilemap[1][9] = ' '
            tilemap[1][10] = ' '
            tilemap[2][7] = 's4'
            tilemap[2][8] = 's1'
            tilemap[2][9] = ' '
            tilemap[2][10] = ' '
            tilemap[2][11] = 's5'
        if next_room == "down" or back_room == "down":
            tilemap[11][7] = 'l2'
            tilemap[11][8] = ' '
            tilemap[11][9] = ' '
            tilemap[11][10] = ' '
            tilemap[11][11] = 'r2'
        if next_room == "left" or back_room == "left":
            tilemap[3][0] = 'l1'
            tilemap[4][0] = 'U'
            tilemap[5][0] = 's4'
            tilemap[6][0] = ' '
            tilemap[7][0] = ' '
            tilemap[8][0] = 'l2'
            tilemap[5][1] = 's1'
            tilemap[6][1] = ' '
            tilemap[7][1] = ' '
            tilemap[8][1] = 's6'
            tilemap[9][1] = 's7'
            tilemap[10][1] = 'l2'
        if next_room == "right" or back_room == "right":
            tilemap[3][18] = 'r1'
            tilemap[4][18] = 'U'
            tilemap[5][18] = 's5'
            tilemap[6][18] = ' '
            tilemap[7][18] = ' '
            tilemap[8][18] = 'r2'

