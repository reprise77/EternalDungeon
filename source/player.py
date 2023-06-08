import pygame as pg
import math
from textures import Textures_player
from textures import Textures_Hud_Sound


class Player:
    def __init__(self, width, height):
        self.textures = Textures_player()
        self.textures_sound = Textures_Hud_Sound()
        self.direction = None
        self.flag_move_side = False
        self.new_width = 74
        self.new_height = 74
        self.angle = 0
        self.animation_index = 0
        self.animation_delay = 0.16
        self.rect = self.textures.images_stay_down["stay_down_1"].get_rect()
        self.rect.x = width
        self.rect.y = height
        self.shadow_rect = self.rect
        self.speed = 400
        self.base_speed = self.speed
        self.speed_diagonal = math.sqrt(pow(self.base_speed, 2) / 2)
        self.base_speed_diagonal = self.speed_diagonal
        self.last_frame_time = 0
        self.image = self.textures.images_move_right["move_right_1"].copy()
        self.sprite_index = 0
        self.next_anim_time = 0
        self.dx = 0
        self.dy = 0
        self.player_hp = 11
        self.player_dead = False
        self.count_do = False
        self.shadow = pg.Surface((200, 100), pg.SRCALPHA)
        pg.draw.ellipse(self.shadow, (0, 0, 0, 160), (0, 0, 40, 15))
        self.heal = 3
        self.heali = False
        self.sound_steps = self.textures_sound.sound["steps"]
        self.sound_heal = self.textures_sound.sound["heal"]
        self.sound_heal.set_volume(0.2)
        self.sound_steps.set_volume(0.4)
        self.flag_steps = False

        for key in self.textures.images_move_right:
            self.textures.images_move_right[key] = pg.transform.scale(self.textures.images_move_right[key],
                                                                      (self.new_width, self.new_height))
        for key in self.textures.images_move_left:
            self.textures.images_move_left[key] = pg.transform.scale(self.textures.images_move_left[key],
                                                                     (self.new_width, self.new_height))
        for key in self.textures.images_move_up:
            self.textures.images_move_up[key] = pg.transform.scale(self.textures.images_move_up[key],
                                                                   (self.new_width, self.new_height))
        for key in self.textures.images_move_down:
            self.textures.images_move_down[key] = pg.transform.scale(self.textures.images_move_down[key],
                                                                     (self.new_width, self.new_height))
        for key in self.textures.images_stay_down:
            self.textures.images_stay_down[key] = pg.transform.scale(self.textures.images_stay_down[key],
                                                                     (self.new_width, self.new_height))
        for key in self.textures.images_stay_up:
            self.textures.images_stay_up[key] = pg.transform.scale(self.textures.images_stay_up[key],
                                                                   (self.new_width, self.new_height))
        for key in self.textures.images_stay_left:
            self.textures.images_stay_left[key] = pg.transform.scale(self.textures.images_stay_left[key],
                                                                     (self.new_width, self.new_height))
        for key in self.textures.images_stay_right:
            self.textures.images_stay_right[key] = pg.transform.scale(self.textures.images_stay_right[key],
                                                                      (self.new_width, self.new_height))
            # Ходьба


    def handle_movement(self, keys, dt):
        if self.player_hp > 1:
            if keys[pg.K_a] and keys[pg.K_w]:
                self.rect.x -= self.speed_diagonal * dt
                self.rect.y -= self.speed_diagonal * dt
            elif keys[pg.K_a] and keys[pg.K_s]:
                self.rect.x -= self.speed_diagonal * dt
                self.rect.y += self.speed_diagonal * dt
            elif keys[pg.K_d] and keys[pg.K_w]:
                self.rect.x += self.speed_diagonal * dt
                self.rect.y -= self.speed_diagonal * dt
            elif keys[pg.K_d] and keys[pg.K_s]:
                self.rect.x += self.speed_diagonal * dt
                self.rect.y += self.speed_diagonal * dt
            elif keys[pg.K_a]:
                self.rect.x -= self.speed * dt
            elif keys[pg.K_d]:
                self.rect.x += self.speed * dt
            elif keys[pg.K_w]:
                self.rect.y -= self.speed * dt
            elif keys[pg.K_s]:
                self.rect.y += self.speed * dt
            if any(keys[key] for key in [pg.K_a, pg.K_d, pg.K_w, pg.K_s]):
                if self.sound_steps.get_num_channels() == 0:
                    self.sound_steps.play(-1)
            else:
                self.sound_steps.fadeout(400)

            self.shadow_rect = self.rect
        else:
            self.sound_steps.fadeout(400)

    def handle_mouse_rotation(self, keys):
        mouse_pos = pg.mouse.get_pos()
        self.dx = mouse_pos[0] - self.rect.centerx - (self.new_width / 2)
        self.dy = mouse_pos[1] - self.rect.centery - (self.new_height / 2)
        self.angle = math.degrees(math.atan2(-self.dy, self.dx))
        # Отвечает за поворот игрока в направлении курсора по осям x, y
        if abs(self.dx) > abs(self.dy):
            if self.dx > 0:
                if keys[pg.K_d]:
                    pass
                else:
                    if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                        self.animation_index = (self.animation_index + 1) % len(
                            self.textures.animation_frames_stay_right)
                        self.last_frame_time = pg.time.get_ticks()
                        self.image = self.textures.images_stay_right[
                            self.textures.animation_frames_stay_right[self.animation_index]]
                self.animation_frames = self.textures.animation_frames_move_right
                self.direction = "right"
                self.handle_animation(keys)
            else:
                if keys[pg.K_a]:
                    pass
                else:
                    if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                        self.animation_index = (self.animation_index + 1) % len(
                            self.textures.animation_frames_stay_left)
                        self.last_frame_time = pg.time.get_ticks()
                        self.image = self.textures.images_stay_left[
                            self.textures.animation_frames_stay_left[self.animation_index]]
                self.animation_frames = self.textures.animation_frames_move_left
                self.direction = "left"
                self.handle_animation(keys)
        else:
            if self.dy > 0:
                if keys[pg.K_s]:
                    pass
                else:
                    if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                        self.animation_index = (self.animation_index + 1) % len(
                            self.textures.animation_frames_stay_down)
                        self.last_frame_time = pg.time.get_ticks()
                        self.image = self.textures.images_stay_down[
                            self.textures.animation_frames_stay_down[self.animation_index]]
                self.animation_frames = self.textures.animation_frames_move_down
                self.direction = "down"
                self.handle_animation(keys)
            else:
                if keys[pg.K_w]:
                    pass
                else:
                    if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                        self.animation_index = (self.animation_index + 1) % len(self.textures.animation_frames_stay_up)
                        self.last_frame_time = pg.time.get_ticks()
                        self.image = self.textures.images_stay_up[
                            self.textures.animation_frames_stay_up[self.animation_index]]
                self.animation_frames = self.textures.animation_frames_move_up
                self.direction = "up"
                self.handle_animation(keys)
                # Все анимации связанные с игроком

    def handle_animation(self, keys):
        if keys[pg.K_a]:
            if self.direction == "left":
                if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                    self.animation_index = (self.animation_index + 1) % len(self.textures.animation_frames_move_left)
                    self.last_frame_time = pg.time.get_ticks()
                    self.image = self.textures.images_move_left[
                        self.textures.animation_frames_move_left[self.animation_index]]
        elif keys[pg.K_d]:
            if self.direction == "right":
                if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                    self.animation_index = (self.animation_index + 1) % len(self.textures.animation_frames_move_right)
                    self.last_frame_time = pg.time.get_ticks()
                    self.image = self.textures.images_move_right[
                        self.textures.animation_frames_move_right[self.animation_index]]
        elif keys[pg.K_w]:
            if self.direction == "up":
                if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                    self.animation_index = (self.animation_index + 1) % len(self.textures.animation_frames_move_up)
                    self.last_frame_time = pg.time.get_ticks()
                    self.image = self.textures.images_move_up[
                        self.textures.animation_frames_move_up[self.animation_index]]
        elif keys[pg.K_s]:
            if self.direction == "down":
                if pg.time.get_ticks() - self.last_frame_time > self.animation_delay * 1000:
                    self.animation_index = (self.animation_index + 1) % len(self.textures.animation_frames_move_down)
                    self.last_frame_time = pg.time.get_ticks()
                    self.image = self.textures.images_move_down[
                        self.textures.animation_frames_move_down[self.animation_index]]

    def handle_speed(self, keys):
        if keys[pg.K_LSHIFT]:
            self.speed = self.base_speed * 1.3
            self.speed_diagonal = self.base_speed_diagonal * 1.3
        else:
            self.speed = self.base_speed
            self.speed_diagonal = self.base_speed_diagonal

    def dead_player(self):
        if self.player_hp <= 1:
            current_time = pg.time.get_ticks()
            if current_time - self.last_frame_time > 500:
                self.sprite_index += 1
                if self.count_do == False:
                    mouse_pos = pg.mouse.get_pos()
                    self.dx = mouse_pos[0] - self.rect.centerx - (self.new_width / 2)
                    self.count_do = True
                if self.sprite_index == 5:
                    self.image = self.textures.images_death["player_death_4"]
                    self.sprite_index -= 1
                    self.player_dead = True
                    if self.dx < 0:
                        self.image = pg.transform.flip(self.image, True, False)
                    self.image = pg.transform.scale(self.image, (self.new_width, self.new_height))
                else:
                    self.image = self.textures.images_death[f"player_death_{self.sprite_index}"]
                    if self.dx < 0:
                        self.image = pg.transform.flip(self.image, True, False)
                    self.image = pg.transform.scale(self.image, (self.new_width, self.new_height))
                    self.last_frame_time = pg.time.get_ticks()

    def update(self, dt, keys):
        self.handle_movement(keys, dt)
        if self.player_hp > 1:
            self.handle_mouse_rotation(keys)
            self.handle_speed(keys)
            self.handle_animation(keys)
        else:
            self.dead_player()

    def healing(self, keys):
        if self.player_hp > 1:
            if keys[pg.K_x]:
                if self.player_hp < 11:
                    if not self.heali:
                        if self.heal != 0:
                            self.sound_heal.play()
                            self.heal -= 1
                            self.player_hp = 11
                            self.heali = True
            else:
                self.heali = False
