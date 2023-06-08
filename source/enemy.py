import pygame as pg
import math
import random
from textures import Textures_enemy
from textures import Textures_Hud_Sound
import os


class Bullet:
    def __init__(self, enemy_rect, player_x, player_y):
        material_image_path = os.path.join(os.getcwd(), "assets", "material")
        self.original_image = pg.image.load(os.path.join(material_image_path, "entity", "enemy_bullet.png"))
        self.original_image = pg.transform.scale(self.original_image, (20, 20))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = enemy_rect.x
        self.rect.y = enemy_rect.y
        self.enemy_rect = enemy_rect
        self.speed = 350
        self.direction = 0
        self.target_x = player_x
        self.target_y = player_y
        self.direction = math.atan2(player_y - self.enemy_rect.y, player_x - self.enemy_rect.x)
        self.angle = 0

    def update(self, dt):
        self.rect.x += self.speed * dt * math.cos(self.direction)
        self.rect.y += self.speed * dt * math.sin(self.direction)

    def draw(self, window):
        rotated_image = pg.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        window.blit(rotated_image, rotated_rect)

        self.angle += 1


class Enemy:
    def __init__(self):
        self.x = random.randint(320, 1280)
        self.y = random.randint(240, 660)
        self.clock = pg.time.Clock()
        self.speed = 200
        self.desired_distance = 130
        self.enemies = []
        self.enemy_hp = 9.0
        self.percent_damage = 1.0
        self.textures = Textures_enemy()
        self.sound = Textures_Hud_Sound()
        self.enemy = self.textures.fly_entity["fly_1"]
        self.rect = pg.Rect(self.x, self.y, 30, 30)
        self.last_update_time = pg.time.get_ticks()
        self.index = 1
        self.player_x = 0
        self.player_y = 0
        self.timer = 1.0
        self.distance_to_target = 0
        self.target_position = (0, 0)
        self.enemy_bullets = []
        self.k = 10
        self.sound_blaster = self.sound.sound["shoot_blaster"]
        self.sound_blaster.set_volume(0.6)
        self.image = self.textures.fly_entity["bullet"]
        self.sound_shoot_enemy = self.sound.sound["shoot_enemy"]
        self.image_hit = self.textures.fly_entity["hit_by_enemy"]
        self.sound_shoot_player = self.sound.sound["enemy_shoot_player"]
        self.shadow = pg.Surface((200, 100), pg.SRCALPHA)
        pg.draw.ellipse(self.shadow, (0, 0, 0, 160), (0, 0, 30, 15))
        self.co = False
        self.spawned = False
        self.move = True
        self.last_move = pg.time.get_ticks()
        self.pre_rect = self.rect.copy()
        self.last_time = pg.time.get_ticks()

    def move_towards_player(self, dt, player_x, player_y):
        self.pre_rect = self.rect.copy()
        if self.spawned == True:
            self.player_x = player_x
            self.player_y = player_y
            self.distance_from_player = ((player_x - self.rect.x) ** 2 + (player_y - self.rect.y) ** 2) ** 0.5
            if self.distance_from_player < self.desired_distance - 30:
                angle = math.atan2(self.rect.y - player_y, self.rect.x - player_x)
                self.rect.x += self.speed * dt * math.cos(angle)
                self.rect.y += self.speed * dt * math.sin(angle)
            elif self.distance_from_player > self.desired_distance + 200:
                angle = math.atan2(player_y - self.rect.y, player_x - self.rect.x)
                self.rect.x += self.speed * dt * math.cos(angle)
                self.rect.y += self.speed * dt * math.sin(angle)
            elif self.distance_from_player < self.desired_distance:
                pass
            elif self.distance_from_player > self.desired_distance + 190:
                pass
            elif self.distance_from_player > self.desired_distance < self.desired_distance + 200:
                if self.timer <= 0 or self.distance_to_target < 10:
                    # выбираем случайную точку назначения в пределах допустимого расстояния
                    random_distance = random.uniform(self.desired_distance + 50, self.desired_distance + 150)
                    random_angle = random.uniform(0, 2 * math.pi)
                    target_x = player_x + random_distance * math.cos(random_angle)
                    target_y = player_y + random_distance * math.sin(random_angle)
                    self.target_position = (target_x, target_y)
                    self.timer = 1.0  # таймер на 1 секунду
                else:
                    target_x, target_y = self.target_position
                    angle = math.atan2(target_y - self.rect.y, target_x - self.rect.x)
                    self.rect.x += (self.speed - 100) * dt * math.cos(angle)
                    self.rect.y += (self.speed - 100) * dt * math.sin(angle)
                self.distance_to_target = ((target_x - self.rect.x) ** 2 + (target_y - self.rect.y) ** 2) ** 0.5

    def spawn_enemy(self):
        new_enemy = Enemy()
        self.enemies.append(new_enemy)

    def fly_anim(self, player):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update_time >= 62.5:
            if self.spawned == False:
                self.spawn()
                self.last_update_time = current_time
            else:
                self.enemy = self.textures.fly_entity[f"fly_{self.index}"]
                self.enemy = pg.transform.scale(self.enemy, (60, 60))
                if self.index == 4:
                    self.index = 0
                self.index += 1
                self.last_update_time = current_time

    def draw_hp(self, surface, player):
        surface.blit(self.enemy,
                     (self.rect.x - self.enemy.get_width() // 2, self.rect.y - self.enemy.get_height() // 2))
        surface.blit(self.shadow, (self.rect.x - 13, self.rect.y + 15))
        health_bar_width = 10
        health_bar_height = 4
        health_bar_x = self.rect.x - health_bar_width * 1.3
        health_bar_y = self.rect.y - 20
        if player.player_hp > 1:
            pg.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width * 3, health_bar_height))
            remaining_health_bar_width = health_bar_width * (self.enemy_hp / 3)
            pg.draw.rect(surface, (0, 255, 0),
                         (health_bar_x, health_bar_y, remaining_health_bar_width, health_bar_height))

    def hit(self, bullet, weapon, hud):
        current_time = pg.time.get_ticks()
        if weapon.current_use_weapon == 1:
            for enemy in self.enemies:
                for arrow in bullet.arrows:
                    if enemy.rect.colliderect(arrow.rect):
                        self.sound_shoot_enemy.play()
                        bullet.arrows.remove(arrow)
                        enemy.enemy_hp -= 3 * self.percent_damage
                        enemy.move = False
                        self.last_move = pg.time.get_ticks()
                        if enemy.enemy_hp <= 0:
                            self.enemies.remove(enemy)
                            hud.score += 30
                if current_time - self.last_move > 300:
                    enemy.move = True

    def update(self, player, dt, character):
        if player.player_hp > 1:
            for enemy in self.enemies:
                enemy.update_bullets(dt)
                enemy.enemy_hit_player(player, character)
                if enemy.move:
                    enemy.move_towards_player(dt, player.rect.x + 12, player.rect.y + 12)
                    enemy.add_bullet()

    def render(self, player, window):
        for enemy in self.enemies:
            enemy.draw_hp(window, player)
            enemy.fly_anim(player)
            enemy.draw_bullets(window)

    def spawn(self):
        self.enemy = self.textures.fly_entity[f"spawn_{self.index}"]
        self.enemy = pg.transform.scale(self.enemy, (60, 60))
        if self.index == 5:
            self.spawned = True
            self.index = 0
        self.index += 1

    def add_bullet(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_time > 1000:
            self.sound_blaster.play()
            new_bullet = Bullet(self.rect, self.player_x, self.player_y)
            self.enemy_bullets.append(new_bullet)
            self.last_time = pg.time.get_ticks()

    def enemy_hit_player(self, player, character):
        for bullet in self.enemy_bullets:
            if bullet.rect.colliderect(character):
                self.enemy_bullets.remove(bullet)
                self.sound_shoot_player.play()
                player.player_hp -= 1

    def update_bullets(self, dt):
        for bullet in self.enemy_bullets:
            bullet.update(dt)

    def draw_bullets(self, window):
        for bullet in self.enemy_bullets:
            bullet.draw(window)
