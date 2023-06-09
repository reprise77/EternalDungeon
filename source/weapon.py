import pygame as pg
import math
import os
from textures import Textures_weapon
from textures import Textures_Hud_Sound


class Weapon:
    def __init__(self):
        self.player_image_path = os.path.join(os.getcwd(), "assets", "material",
                                              "player_sprite")
        self.textures = Textures_weapon()
        self.sound_direct = Textures_Hud_Sound()
        self.dx = 0
        self.dy = 0
        self.image = self.textures.images_bow["bow_idle"]
        self.image_sword_1 = pg.image.load(os.path.join(self.player_image_path, "sword_1.png"))
        self.image_sword_2 = pg.image.load(os.path.join(self.player_image_path, "sword_2.png"))
        self.image_center = self.image.get_rect()
        self.rotated_image = self.image
        self.image_rect = (0, 0)
        self.width, self.height = 148, 148
        self.sprite_index = 0
        self.shoot = False
        self.weapon = False
        self.sound = self.sound_direct.sound["pulling_arrow"]
        self.sound_shoot = self.sound_direct.sound["shoot_arrow"]
        self.sound.set_volume(0.2)
        self.sound_shoot.set_volume(0.4)
        self.animation_speed = 90
        self.animation_time = 0
        self.last_frame_time = 0
        self.count_weapon_sprite_crash = 0
        self.count_do = False
        self.sound_flag = False
        self.next_anim_time = 0
        self.current_use_weapon = 1
        self.rotate_sword_angle = 0
        self.flag = True
        self.distance = 45
        self.square_size = 110
        self.rotate = True
        self.sword_box = pg.Surface((self.square_size, self.square_size), pg.SRCALPHA)
        self.sword_box.fill((255, 255, 255, 0))
        self.sword_rect = self.sword_box.get_rect()
        self.hit = False
        self.last_time = pg.time.get_ticks()
        self.swing_sword = self.sound_direct.sound["swing_sword"]
        self.swing_sword_1 = self.sound_direct.sound["swing_sword_1"]
        self.swing_sword.set_volume(0.5)
        self.swing_sword_1.set_volume(0.5)
        self.sword_flag = False
        self.sword_flag_1 = False
        self.draw_sword_sound = self.sound_direct.sound["draw_sword"]
        self.draw_sword_sound.set_volume(0.7)
        self.draw_sword_flag = False

    def handle_mouse_rotation(self, player):
        mouse_pos = pg.mouse.get_pos()
        if self.rotate == True:
            self.dx = mouse_pos[0] - player.rect.centerx - (player.new_width / 2)
            self.dy = mouse_pos[1] - player.rect.centery - (player.new_height / 2)
        center = self.image.get_rect().center
        self.angle = math.degrees(math.atan2(-self.dy, self.dx)) + self.rotate_sword_angle
        if self.current_use_weapon == 1:
            self.image = pg.transform.scale(self.image, (self.width, self.height))
        elif self.current_use_weapon == 2:
            self.image = pg.transform.scale(self.image, (190, 190))
        if self.dx < 0 and self.current_use_weapon == 1:
            self.image = pg.transform.flip(self.image, False, True)
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        self.image_center = self.rotated_image.get_rect(center=center)
        self.image_rect = player.rect.copy()
        self.image_rect.x += self.image_center.x - center[0] + (player.new_width / 2) + (
                player.new_width / 6)  # Центральные координаты спрайта игрока
        self.image_rect.y += self.image_center.y - center[1] + (player.new_height / 2) + (player.new_height / 6)
        if self.dx < 0 and self.current_use_weapon == 1:
            self.image = pg.transform.flip(self.image, False, True)
            # Отвечает за поворот игрока в направлении курсора по осям x, y
        if abs(self.dx) > abs(self.dy):
            if self.dx > 0:
                self.weapon = False
            else:
                self.weapon = False
        else:
            if self.dy > 0:
                self.weapon = False
            else:
                self.weapon = True

    def handle_animation_bow(self):
        self.rotate = True
        if pg.mouse.get_pressed()[0]:
            if self.sound_flag == False:
                self.sound.play()
                self.sound_flag = True
            current_time = pg.time.get_ticks()
            if current_time >= self.next_anim_time:
                self.animation_time += current_time - self.next_anim_time
                self.next_anim_time = current_time + 1000 / self.animation_speed
                if self.sprite_index == 4:
                    sprite_index = 4
                    self.image = self.textures.images_bow[f"bow_{sprite_index}"]
                elif self.animation_time > 1000 / self.animation_speed:
                    self.sprite_index += 1
                    self.image = self.textures.images_bow[f"bow_{self.sprite_index}"]
                    self.animation_time = 0
        else:
            self.sound.stop()
            self.sound_flag = False  # Если же ЛКМ не зажат то сработает спрайт bow_shoot который будте работать 4 фрэйма, в процесе будет задержка в 150 мл секунд
            if self.sprite_index > 0:
                self.next_anim_time = pg.time.get_ticks()
                if self.sprite_index == 4:
                    self.bow = self.textures.images_bow["bow_shoot"]
                    self.shoot = True
                    self.sound_shoot.play()
                self.sprite_index -= 1
            elif self.sprite_index == 0:
                self.shoot = False
                self.animation_time = 0
                self.sprite_index = 0
                self.image = self.textures.images_bow["bow_idle"]

    def weapon_look(self, window, player, enemy, hud):
        if self.weapon == False:
            window.blit(player.shadow, (player.rect.x + player.new_width / 2.45, player.rect.y + player.new_height + 3))
            window.blit(player.image, player.rect.center)
            window.blit(self.rotated_image, self.image_rect)

        else:
            window.blit(player.shadow, (player.rect.x + player.new_width / 2.45, player.rect.y + player.new_height + 3))
            window.blit(self.rotated_image, self.image_rect)
            window.blit(player.image, player.rect.center)
        if self.current_use_weapon == 2:
            self.sword_hit_box(player, window, enemy, hud)
        else:
            self.sword_rect.x = 0
            self.sword_rect.y = 0

    def weapon_crash(self, player):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_time > 200:
            self.count_weapon_sprite_crash += 1
            if self.count_do == False:
                mouse_pos = pg.mouse.get_pos()
                self.dx = mouse_pos[0] - player.rect.centerx - (player.new_width / 2)
                self.dy = mouse_pos[1] - player.rect.centery - (player.new_height / 2)
                self.angle = math.degrees(math.atan2(-self.dy, self.dx))
                self.count_do = True
            if self.count_weapon_sprite_crash == 6:
                self.image = self.textures.images_bow["bow_death_5"]
                self.rotated_image = pg.transform.rotate(self.image, self.angle)
                self.count_weapon_sprite_crash -= 1
            else:
                self.image = self.textures.images_bow[f"bow_death_{self.count_weapon_sprite_crash}"]
                self.image = pg.transform.scale(self.image, (self.width, self.height))
                self.rotated_image = pg.transform.rotate(self.image, self.angle)
                self.last_frame_time = pg.time.get_ticks()

    def update(self, player, keys, enemy):
        if player.player_hp > 1:
            self.deflect_bullet(enemy, player)
            self.handle_mouse_rotation(player)
            self.use_weapon(keys)
            if self.current_use_weapon == 1:
                self.handle_animation_bow()
                self.draw_sword_flag = False
            elif self.current_use_weapon == 2:
                self.handle_animation_sword()
                if not self.draw_sword_flag:
                    self.draw_sword_sound.play()
                    self.draw_sword_flag = True
        else:
            self.weapon_crash(player)

    def handle_animation_sword(self):
        current_time = pg.time.get_ticks()
        if pg.mouse.get_pressed()[0]:
            if current_time - self.next_anim_time > 280:
                self.next_anim_time = pg.time.get_ticks()
                self.flag = not self.flag
        self.rotate_sword()
        if self.current_use_weapon == 2:
            if self.rotate_sword_angle == 0:
                self.image = self.image_sword_1
            elif self.rotate_sword_angle == -180:
                self.image = self.image_sword_2

    def rotate_sword(self):
        if self.flag == True and self.rotate_sword_angle != 0:
            self.sword_flag_1 = False
            if not self.sword_flag:
                self.swing_sword.play()
                self.sword_flag = True
            self.rotate_sword_angle += 15
        elif self.flag == False and self.rotate_sword_angle != -180:
            self.sword_flag = False
            if not self.sword_flag_1:
                self.swing_sword_1.play()
                self.sword_flag_1 = True
            self.rotate_sword_angle -= 15

    def use_weapon(self, keys):
        if keys[pg.K_1]:
            self.current_use_weapon = 1
            self.rotate_sword_angle = 0
        elif keys[pg.K_2]:
            self.current_use_weapon = 2

    def sword_hit_box(self, player, window, enemys, hud):
        current_time = pg.time.get_ticks()
        player_pos = pg.Rect(player.rect.x + 50, player.rect.y + 50, 1, 1)
        cursor_pos = pg.mouse.get_pos()
        dx = cursor_pos[0] - player_pos[0]
        dy = cursor_pos[1] - player_pos[1]
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            normalized_dx = dx / magnitude
            normalized_dy = dy / magnitude
            square_pos = [
                int(player_pos[0] + normalized_dx * self.distance),
                int(player_pos[1] + normalized_dy * self.distance)
            ]
        else:
            square_pos = player_pos
        self.sword_rect.x = square_pos[0] - self.square_size // 2
        self.sword_rect.y = square_pos[1] - self.square_size // 2
        window.blit(self.sword_box, (square_pos[0] - self.square_size // 2, square_pos[1] - self.square_size // 2))
        if pg.mouse.get_pressed()[0]:
            if current_time - self.last_time > 350:
                for enemy in enemys.enemies:
                    if enemy.rect.colliderect(self.sword_rect):
                        enemy.enemy_hp -= 2 * enemys.percent_damage
                        enemys.sound_shoot_enemy.play()
                        if enemy.enemy_hp <= 0:
                            enemys.enemies.remove(enemy)
                            hud.score += 40
                        self.last_time = pg.time.get_ticks()


    def arrow_fix(self, player, bullet):
        if player.player_hp <= 1 or self.current_use_weapon != 1:
            for arrow in bullet.arrows:
                bullet.arrows.remove(arrow)

    def deflect_bullet(self, enemys, player):
        for enemy in enemys.enemies:
            for bullet in enemy.enemy_bullets:
                if bullet.rect.colliderect(enemy.rect) and bullet.deflect == True:
                    enemy.enemy_hp -= 1
                    if enemy.enemy_hp <= 0:
                        enemys.enemies.remove(enemy)
                    enemy.sound_shoot_enemy.play()
                    enemy.enemy_bullets.remove(bullet)
                cursor_pos = pg.mouse.get_pos()
                for bullet in enemy.enemy_bullets:
                    if pg.mouse.get_pressed()[0] and bullet.rect.colliderect(self.sword_rect):
                        bullet.direction = math.atan2(cursor_pos[1] - player.rect.y - 2, cursor_pos[0] - player.rect.x - 50)
                        bullet.deflect = True







