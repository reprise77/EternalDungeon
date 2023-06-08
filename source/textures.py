import pygame as pg
import os


class Textures_player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image_path = os.path.join(os.getcwd(), "assets", "material",
                                         "player_sprite")  # Директория всех спрайтов игрока и лука
        self.images_move_right = {
            "move_right_1": pg.image.load(os.path.join(player_image_path, "player_move_right_1.png")),
            "move_right_2": pg.image.load(os.path.join(player_image_path, "player_move_right_2.png")),
            "move_right_3": pg.image.load(os.path.join(player_image_path, "player_move_right_3.png")),
            "move_right_4": pg.image.load(os.path.join(player_image_path, "player_move_right_4.png")),
            "move_right_5": pg.image.load(os.path.join(player_image_path, "player_move_right_5.png")),
            "move_right_6": pg.image.load(os.path.join(player_image_path, "player_move_right_6.png")),
        }  # спрайты ходьбы вправо
        self.images_move_left = {
            "move_left_1": pg.image.load(os.path.join(player_image_path, "player_move_left_1.png")),
            "move_left_2": pg.image.load(os.path.join(player_image_path, "player_move_left_2.png")),
            "move_left_3": pg.image.load(os.path.join(player_image_path, "player_move_left_3.png")),
            "move_left_4": pg.image.load(os.path.join(player_image_path, "player_move_left_4.png")),
            "move_left_5": pg.image.load(os.path.join(player_image_path, "player_move_left_5.png")),
            "move_left_6": pg.image.load(os.path.join(player_image_path, "player_move_left_6.png")),
        }  # спрайты ходьбы влево
        self.images_move_up = {
            "move_up_1": pg.image.load(os.path.join(player_image_path, "player_move_up_1.png")),
            "move_up_2": pg.image.load(os.path.join(player_image_path, "player_move_up_2.png")),
            "move_up_3": pg.image.load(os.path.join(player_image_path, "player_move_up_3.png")),
            "move_up_4": pg.image.load(os.path.join(player_image_path, "player_move_up_4.png")),
            "move_up_5": pg.image.load(os.path.join(player_image_path, "player_move_up_5.png")),
            "move_up_6": pg.image.load(os.path.join(player_image_path, "player_move_up_6.png")),
        }  # спрайты ходьбы вверх
        self.images_move_down = {
            "move_down_1": pg.image.load(os.path.join(player_image_path, "player_move_down_1.png")),
            "move_down_2": pg.image.load(os.path.join(player_image_path, "player_move_down_2.png")),
            "move_down_3": pg.image.load(os.path.join(player_image_path, "player_move_down_3.png")),
            "move_down_4": pg.image.load(os.path.join(player_image_path, "player_move_down_4.png")),
            "move_down_5": pg.image.load(os.path.join(player_image_path, "player_move_down_5.png")),
            "move_down_6": pg.image.load(os.path.join(player_image_path, "player_move_down_6.png")),
        }  # спрайты ходьбы вниз
        self.images_stay_down = {
            "stay_down_1": pg.image.load(os.path.join(player_image_path, "player_idle_1.png")),
            "stay_down_2": pg.image.load(os.path.join(player_image_path, "player_idle_2.png")),
            "stay_down_3": pg.image.load(os.path.join(player_image_path, "player_idle_3.png")),
            "stay_down_4": pg.image.load(os.path.join(player_image_path, "player_idle_4.png")),
        }  # спрайты idle вниз
        self.images_stay_up = {
            "stay_up_1": pg.image.load(os.path.join(player_image_path, "player_up_look_1.png")),
            "stay_up_2": pg.image.load(os.path.join(player_image_path, "player_up_look_2.png")),
            "stay_up_3": pg.image.load(os.path.join(player_image_path, "player_up_look_3.png")),
            "stay_up_4": pg.image.load(os.path.join(player_image_path, "player_up_look_4.png")),
        }  # спрайты idle вверх
        self.images_stay_left = {
            "stay_left_1": pg.image.load(os.path.join(player_image_path, "player_left_look_1.png")),
            "stay_left_2": pg.image.load(os.path.join(player_image_path, "player_left_look_2.png")),
            "stay_left_3": pg.image.load(os.path.join(player_image_path, "player_left_look_3.png")),
            "stay_left_4": pg.image.load(os.path.join(player_image_path, "player_left_look_4.png")),
        }  # спрайты idle влево
        self.images_stay_right = {
            "stay_right_1": pg.image.load(os.path.join(player_image_path, "player_right_look_1.png")),
            "stay_right_2": pg.image.load(os.path.join(player_image_path, "player_right_look_2.png")),
            "stay_right_3": pg.image.load(os.path.join(player_image_path, "player_right_look_3.png")),
            "stay_right_4": pg.image.load(os.path.join(player_image_path, "player_right_look_4.png")),
        }  # спрайты idle вправо
        self.images_death = {
            "player_death_1": pg.image.load(os.path.join(player_image_path, "player_death_1.png")),
            "player_death_2": pg.image.load(os.path.join(player_image_path, "player_death_2.png")),
            "player_death_3": pg.image.load(os.path.join(player_image_path, "player_death_3.png")),
            "player_death_4": pg.image.load(os.path.join(player_image_path, "player_death_4.png")),
        }  # спрайты death
        # Массивы всех спрайтов idle
        self.animation_frames_stay_down = ["stay_down_1", "stay_down_2", "stay_down_3", "stay_down_4"]
        self.animation_frames_stay_up = ["stay_up_1", "stay_up_2", "stay_up_3", "stay_up_4"]
        self.animation_frames_stay_left = ["stay_left_1", "stay_left_2", "stay_left_3", "stay_left_4"]
        self.animation_frames_stay_right = ["stay_right_1", "stay_right_2", "stay_right_3", "stay_right_4"]
        # Массивы всех спрайтов move
        self.animation_frames_move_right = ["move_right_1", "move_right_2", "move_right_3", "move_right_4",
                                            "move_right_5", "move_right_6"]
        self.animation_frames_move_left = ["move_left_1", "move_left_2", "move_left_3", "move_left_4",
                                           "move_left_5", "move_left_6"]
        self.animation_frames_move_up = ["move_up_1", "move_up_2", "move_up_3", "move_up_4",
                                         "move_up_5", "move_up_6"]
        self.animation_frames_move_down = ["move_down_1", "move_down_2", "move_down_3", "move_down_4",
                                           "move_down_5", "move_down_6"]
        self.animation_frames_bow = ["bow_1", "bow_2", "bow_3", "bow_4"]


class Textures_enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        material_image_path = os.path.join(os.getcwd(), "assets", "material")
        self.fly_entity = {
            "fly_1": pg.image.load(os.path.join(material_image_path, "entity", "fly_1.png")),
            "fly_2": pg.image.load(os.path.join(material_image_path, "entity", "fly_2.png")),
            "fly_3": pg.image.load(os.path.join(material_image_path, "entity", "fly_3.png")),
            "fly_4": pg.image.load(os.path.join(material_image_path, "entity", "fly_4.png")),
            "spawn_1": pg.image.load(os.path.join(material_image_path, "entity", "spawn_fly_1.png")),
            "spawn_2": pg.image.load(os.path.join(material_image_path, "entity", "spawn_fly_2.png")),
            "spawn_3": pg.image.load(os.path.join(material_image_path, "entity", "spawn_fly_3.png")),
            "spawn_4": pg.image.load(os.path.join(material_image_path, "entity", "spawn_fly_4.png")),
            "spawn_5": pg.image.load(os.path.join(material_image_path, "entity", "spawn_fly_5.png")),
            "fly_dead_1": pg.image.load(os.path.join(material_image_path, "entity", "fly_dead_1.png")),
            "fly_dead_2": pg.image.load(os.path.join(material_image_path, "entity", "fly_dead_2.png")),
            "fly_dead_3": pg.image.load(os.path.join(material_image_path, "entity", "fly_dead_3.png")),
            "fly_dead_4": pg.image.load(os.path.join(material_image_path, "entity", "fly_dead_4.png")),
            "bullet": pg.image.load(os.path.join(material_image_path, "entity", "enemy_bullet.png")),
            "hit_by_enemy": pg.image.load(os.path.join(material_image_path, "entity", "hit_by_enemy.png")),
        }


class Textures_weapon(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image_path = os.path.join(os.getcwd(), "assets", "material",
                                         "player_sprite")
        self.images_bow = {
            "bow_1": pg.image.load(os.path.join(player_image_path, "bow_1.png")),
            "bow_2": pg.image.load(os.path.join(player_image_path, "bow_2.png")),
            "bow_3": pg.image.load(os.path.join(player_image_path, "bow_3.png")),
            "bow_4": pg.image.load(os.path.join(player_image_path, "bow_4.png")),
            "bow_death_1": pg.image.load(os.path.join(player_image_path, "bow_death_1.png")),
            "bow_death_2": pg.image.load(os.path.join(player_image_path, "bow_death_2.png")),
            "bow_death_3": pg.image.load(os.path.join(player_image_path, "bow_death_3.png")),
            "bow_death_4": pg.image.load(os.path.join(player_image_path, "bow_death_4.png")),
            "bow_death_5": pg.image.load(os.path.join(player_image_path, "bow_death_5.png")),
            "bow_shoot": pg.image.load(os.path.join(player_image_path, "bow_shoot.png")),
            "bow_idle": pg.image.load(os.path.join(player_image_path, "bow_idle.png")),

        }


class Textures_tile(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tiles_image_path = os.path.join(os.getcwd(), "assets", "tiles")
        self.tileData = [
            ['0', 'c1', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'c4'],
            ['c1', 'l1', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'r1', 'c4'],
            ['lg', 'U', 's3', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 's4', 'U',
             'rg'],
            ['lg', 's3', 's1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 's5', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['lg', 's2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'rg'],
            ['c2', 'l2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'r2', 'c3'],
            ['0', 'c2', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'c3'],
            ['0', '0', '0', '0', '0', '0', '0', '0', 't', 't', 't'],
        ]
        self.texture_room = {
            "floor_1": pg.image.load(os.path.join(tiles_image_path, "floor_1.bmp")),
            "floor_2": pg.image.load(os.path.join(tiles_image_path, "floor_2.bmp")),
            "floor_3": pg.image.load(os.path.join(tiles_image_path, "floor_3.bmp")),
            "floor_4": pg.image.load(os.path.join(tiles_image_path, "floor_4.bmp")),
            "floor_5": pg.image.load(os.path.join(tiles_image_path, "floor_5.bmp")),
            "floor_side_1": pg.image.load(os.path.join(tiles_image_path, "floor_side_1.bmp")),
            "floor_side_2": pg.image.load(os.path.join(tiles_image_path, "floor_side_2.bmp")),
            "floor_side_3": pg.image.load(os.path.join(tiles_image_path, "floor_side_3.bmp")),
            "floor_side_up": pg.image.load(os.path.join(tiles_image_path, "floor_side_up.bmp")),
            "floor_side_continue": pg.image.load(os.path.join(tiles_image_path, "floor_side_continue.bmp")),
            "border_1": pg.image.load(os.path.join(tiles_image_path, "border_1.bmp")),
            "border_2": pg.image.load(os.path.join(tiles_image_path, "border_2.bmp")),
            "border_3": pg.image.load(os.path.join(tiles_image_path, "border_3.bmp")),
            "border_4": pg.image.load(os.path.join(tiles_image_path, "border_4.bmp")),
            "border_5": pg.image.load(os.path.join(tiles_image_path, "border_5.bmp")),
            "border_up_1": pg.image.load(os.path.join(tiles_image_path, "border_up_1.bmp")),
            "border_up_2": pg.image.load(os.path.join(tiles_image_path, "border_up_2.bmp")),
            "border_up_3": pg.image.load(os.path.join(tiles_image_path, "border_up_3.bmp")),
            "border_up_4": pg.image.load(os.path.join(tiles_image_path, "border_up_4.bmp")),
            "border_up_5": pg.image.load(os.path.join(tiles_image_path, "border_up_5.bmp")),
            "border_corner": pg.image.load(os.path.join(tiles_image_path, "border_corner.bmp")),
            "wall": pg.image.load(os.path.join(tiles_image_path, "wall.bmp")),
            "angle_1": pg.image.load(os.path.join(tiles_image_path, "angle_1.bmp")),
            "angle_2": pg.image.load(os.path.join(tiles_image_path, "angle_2.bmp")),
            "side_lock_down": pg.image.load(os.path.join(tiles_image_path, "side_lock_down.png")),
            "side_lock_up": pg.image.load(os.path.join(tiles_image_path, "side_lock_up.png")),
            "side_lock_left": pg.image.load(os.path.join(tiles_image_path, "side_lock_left.png")),
            "side_lock_right": pg.image.load(os.path.join(tiles_image_path, "side_lock_right.png")),
        }


class Textures_Hud_Sound(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sound_directory = os.path.join(os.getcwd(), "sounds")  # Основная карта локации
        material_image_path = os.path.join(os.getcwd(), "assets", "material")
        self.hud = {
            "hp_bar_1": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_1.png")),
            "hp_bar_2": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_2.png")),
            "hp_bar_3": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_3.png")),
            "hp_bar_4": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_4.png")),
            "hp_bar_5": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_5.png")),
            "hp_bar_6": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_6.png")),
            "hp_bar_7": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_7.png")),
            "hp_bar_8": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_8.png")),
            "hp_bar_9": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_9.png")),
            "hp_bar_10": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_10.png")),
            "hp_bar_11": pg.image.load(os.path.join(material_image_path, "Hud", "hp_bar_11.png")),
            "crosshair_1": pg.image.load(os.path.join(material_image_path, "Hud", "crosshair_1.png")),
            "security": pg.image.load(os.path.join(material_image_path, "Hud", "security.png")),
            "start": pg.image.load(os.path.join(material_image_path, "Hud", "start.png")),
            "continue": pg.image.load(os.path.join(material_image_path, "Hud", "continue.png")),
            "exit": pg.image.load(os.path.join(material_image_path, "Hud", "exit.png")),
            "Fullscreen": pg.image.load(os.path.join(material_image_path, "Hud", "Fullscreen.png")),
            "Windowed": pg.image.load(os.path.join(material_image_path, "Hud", "Windowed.png")),
            "cursor": pg.image.load(os.path.join(material_image_path, "Hud", "crosshair_1.png")),

        }
        self.sound = {
            "arrow_wall": pg.mixer.Sound(os.path.join(sound_directory, "arrow_wall.wav")),
            "enemy_shoot_player": pg.mixer.Sound(os.path.join(sound_directory, "enemy_shoot_player.wav")),
            "pulling_arrow": pg.mixer.Sound(os.path.join(sound_directory, "pulling_arrow.wav")),
            "shoot_arrow": pg.mixer.Sound(os.path.join(sound_directory, "shoot_arrow.wav")),
            "shoot_blaster": pg.mixer.Sound(os.path.join(sound_directory, "shoot_blaster.wav")),
            "shoot_enemy": pg.mixer.Sound(os.path.join(sound_directory, "shoot_enemy.wav")),
            "swing_sword": pg.mixer.Sound(os.path.join(sound_directory, "swing_sword.wav")),
            "swing_sword_1": pg.mixer.Sound(os.path.join(sound_directory, "swing_sword_1.wav")),
            "vzhooh": pg.mixer.Sound(os.path.join(sound_directory, "vzhooh.wav")),
            "steps": pg.mixer.Sound(os.path.join(sound_directory, "step_sound.wav")),
            "destruction_wall": pg.mixer.Sound(os.path.join(sound_directory, "destruction_wall.wav")),
            "heal": pg.mixer.Sound(os.path.join(sound_directory, "heal_sound.wav")),
            "button": pg.mixer.Sound(os.path.join(sound_directory, "button.wav")),
            "draw_sword": pg.mixer.Sound(os.path.join(sound_directory, "draw_sword.wav")),
        }
