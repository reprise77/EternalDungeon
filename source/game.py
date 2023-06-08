import pygame as pg
import sys
import os
from textures import Textures_Hud_Sound
from player import Player
from enemy import Enemy
from bullet import Bullet
from hud import Hud
from weapon import Weapon
from menu import Menu
from map_generator import Map_generator
import random

pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
pg.mixer.music.load("eternal.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.2)


class Game:
    def __init__(self):
        pg.init()
        self.menu = Menu()
        self.weapon = Weapon()
        hud_directory = os.path.join(os.getcwd(), "assets", "material", "Hud")
        self.width, self.height = 1600, 900
        self.window = pg.display.set_mode((self.width, self.height), pg.DOUBLEBUF | pg.SWSURFACE)
        self.bg_color = pg.Color(38, 30, 51, 150)
        self.x = random.randint(300, 700)
        self.y = random.randint(300, 700)
        self.enemy = Enemy()  # Enemy
        self.textures = Textures_Hud_Sound()
        self.player = Player(self.width / 2 - 37, self.height / 2 - 37)  # Player
        self.bullet = Bullet(self.player.rect.x, self.player.rect.y)  # Bullet
        self.hud = Hud()
        pg.display.set_caption("EternalDungeon")
        icon = pg.image.load(os.path.join(hud_directory, "security.png"))
        pg.display.set_icon(icon)
        self.font = pg.font.Font("ThaleahFat.ttf", 28)
        self.clock = pg.time.Clock()
        self.objects = []
        self.sound_shoot_enemy = self.textures.sound["shoot_enemy"]
        self.character_rect = pg.Rect(0, 0, 0, 0)
        self.alpha = 0
        self.play_menu = True
        self.play_pause = False
        self.fullscreen = False
        self.triget = self.menu_f_t()
        self.generate_world = Map_generator(self.width, self.height, self.window)
        self.last_time = pg.time.get_ticks()
        self.dt = pg.time.get_ticks()
        self.cursor_image = self.textures.hud["cursor"]
        self.cursor_image = pg.transform.scale(self.cursor_image, (26, 26))
        pg.mouse.set_visible(False)
        self.cursor_rect = self.cursor_image.get_rect()
        self.prev_rect = self.player.rect.copy()
        self.sound_button = self.textures.sound["button"]

    def add_object(self, obj):
        self.objects.append(obj)

    def run(self):  # Главный цикл игры
        while True:
            self.triget = self.menu_f_t()
            if self.triget == False:
                self.handle_events()
                self.update()
                self.render()
                if self.play_pause == True:
                    self.menu.update(self.width, self.height, self.play_pause)
                    self.menu.render(self.play_pause)
            elif self.triget == True:
                self.handle_events()
                self.menu.update(self.width, self.height, self.play_pause)
                self.menu.render(self.play_pause)
            self.cursor_rect.center = pg.mouse.get_pos()
            self.window.blit(self.cursor_image, self.cursor_rect)

            pg.display.update()
            self.clock.tick(150)

    def handle_events(self):  # В процессе главного цикла считывает данные
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and self.play_menu == False:
                    if self.player.player_dead == True:
                        self.play_menu = True
                        self.player = Player(self.width / 2 - 42, self.height / 2 - 42)
                        self.weapon = Weapon()
                        self.enemy = Enemy()
                        self.generate_world = Map_generator(self.width, self.height, self.window)
                    else:
                        self.play_pause = not self.play_pause
                if event.key == pg.K_F11:
                    self.fullscreen = not self.fullscreen
                    self.fullscreen_mode()
            elif event.type == pg.VIDEORESIZE:
                self.player.rect.x = int(self.player.rect.x / self.width * event.w)
                self.player.rect.y = int(self.player.rect.y / self.height * event.h)
                self.fullscreen_mode()
                self.menu.fill_surface = pg.transform.scale(self.menu.fill_surface, (self.width, self.height))
            elif self.menu.is_clicked(event):
                if pg.mouse.get_pressed()[0]:
                    if self.play_menu == True or self.play_pause == True:
                        self.sound_button.play()
                        self.play_pause = False
                        self.play_menu = False
            elif self.menu.exit_clicked(event):
                if pg.mouse.get_pressed()[0]:
                    if self.play_menu == True or self.play_pause == True:
                        sys.exit()
            elif self.hud.screen_mode_clicked(event):
                if pg.mouse.get_pressed()[0]:
                    self.fullscreen = not self.fullscreen
                    self.fullscreen_mode()

    def update(self):  # Все обновляется по частоте FPS: 150 в секунду
        current_time = pg.time.get_ticks()
        self.dt = (current_time - self.last_time) / 1000.0
        keys = pg.key.get_pressed()
        self.prev_rect = self.player.rect.copy()
        self.player.healing(keys)
        character_rect = pg.Rect(self.player.rect.x + 30, self.player.rect.y + 10, 69, 84)
        if self.play_pause == False:
            self.player.update(self.dt, keys)
            self.weapon.update(self.player, keys)
            self.enemy.update(self.player, self.dt, character_rect)
        self.last_time = pg.time.get_ticks()
        character_rect = pg.Rect(self.player.rect.x + 30, self.player.rect.y + 10, 69, 84)
        if self.weapon.shoot == True:
            self.bullet.spawn_arrow(self.player.rect)
        if self.generate_world.check_collision(character_rect):
            self.player.rect = self.prev_rect
        if self.player.player_hp <= 1:
            self.hud.game_over_player_move(self.player, self.weapon, self.width, self.height)
        self.generate_world.arrow_collide_wall(self.bullet)
        self.generate_world.enemy_collide_wall(self.enemy)
        self.weapon.arrow_fix(self.player, self.bullet)
        self.enemy.hit(self.bullet, self.weapon, self.hud)
        self.menu.wallpaper(self.dt, self.player)

    def render(self):  # Выводит все на экран
        self.window.fill(self.bg_color)
        character_rect = pg.Rect(self.player.rect.x + 30, self.player.rect.y + 10, 69, 84)
        self.generate_world.generate_world(self.window, character_rect, self.player, self.enemy, self.prev_rect)
        self.enemy.render(self.player, self.window)
        if self.player.player_hp <= 1:
            self.window.fill(self.bg_color)
        self.interface()
        self.bullet.update_arrow(self.window, self.player.angle, self.dt)
        self.weapon.weapon_look(self.window, self.player, self.enemy, self.hud)
        self.hud.heal_idicate(self.player.player_hp, self.width, self.height, self.window)
        self.hud.screen_mode(self.fullscreen, self.window, self.width)

    def menu_f_t(self):
        return self.play_menu

    def fullscreen_mode(self):
        if self.fullscreen == True:
            self.window = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN | pg.DOUBLEBUF | pg.SWSURFACE)
        else:
            self.window = pg.display.set_mode((self.width, self.height), pg.DOUBLEBUF | pg.SWSURFACE)

    def interface(self):
        fps_text = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, pg.Color('white'))
        heal_user = self.font.render("Heal press X : " + str(int(self.player.heal)), True, pg.Color('white'))
        self.window.blit(fps_text, (10, 10))
        self.window.blit(heal_user, (self.width - 200, self.height - 100))
        self.hud.score_bar(self.window)
        for star in self.menu.stars:
            pg.draw.circle(self.window, (160, 160, 160), star[:2], 1)
