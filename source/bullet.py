import pygame as pg
import math
import os
import random


class Bullet:
    def __init__(self, x, y):
        player_image_path = os.path.join(os.getcwd(), "assets", "material",
                                         "player_sprite")
        self.arrow = pg.image.load(os.path.join(player_image_path, "arrow.png"))
        self.new_height = 8
        self.new_width = 54
        self.arrow = pg.transform.scale(self.arrow, (self.new_width, self.new_height))
        self.rect = self.arrow.get_rect()
        self.rotated_arrow_image = self.arrow
        self.rotated_arrow_rect = self.arrow.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.arrow_speed = 2000
        self.angle = 0.0
        self.direction_with_offset = (0, 0)
        self.arrow_dx = 0.0
        self.arrow_dy = 0.0
        self.tr = False
        self.arrows = []
        self.count = 0
        self.last_arrow_time = 0

    def shoot_arrow(self, dt):
        self.rect.move_ip(self.arrow_speed * dt * self.direction_with_offset[0],
                          self.arrow_speed * dt * self.direction_with_offset[1])
        self.rotated_arrow_rect.centerx = self.rect.centerx - 17
        self.rotated_arrow_rect.centery = self.rect.centery + 2

    def player_rect(self, angle):
        if pg.mouse.get_pressed()[0]:
            self.tr = False
        else:
            if self.count < 1:
                mouse_pos = pg.mouse.get_pos()
                dx = mouse_pos[0] - self.rect.centerx + 16
                dy = mouse_pos[1] - self.rect.centery - 2
                dist = math.sqrt(dx ** 2 + dy ** 2)
                direction = (dx / dist, dy / dist)
                random_offset = pg.Vector2(random.uniform(-0.09, 0.09), random.uniform(-0.05, 0.05))
                self.direction_with_offset = pg.Vector2(direction) + random_offset
                self.direction_with_offset.normalize_ip()
                self.rotated_arrow_image = pg.transform.rotate(self.arrow, angle)
                self.rotated_arrow_rect = self.rotated_arrow_image.get_rect()
                self.count += 1

    def spawn_arrow(self, rect):
        if pg.time.get_ticks() - self.last_arrow_time > 280:
            self.last_arrow_time = pg.time.get_ticks()
            new_arrow = Bullet(rect[0] + 41, rect[1] + 48)
            self.arrows.append(new_arrow)

    def draw(self, window, angle, dt):
        self.player_rect(angle)
        self.shoot_arrow(dt)
        window.blit(self.rotated_arrow_image, self.rotated_arrow_rect)

    def update_arrow(self, window, player_angle, dt):
        for arrow in self.arrows:
            arrow.draw(window, player_angle, dt)
