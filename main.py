# SOURCES:
# Mr. Cozort - created base code
# ChatGPT - created Background_Flower_Field_1024x1024

# yay I can use github from VS CODE!

import math
import random
import sys
from typing import List, Tuple, Optional
import pygame as pg
from settings import *
from sprites import *
from utils import *
from os import path
from random import randint 




class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Mob Hunters")
        self.playing = True

    # sets up a game folder directory path using the current folder containing this file
    # gives the Game class a map property which uses the Map class to parse the level1.txt file
    # loads image files from images folder
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.sound_folder = path.join(self.game_folder, 'sounds')
        self.map = Map(path.join(self.game_folder, "level1.txt"))


        # loads images into memory when a new game is created and load_data
        self.player_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.mob_img = pg.image.load(path.join(self.img_folder, "Coal_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.coin_img = pg.image.load(path.join(self.img_folder, "Emerald_Coin_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.wall_img = pg.image.load(path.join(self.img_folder, "Cobblestone_Wall_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.projectile_img = pg.image.load(path.join(self.img_folder, "Water_Projectile_16x16.png")).convert_alpha()  # PUT FILE HERE
        self.background_img = pg.image.load(path.join(self.img_folder, "Background_Flower_Field_1024x768.png")).convert_alpha()  # PUT FILE HERE
        self.player_running_left = pg.image.load(path.join(self.img_folder, "Diamond_Man_Running_Left_32x32.png")).convert()
        # self.spin_move1_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move2_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r1.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move3_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r2.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move4_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r3.png")).convert_alpha()  # PUT FILE HERE


        # MUSIC THEMES

        pg.mixer.music.load(path.join(self.sound_folder, "Back_Ground_Theme_1.mp3"))
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(-1)


    def new(self):
        # the sprite Group allows us to update and draw sprite in grouped batches
        self.load_data()
        # create all sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group() 

        # takes the map data and creates the appropriate object for each tile
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row, "unmoveable")
                elif tile == "2":
                    Wall(self, col, row, "moveable")
                elif tile == "C":
                    Coin(self, col, row)
                elif tile == "P":
                    self.player = Player(self, col, row)
                elif tile == "M":
                    Mob(self, col, row)

    def run(self):
        # game loop
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()
        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("this is happening")
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print("I can get input from mousey mouse mouse mouskerson")

    def update(self):
        # creates a countdown timer
        self.all_sprites.update()
        seconds = pg.time.get_ticks() // 1000
        countdown = 10
        self.time = countdown - seconds
        # once there are no coins left, spawns more coins
        if len(self.all_coins) == 0:
            for i in range(2, 5):
                Coin(self, randint(1, 20), randint(1, 20))  
            print("I'm BROKE!")

    def draw_text(self, surface, text, size, color, x, y):
        # draws text on screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        # calls on draw_text
        # self.screen.fill(WHITE) # white Background if needed
        self.screen.blit(self.background_img, (0, 0)) # IMG background
        self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
        self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 100)
        self.draw_text(self.screen, str(self.time), 24, BLACK, 500, 100) 
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == "__main__":
    # creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()
