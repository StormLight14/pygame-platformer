from tracemalloc import is_tracing
import pygame
from game.player import Player
from game.tile import Tile
from game.enemy import Enemy
import os
import pytmx

class Level:
    def __init__(self, screen):

        self.get_level_data()
        self.level = self

        # get the display surface
        self.display_surface = pygame.display.get_surface() 

        self.visible_sprites = pygame.sprite.Group()
        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        # gravity
        self.gravity = 1

        # tile and map
        self.tmx_data = pytmx.load_pygame(f"./game/levels/{self.current_level}.tmx")

        self.screen = screen

        # setup for level transition
        self.current_time = 0
        self.transition_time = 0
        self.transitions_enabled = False

        self.is_transitioning = False

        with open("./game/leveldata/game_data.txt", 'r') as level_file:
            self.transition_data = level_file.read()
            self.transition_data = self.transition_data.split(", ")
            if self.transition_data[3] == 'True':
                self.transitions_enabled = True

        # level positions
        self.player_positions_right = [
            "128, 128",
            "128, 128",
            "128, 0",
            "128, 128",
            "128, 128",
        ]

        self.player_positions_left = [
            "1800, 128",
            "1800, 128",
            "1800, 0",
            "1800, 128",
            "1800, 128"
        ]

        self.level_index = int(self.game_data[0].replace("level", ""))

        self.create_map()

    def create_map(self):
        self.visible_sprites.empty()
        self.tile_sprites.empty()
        self.tmx_data = pytmx.load_pygame(f"./game/levels/{self.current_level}.tmx")
        self.player = Player((self.player_x, self.player_y), self.gravity, [self.visible_sprites], self.tile_sprites, self.enemy_sprites, self.visible_sprites, self.bullet_sprites, self.level, self.screen)

        for row in self.tmx_data:
            if row.name == "platforms":
                for col in row:
                    if col[2] != 0: 
                        # add tile to sprite group and get the correct image for it
                        image = self.tmx_data.get_tile_image(col[0], col[1], 0)

                        Tile((col[0] * 64, col[1] * 64), image, [self.visible_sprites, self.tile_sprites])
            if row.name == "enemies":
                for col in row:
                    if col[2] != 0: 
                        Enemy((col[0] * 64, col[1] * 64), col[2], self.player, [self.visible_sprites, self.enemy_sprites])
            if row.name == "border":
                for col in row:
                    if col[2] != 0:
                        image = pygame.image.load("./game/assets/tile.png").convert()
                        Tile((col[0] * 64, col[1] * 64), image, [self.tile_sprites])


    def get_level_data(self):
        # set default level data
        if os.path.exists('./game/leveldata/game_data.txt') == False:
            with open("./game/leveldata/game_data.txt", 'a') as level_file:
                level_file.write(f'level0, {self.player_positions_left[0]} False, 3')
                self.level_index = 0

        # get data from level data file
        with open("./game/leveldata/game_data.txt", 'r') as level_file:
            self.game_data = level_file.read()
            self.game_data = self.game_data.split(", ")

            self.current_level = self.game_data[0]
            self.level_index = int(self.game_data[0].replace("level", ""))
            self.player_x = int(self.game_data[1])
            self.player_y = int(self.game_data[2])
            if self.game_data[3] == 'True':
                self.transitions_enabled = True
            

    def switch_level(self, dir):
        if dir == "right":
            # increment level index by 1
            self.level_index += 1
            self.check_level(dir)

            # get time since started transition
            if self.transitions_enabled == True:
                self.transition_time = pygame.time.get_ticks()

                self.is_transitioning = True
                self.screen.fill("#000000")
            else:
                self.create_map()


        if dir == "left":
            # increment level index by 1
            self.level_index -= 1
            self.check_level(dir)


            # get time since started transition
            if self.transitions_enabled == True:
                self.transition_time = pygame.time.get_ticks()

                self.is_transitioning = True
                self.screen.fill("#000000")
            else:
                self.create_map()


    def check_level(self, dir):

        # level index choosing level
        if self.level_index == 0:
            self.current_level = 'level0'
            if dir == "left":
                self.write_level(dir)
            elif dir == "right":
               self.write_level(dir)
            
            self.get_level_data()
                    
        elif self.level_index == 1:
            self.current_level = 'level1'
            if dir == "left":
                self.write_level(dir)
            elif dir == "right":
                self.write_level(dir)

            self.get_level_data()

        elif self.level_index == 2:
            self.current_level = 'level2'
            if dir == "left":
                self.write_level(dir)
            elif dir == "right":
                self.write_level(dir)

            self.get_level_data()

        elif self.level_index == 3:
            self.current_level = 'level3'
            if dir == "left":
                self.write_level(dir)
            elif dir == "right":
                self.write_level(dir)

            self.get_level_data()

        elif self.level_index == 4:
            self.current_level = 'level4'
            if dir == "left":
                self.write_level(dir)
            elif dir == "right":
                self.write_level(dir)

            self.get_level_data()

    def write_level(self, dir):
        with open("./game/leveldata/game_data.txt", 'w') as level_file:
            if dir == 'left':
                level_file.write(f"{self.current_level}, {self.player_positions_left[self.level_index]}, {self.transitions_enabled}, {self.player.lives}")
            if dir == 'right':
                level_file.write(f"{self.current_level}, {self.player_positions_right[self.level_index]}, {self.transitions_enabled}, {self.player.lives}")
        self.get_level_data()
        print(self.transitions_enabled)

    def check_level_switch(self):
        # move levels when moving
        if self.player.rect.left > 1920:
            self.switch_level("right")
        
        elif self.player.rect.right < 0:
            self.switch_level("left")


    def timer(self):
        self.current_time = pygame.time.get_ticks()
        

    def transition(self):
        if self.is_transitioning == True:
            if self.current_time - self.transition_time > 2000:
                self.create_map()
                self.is_transitioning = False
            

    def background(self):
        self.screen.fill("#44d1db")


    def save_game(self):
        with open("./game/leveldata/game_data.txt", 'w') as level_file:
            level_file.write(f"{self.current_level}, {self.player.rect.x}, {self.player.rect.y}, {self.transitions_enabled}, {self.player.lives}")

    def reset_game(self):
        self.current_level = 'level0'
        self.level_index = 0
        self.player.lives = 3

        with open("./game/leveldata/game_data.txt", 'w') as level_file:
            level_file.write(f"{self.current_level}, {self.player_positions_right[0]}, {self.transitions_enabled}, {self.player.lives}")
        self.enemy_sprites.empty()
        self.tile_sprites.empty()
        self.visible_sprites.empty()

        self.get_level_data()
        self.create_map()

    def run(self):
        # only run if not in transition phase
        if self.is_transitioning == False:
            self.background()
            self.visible_sprites.draw(self.display_surface)
            self.visible_sprites.update()
            self.check_level_switch()

        # always run timer
        self.timer()
        if self.transitions_enabled == True:
            self.transition()
