# Github: https://github.com/EliasDweiri/dweiri_mob_hunters


# SOURCES:

# Mr. Cozort - created base code, created spin attack
# ChatGPT - bug fixes, and animated score, assisted with boss attacks, 
# Sprites - Created in https://www.piskelapp.com/p/create/sprite/ by Elias Dweiri

# Game Music: 
# 
# found in https://opengameart.org/ 
# - Sci-fi Puzzle In-Game 3 / Back_Ground_Theme_1

# GOALS:

# be able to kill mobs- COMPLETED
# Mobs have collision between each other - COMPLETED
# A sort of wave system where mobs come in waves after they are killed - COMPLETED
# Different weapons - COMPLETED
# Background revamp - COMPLETED
# Different levels/difficulties after defeating mobs - COMPLETED
# updated screen health and coin amount counters - COMPLETED
# mobs have collission against weapons - COMPLETED
# walking animation - COMPLETED
# update text - COMPLETED
# Pause Mechanism - COMPLETED
# Unlock Weapons when mobs are killed - COMPLETED
# Health bar - COMPLETED
# mob kill counter: lvl 1 mob with 1 kill, lvl 5 mob worth 5 kills etc. basically a total score - COMPLETED
# water shot, sword, staff, axe - COMPLETED
# add a title screen/start screen and end screen - COMPLETED
# give a sprite to the power 2 mob
# power 3 mob - COMPLETED
# score calculated on death screen - COMPLETED
# better way of doing potions - COMPLETED
# speed potion goes away after 12 seconds - COMPLETED
# mobs are killed when they are kicked out of the map - COMPLETED
# fix game loop when player dies - COMPLETED
# win screen - COMPLETED

# KEYS:

# w - up
# a - left
# s - down
# d - right
# k - sword
# o - axe
# p - water shot
# i - staff
# tab - pause

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
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("MOB HUNTERS")
        self.playing = True
        self.running = True
        self.total_kills = 0
        self.mob_kills = 0
        self.font = pg.font.Font(None, 50)
        self.total_score = 0
        self.displayed_score = 0
        self.score_speed = 1
        self.wave = 1
        self.sword_unlocked = False
        self.staff_unlocked = False
        self.axe_unlocked = False
        self.water_unlocked = True      # starting weapon
        self.unlock_message = None
        self.unlock_message_time = 0
        self.game_over_time = None
        self.score_pause_done = False

       

    # sets up a game folder directory path using the current folder containing this file
    # gives the Game class a map property which uses the Map class to parse the level1.txt file
    # loads image files from images folder
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images') # images folder
        self.sound_folder = path.join(self.game_folder, 'sounds') # sound folder
        self.map = Map(path.join(self.game_folder, "level1.txt")) # text map folder


        # loads images into memory when a new game is created and load_data
        self.player_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.mob_img = pg.image.load(path.join(self.img_folder, "Coal_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.coin_img = pg.image.load(path.join(self.img_folder, "Emerald_Coin_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.wall_img = pg.image.load(path.join(self.img_folder, "Cobblestone_Wall_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.projectile_img = pg.image.load(path.join(self.img_folder, "Water_Projectile_16x16.png")).convert_alpha()  # PUT FILE HERE
        self.background_img = pg.image.load(path.join(self.img_folder, "Ground.png")).convert_alpha()
        self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
        self.player_running_left = pg.image.load(path.join(self.img_folder, "Diamond_Man_Running_Left_32x32.png")).convert_alpha() # PUTFILE HERE
        self.player_running_right = pg.image.load(path.join(self.img_folder, "Diamond_Man_Running_Right_32x32.png")).convert_alpha() # PUTFILE HERE
        self.sword_left_img = pg.image.load(path.join(self.img_folder, "sword_left.png")).convert_alpha()
        self.sword_right_img = pg.image.load(path.join(self.img_folder, "sword_right.png")).convert_alpha()
        self.sword_up_img = pg.image.load(path.join(self.img_folder, "sword_up.png")).convert_alpha()
        self.sword_down_img = pg.image.load(path.join(self.img_folder, "sword_down.png")).convert_alpha()
        self.axe_img = pg.image.load(path.join(self.img_folder, "Axe_5x50.png")).convert_alpha()
        self.staff_img = pg.image.load(path.join(self.img_folder, "Staff_60x15.png")).convert_alpha()
        self.health_potion_img = pg.image.load(path.join(self.img_folder, "Health_Potion_32x32.png")).convert_alpha()
        self.speed_potion_img = pg.image.load(path.join(self.img_folder, "Speed_Potion_32x32.png")).convert_alpha()
        self.damage_potion_img = pg.image.load(path.join(self.img_folder, "Damage_Potion.png")).convert_alpha()
        self.knockback_potion_img = pg.image.load(path.join(self.img_folder, "Knockback_Potion_33x33.png")).convert_alpha()
        self.defense_potion_img = pg.image.load(path.join(self.img_folder, "Defense_Potion_33x33.png")).convert_alpha()
        self.mob_boss1_img = pg.image.load(path.join(self.img_folder, "Coal_Man_Boss_64x64.png")).convert_alpha()  # PUT FILE HERE
        self.mobp2_img = pg.image.load(path.join(self.img_folder, "Power2Mob_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.mob_boss2_img = pg.image.load(path.join(self.img_folder, "Power2BossMob_64x64.png")).convert_alpha()  # PUT FILE HERE
        self.mobp3_img = pg.image.load(path.join(self.img_folder, "Power3Mob_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.mob_boss3_img = pg.image.load(path.join(self.img_folder, "Power3BossMob_64x64.png")).convert_alpha()  # PUT FILE HERE
        self.mobp4_img = pg.image.load(path.join(self.img_folder, "Power4Mob_32x32.png")).convert_alpha()  # PUT FILE HERE
        self.mob_boss4_img = pg.image.load(path.join(self.img_folder, "Power4BossMob_64x64.png")).convert_alpha()  # PUT FILE HERE


        # self.spin_move1_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move2_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r1.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move3_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r2.png")).convert_alpha()  # PUT FILE HERE
        # self.spin_move4_img = pg.image.load(path.join(self.img_folder, "Diamond_Man_32x32_r3.png")).convert_alpha()  # PUT FILE HERE


        # MUSIC THEMES

        pg.mixer.music.load(path.join(self.sound_folder, "Back_Ground_Theme_1.mp3"))
        pg.mixer.music.set_volume(MUSIC_VOLUME)
        pg.mixer.music.play(-1)


    def new(self):

        self.wave = 1
        self.sword_unlocked = False
        self.staff_unlocked = False
        self.axe_unlocked = False
        self.water_unlocked = True
        self.total_score = 0
        self.displayed_score = 0
        self.game_over_time = None
        self.paused = False
        self.playing = True
        self.total_kills = 0
        self.mob_kills = 0
        self.start_time = pg.time.get_ticks()
        # the sprite Group allows us to update and draw sprite in grouped batches
        self.load_data()
        # create all sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_weapons = pg.sprite.Group()
        self.all_breakable_walls = pg.sprite.Group()
        self.all_potions = pg.sprite.Group()
        self.potions = pg.sprite.Group()
        self.damage_numbers = pg.sprite.Group()
        self.boss_attacks = pg.sprite.Group()

        # takes the map data and creates the appropriate object for each tile, map maker
        for row, tiles in enumerate(self.map.data):
            # print(row)
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row, "unmoveable")
                elif tile == "2":
                    Wall(self, col, row, "moveable")
                elif tile == "3":
                    Indestructible_Wall(self, col, row, "unmoveable")
                elif tile == "4":
                    Indestructible_Wall(self, col, row, "moveable")
                elif tile == "C":
                    Coin(self, col, row)
                elif tile == "P":
                    self.player = Player(self, col, row)
                    self.player.health = 100 # this is here to reset for a new round
                # elif tile == "M":
                #     Mob(self, col, row) # old mob spawning
                

        # for i in range(5):
        #     MOb(self, randint(1, 2))
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

    def events(self):
      for event in pg.event.get():
        if event.type == pg.QUIT:
         #  print("this is happening")
          self.playing = False
          self.running = False

        if event.type == pg.KEYDOWN:

            # ESC quits game completely
            if event.key == pg.K_ESCAPE:
                self.playing = False
                self.running = False

            # TAB toggles pause
            if event.key == pg.K_TAB:
                self.paused = not getattr(self, "paused", False)

            # prevent controls from working while paused
            if getattr(self, "paused", False):
                return
            
        # if event.type == pg.MOUSEBUTTONDOWN:
        #    print("I can get input from mousey mouse mouse mousekerson")
        # sword 
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_k and self.sword_unlocked: # makes it locked until certain
                self.player.attacking = True
                self.player.weapon = Sword(self, self.player.rect.x, self.player.rect.y)

        if event.type == pg.KEYUP:
            if event.key == pg.K_k and self.player.weapon:
                self.player.attacking = False
                self.player.weapon.kill()

                
        
        # if event.type == pg.KEYUP:
        #     if event.key == pg.K_TAB:
        #         self.play_game == False


    def update(self):

        # How many seconds the player survived
        self.time_survived = (pg.time.get_ticks() - self.start_time) // 1000
        # end game if health is 0 or under

        if self.player.health <= 0:
            self.show_game_over_screen()  # show death screen immediately
            self.playing = False
            return

        if getattr(self, "paused", False):
            return
        

        # creates a countdown timer
        self.all_sprites.update()
        seconds = pg.time.get_ticks() // 1000
        countdown = 10
        self.time = countdown - seconds
        # once there are no coins left, spawns more coins
        #coin spawning
        if len(self.all_coins) == 0:
            for i in range(2, 7):
                Coin(self, randint(1, 20), randint(1, 20))  
            # print("I'm BROKE!")

        if not hasattr(self, 'displayed_score'):
            self.displayed_score = 0
        if self.displayed_score < self.total_score:
            # Gradually increment score
            self.displayed_score += max(1, self.total_score // 120)
            if self.displayed_score > self.total_score:
                self.displayed_score = self.total_score

        # potion spawning

        health_count = 0
        for potion in self.all_potions:
            if isinstance(potion, Health_Potion):
                health_count += 1

        #  Always guarantee exactly ONE health potion
        if health_count == 0:
            Health_Potion(self, randint(1, 20), randint(1, 20))

        # Speed & Knockback = rare but always possible
        if random.random() < 0.005:   # chance of spawn
            Speed_Potion(self, randint(1, 20), randint(1, 20))

        if random.random() < 0.005:   
            Knockback_Potion(self, randint(1, 20), randint(1, 20))

        # Damage & Defense 
        if self.mob_kills >= 47: # when wave 3 is reached
            if random.random() < 0.005:   
                Damage_Potion(self, randint(1, 20), randint(1, 20))

            if random.random() < 0.005:
                Defense_Potion(self, randint(1, 20), randint(1, 20))
        

        # mobs spawning in waves
        if self.all_mobs_dead(): # only spawn when last wave is dead
            self.clear_potions()
            self.spawn_wave()
 
   
    def all_mobs_dead(self):
        # Return True if NO mobs are alive and visible in the game area 
        for mob in self.all_mobs:
            if mob.alive():
                # Check if mob is within the visible screen
                if 0 <= mob.rect.centerx <= WIDTH and 0 <= mob.rect.centery <= HEIGHT:
                    return False    # There is at least ONE valid mob alive
        return True  # No live mobs found on-screen


    def clear_potions(self):
        for p in list(self.all_potions):
            p.kill()


    def spawn_mobs(self, num, power):
        for i in range(num):
            Mob(self, randint(1,20), randint(1,20), power)

    def spawn_wave(self):
        # Show pre-wave countdown
        self.show_wave_countdown(self.wave)
        

        # Then spawn the actual mobs
        if self.wave == 1:
            self.spawn_mobs(1, 1) # self.spawn_mobs(  amount of mobs spawned , strength of the mobs  )

        elif self.wave == 2:
            self.spawn_mobs(3, 1)

        elif self.wave == 3:
            self.spawn_mobs(8, 1)

        elif self.wave == 4:
            self.spawn_mobs(15, 1)

        elif self.wave == 5:
            self.spawn_mobs(1, 101) # boss mob, three digits for boss, but still considered power 1

        elif self.wave == 6:
            self.sword_unlocked = True
            self.unlock_message = "SWORD UNLOCKED!"
            self.unlock_message_time = pg.time.get_ticks()

            self.spawn_mobs(1, 2)
        elif self.wave == 7:

            self.spawn_mobs(3, 2)
        elif self.wave == 8:

            self.spawn_mobs(8, 2)
        elif self.wave == 9:

            self.spawn_mobs(15, 2)
        elif self.wave == 10:

            self.spawn_mobs(1, 102) 
        elif self.wave == 11:
            self.staff_unlocked = True
            self.unlock_message = "STAFF UNLOCKED!"
            self.unlock_message_time = pg.time.get_ticks()
            self.spawn_mobs(1, 3)

        elif self.wave == 12:
            self.spawn_mobs(3, 3)

        elif self.wave == 13:
            self.spawn_mobs(8, 3)

        elif self.wave == 14:
            self.spawn_mobs(15, 3) 

        elif self.wave == 15:
            self.spawn_mobs(1, 103) 

        elif self.wave == 16:
            self.axe_unlocked = True
            self.unlock_message = "AXE UNLOCKED!"
            self.unlock_message_time = pg.time.get_ticks()
            self.spawn_mobs(1, 4)

        elif self.wave == 17:
            self.spawn_mobs(3, 4)

        elif self.wave == 18:
            self.spawn_mobs(8, 4)

        elif self.wave == 19:
            self.spawn_mobs(15, 4)

        elif self.wave == 20:
            self.spawn_mobs(1, 104) 

        elif self.wave == 21:
            self.spawn_mobs(2, 101)
            self.spawn_mobs(2, 102)
            self.spawn_mobs(2, 103)
            self.spawn_mobs(2, 104)
        

        # advance to next wave
        self.wave += 1


    def show_wave_countdown(self, wave_number):
        # Duration for each message in milliseconds
        display_time = 1000  # 1 second per message

        # Messages to display
        messages = [f"WAVE {wave_number}", "3", "2", "1", "GO!"]

        for msg in messages:
            start_time = pg.time.get_ticks()
            while pg.time.get_ticks() - start_time < display_time:
                self.clock.tick(FPS)
                self.screen.fill(BLACK)
                self.draw_text(self.screen, msg, 64, WHITE, WIDTH // 2, HEIGHT // 2 - 64)
                pg.display.flip()


    # old mobs spawning
    # def spawn_mobs(self, num_mobs):
    #     for i in range(num_mobs):
    #         rand = random.random()  # 0.0 to 1.0
    #         if rand < 0.6:          # 60% chance
    #             power = 1
    #         elif rand < 0.9:        # 30% chance
    #             power = 2
    #         else:                   # 10% chance
    #             power = 3

    #         Mob(self, randint(1,20), randint(1,20), power)



    def draw_text(self, surface, text, size, color, x, y):
        # draws text on screen
        font_name = pg.font.match_font('impact')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        font_name = pg.font.match_font('impact') 
        # calls on draw_text
        # self.screen.fill(WHITE) # white Background if needed
        self.screen.blit(self.background_img, (0, 0)) # IMG background
        # self.draw_text(self.screen, f"Health: {self.player.health}", 24, BLACK, 350, 50)
        self.draw_text(self.screen, f"Coins: {self.player.coins}", 24, BLACK, 500, 50)
        # self.draw_text(self.screen, f"Cooldown: {self.time}", 24, BLACK, 650, 50) Cooldown on screen 
        # 1. Draw player with health tint
        tint_color = self.player.get_health_tint()
        tinted_image = self.player.image.copy()
        tinted_image.fill(tint_color, special_flags=pg.BLEND_MULT)
        self.screen.blit(tinted_image, self.player.rect.topleft)


       
        #Draw circular health around player
        # self.player.draw_health_circle(self.screen)

        # Draw damage numbers
        self.damage_numbers.update()
        self.damage_numbers.draw(self.screen)
        # HEALTH BAR
        self.player.draw_health_bar(self.screen)
        # self.draw_text(self.screen, f"Current Weapon: {self.weapon}", 24, BLACK, 800, 50)
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            if hasattr(sprite, "draw"):
                sprite.draw(self.screen)
            else:
                self.screen.blit(sprite.image, sprite.rect)


        # red border only on the edges
        red_overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

        # Fade & thickness scale with health, max, return its biggest item
        health_percent = max(self.player.health / 100, 0)

        red_intensity = int((1 - health_percent) * 180)   # how strong red is
        border_thickness = int((1 - health_percent) * 100)  # how thick border is

        # so it doesnt break
        border_thickness = max(5, border_thickness)

        # Top edge
        pg.draw.rect(red_overlay, (255, 0, 0, red_intensity), (0, 0, WIDTH, border_thickness))
        # Bottom edge
        pg.draw.rect(red_overlay, (255, 0, 0, red_intensity), (0, HEIGHT - border_thickness, WIDTH, border_thickness))
        # Left edge
        pg.draw.rect(red_overlay, (255, 0, 0, red_intensity), (0, 0, border_thickness, HEIGHT))
        # Right edge
        pg.draw.rect(red_overlay, (255, 0, 0, red_intensity), (WIDTH - border_thickness, 0, border_thickness, HEIGHT))

        self.screen.blit(red_overlay, (0, 0))


        # Draw sword unlock message 
        if self.unlock_message:
            if pg.time.get_ticks() - self.unlock_message_time < 2000:
                self.draw_text(
                    self.screen,
                    self.unlock_message,
                    48,
                    (BLACK),  # gold
                    WIDTH // 2,
                    HEIGHT // 2 - 150
                )
            else:
                self.unlock_message = None

        pg.display.flip()

    def wait_for_key(self, delay=0):
        waiting = True
        start_time = pg.time.get_ticks()

        while waiting:
            self.clock.tick(FPS)

            # Only allow input AFTER the delay passes
            allow_input = (pg.time.get_ticks() - start_time) >= delay

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.playing = False
                    waiting = False

                elif allow_input and (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN):
                    waiting = False

            pg.display.flip()


     # title screen stuff
    def show_start_screen(self):
        # game splash/start screen
      #   pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
      #   pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text(self.screen,"Mob Hunters", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen,"Click any button to start.", 24, WHITE, WIDTH / 2, 700)
        self.draw_text(self.screen,"Controls:", 24, WHITE, WIDTH / 4, 350)
        self.draw_text(self.screen,"w     -     up", 24, WHITE, (WIDTH / 4) + 30, 410)
        self.draw_text(self.screen,"a     -     left", 24, WHITE, (WIDTH / 4) + 175, 410)
        self.draw_text(self.screen,"s     -     down", 24, WHITE, (WIDTH / 4) + 320, 410)
        self.draw_text(self.screen,"d     -     right", 24, WHITE, (WIDTH / 4) + 465, 410)
        self.draw_text(self.screen,"p     -     water", 24, WHITE, (WIDTH / 4) + 45, 470)
        self.draw_text(self.screen,"k     -     sword", 24, WHITE, (WIDTH / 4) + 190, 470)
        self.draw_text(self.screen,"i     -     staff", 24, WHITE, (WIDTH / 4) + 335, 470)
        self.draw_text(self.screen,"o     -     axe", 24, WHITE, (WIDTH / 4) + 480, 470)
        self.draw_text(self.screen,"Tab     -     pause", 24, WHITE, (WIDTH / 2) + 100, 530)
        self.draw_text(self.screen,"Esc     -     Quit", 24, WHITE, (WIDTH / 2) - 100, 530)
        pg.display.flip()
        self.wait_for_key()

    # end screen stuff
    def show_game_over_screen(self):
        self.displayed_score = 0
        self.total_score = self.calculate_score()
        self.score_speed = max(1, self.total_score // 120)  # How fast the score rolls

        lock_time = 3500  # 3.5 seconds input lock
        start_time = pg.time.get_ticks()


        running_screen = True
        while running_screen:
            self.clock.tick(FPS)

            allow_input = (pg.time.get_ticks() - start_time) >= lock_time

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.playing = False
                    running_screen = False

                elif allow_input and (event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN):
                    running_screen = False  # Only exits AFTER 3.5 sec

            # Fill background
            self.screen.fill(BLACK)

            # Draw texts
            self.draw_text(self.screen, "GAME OVER", 64, RED, WIDTH / 2, HEIGHT / 4)
            self.draw_text(self.screen, f"Total Kills: {self.total_kills}", 32, WHITE, WIDTH / 2, HEIGHT / 2)
            if allow_input:
                self.draw_text(self.screen, "Click any button to Restart", 24, WHITE, WIDTH / 2, 700)
            else:
                self.draw_text(self.screen, "Loading Score...", 24, WHITE, WIDTH / 2, 700)
            # Update rolling scorete
            # Update rolling score manually
            # score animation
            if self.displayed_score < self.total_score:
                self.displayed_score += max(1, self.total_score // 120)
                if self.displayed_score > self.total_score:
                    self.displayed_score = self.total_score

            impact_font = pg.font.Font(pg.font.match_font('impact'), 35)
            rolling_text = impact_font.render(f"Score: {self.displayed_score}", True, WHITE)
            self.screen.blit(rolling_text, (WIDTH / 2 - 100, HEIGHT / 2 + 125))

            # Update the display
            pg.display.flip()


    def calculate_score(self):
        potion_score = self.player.potions_collected * 100
        time_score = self.time_survived * 1000
        coin_score = self.player.coins * 100
        potion_score = self.player.potions_collected * 100

        mob_score = 0
        for mob in self.all_mobs:
            if mob.power == 1:
                mob_score += 5
            elif mob.power == 2:
                mob_score += 10
            elif mob.power == 3:
                mob_score += 20

        total_score = time_score + coin_score + potion_score + mob_score
        return total_score

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.show_start_screen()
        g.new()
        g.run()

    pg.quit()
    sys.exit()