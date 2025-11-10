# Github: https://github.com/EliasDweiri/dweiri_mob_hunters


# SOURCES:

# Mr. Cozort - created base code - created spin move attack
# ChatGPT - generated Background_Flower_Field_1024x1024, cocreated mob v mob collision with Elias Dweiri
# Sprites - Created in https://www.piskelapp.com/p/create/sprite/ by Elias Dweiri
# Pathfinding - Found in https://medium.com/@aggorjefferson/building-an-a-pathfinding-visualizer-in-python-with-pygame-a2cb3502f49e

# Game Music: 
# 
# found in https://opengameart.org/ 
# - Sci-fi Puzzle In-Game 3 / Back_Ground_Theme_1

# GOALS:

# Mobs have collision between each other - COMPLETED
# A sort of wave system where mobs come in waves after they are killed
# Different weapons
# Complete Sprite retexture
# Background change
# Staring screen  ui to choose starting weapons and traits
# Different levels/difficulties aftrer defeating mobs
# updated screen health and coin amount counters
# mobs have collission against weapons
# Screen Text that tells what weapon you are currently using when clicked
# walking animation
# better mob pathing 



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
from queue import PriorityQueue




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
        self.img_folder = path.join(self.game_folder, 'images') # images folder
        self.sound_folder = path.join(self.game_folder, 'sounds') # sound folder
        self.map = Map(path.join(self.game_folder, "level1.txt")) # ttext map folder


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
        pg.mixer.music.set_volume(0.5)
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
        self.all_weapons = pg.sprite.Group()

        # takes the map data and creates the appropriate object for each tile, map maker
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
         #  print("this is happening")
          self.playing = False
        if event.type == pg.MOUSEBUTTONDOWN:
           print("I can get input from mousey mouse mouse mousekerson")
        if event.type == pg.KEYDOWN:
           if event.key == pg.K_k:
              self.player.attacking = True
              self.player.weapon = Sword(self, self.player.rect.x, self.player.rect.y)
        if event.type == pg.KEYUP:
           if event.key == pg.K_k:
              self.player.attacking = False
              self.player.weapon.kill()

    def update(self):

        # creates a countdown timer
        self.all_sprites.update()
        seconds = pg.time.get_ticks() // 1000
        countdown = 10
        self.time = countdown - seconds
        # once there are no coins left, spawns more coins
        if len(self.all_coins) == 0:
            for i in range(2, 7):
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
