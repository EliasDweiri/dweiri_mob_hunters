import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from utils import Cooldown
from utils import Spritesheet
from random import choice
from os import path
import pygame
import math
vec = pg.math.Vector2
 
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # animated sprite
        # self.spritesheet = Spritesheet(path.join(self.game.img_folder, "spritesheet.png")) # PUT FILES HERE
        self.image = pg.Surface((32, 32))
        # creates the sprite
        # how big the sprite is
        # sprite color
        # self.image.fill(GREEN)
        self.image = game.player_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        # sprite coordinates
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        # velocity
        self.vel = vec(0, 0)
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # speed
        self.speed = 300
        self.health = 100
        # coins
        self.coins = 0
        # cooldown
        self.cd = Cooldown(1000)
        self.weapon_cd = Cooldown(400)
        self.effect_cd = Cooldown(200)
        self.dir = vec(0,0)
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0
        self.last_update = 0
        self.attack_hitbox = None
        self.attacking = False
        self.speed_boost_active = False
        self.speed_boost_amount = 0
        self.speed_boost_end_time = 0
        self.speed_timer = 0  # how long the boost lasts
        self.mace_cd = Cooldown(500) 


    def health_potion_pickup(self):
    # Check collision with health potions
        hits = pg.sprite.spritecollide(self, self.game.all_potions, True)
        for potion in hits:
            print("PLAYER PICKED UP HEALTH POTION!")
            self.health += 50
            if self.health > 100:  # optional max health
                self.health = 100


    def rotate(self):
        pass

    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
    #                             self.spritesheet.get_image(0, 32, 32, 32)]
    #     for frame in self.standing_frames:
    #         frame.set_colorkey(BLACK)
    #     # self.walk_frames_r
    #     # self.walk_frames_l
    #     # pg.transform.flip

    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.walking:
    #         if now - self.last_update > 350:
    #             # print(now)
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
    


    def get_keys(self):        
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()


        # when space is pressed shoot a projectile
        # when w is pressed the player moves up
        if keys[pg.K_w]:
            self.vel.y = -self.speed * self.game.dt
            self.dir = vec(0,-1)
            # self.rect.y -= self.speed


            self.image = self.game.player_img


        # when a is pressed the player moves to the left
        if keys[pg.K_a]:
            self.vel.x = -self.speed * self.game.dt
            self.dir = vec(-1,0)
            
            self.image = self.game.player_running_left




        # when s is pressed the player moves down
        if keys[pg.K_s]:
            self.vel.y = self.speed * self.game.dt
            self.dir = vec(0,1)

        


            # self.rect.y += self.speed
        # when d is pressed the player moves to the right
        if keys[pg.K_d]:
            self.vel.x = self.speed * self.game.dt
            self.dir = vec(1,0)
       
            self.image = self.game.player_running_right


        # accounting for diagonal movement
        if self.vel.x != 0 and self.vel[1] != 0:
            self.vel *= 0.7071


        # AXE
        if keys[pg.K_o]:
            # print(self.rect.x)
            Axe(self.game, self)


        if keys[pg.K_i]:  # Key to use Mace
            # Only spawn a Mace if cooldown is ready AND no other Mace exists
            if self.mace_cd.ready() and not any(isinstance(s, Mace) for s in self.game.all_sprites):
                Mace(self.game, self)   # Spawn the Mace
                self.mace_cd.start()    # Start cooldown


        if keys[pg.K_p]:
            p = Water_Shot(self.game, self.rect.x, self.rect.y, self.dir)


        # sword is found in events in main

    def attack(self):
        if not self.attacking and self.weapon_cd.ready():
            self.weapon_cd.start()
            self.attacking = True
            # print("im attacking")
            self.weapon = Sword(self.game, self.rect.x, self.rect.y)
            
        

    # USE THIS FOR POSSIBLE FIRE EFFECT
    # class EffectTrail(Sprite):
    #     def __init__(self, game, x, y):
    #         self.game = game
    #         self.groups = game.all_sprites
    #         Sprite.__init__(self, self.groups)
    #         self.image = pg.Surface(TILESIZE, pg.SRCALPHA)
    #         self.alpha = 255
    #         self.image.fill((255,255,255,255))
    #         self.rect = self.image.get_rect()
    #         self.cd = Cooldown(10)
    #         self.rect.x = x
    #         self.rect.y = y
    #         # coin behavior
    #         self.scale_x = 32
    #         self.scale_y = 32
    #     def update(self):
    #         if self.alpha <= 10:
    #             self.kill()
    #         self.image.fill((255,255,255,self.alpha))
            
    #         if self.cd.ready():
    #             self.scale_x -=1
    #             self.scale_y -=1
    #             print("I'm ready")
    #             self.alpha -= 50
    #             new_image = pg.transform.scale(self.image, (self.scale_x, self.scale_y))
    #             self.image = new_image

    def get_dir(self):
        return self.vel

    def collide_with_walls(self, dir):
        # handles collsion with walls
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # detects if the wall is moveable
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        # moves if the wall is moveable
                        hits[0].vel.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # detects if the wall is moveable
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        # moves if the wall is moveable
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].vel.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        # collides with mob
        # collides with coin
        # makes collisions happen
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 20
                    self.cd.start()
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
                print(self.coins)

    def update(self):
        # self.EffectTrail
        self.get_keys()

        # self.animate() COME BACK TO THIS
        # moves the player
        self.pos += self.vel
        self.rect.x = self.pos.x
        # handles collision with walls
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        # makes mob collide
        self.collide_with_stuff(self.game.all_mobs, False)
        # makes coin disappear
        self.collide_with_stuff(self.game.all_coins, True)

        self.health_potion_pickup()


        #  SPEED POTION PICKUP 

        speed_potion_hits = pg.sprite.spritecollide(self, self.game.all_potions, True)
        if speed_potion_hits:
            print("PLAYER PICKED UP SPEED POTION!")
            self.speed += 30
            self.speed_boost_active = True
            self.speed_timer = pg.time.get_ticks()

        # Remove speed boost after 12 seconds
        if self.speed_boost_active:
            if pg.time.get_ticks() - self.speed_timer >= 12000:
                print("Speed boost ended.")
                self.speed -= 50
                self.speed_boost_active = False
                # if self.attacking:
                #     Sword(self.game, self.rect.x, self.rect.y)



        # HEALTH POTION PICKUP

        health_hits = pg.sprite.spritecollide(self, self.game.all_potions, True)

        for potion in health_hits:
            if isinstance(potion, Health_Potion):
                print("HEALTH POTION PICKED UP!")
                self.health += 50
                if self.health > 100:
                    self.health = 100




        # if not self.cd.ready():
        #     self.image_inv = self.game.player_img
        #     # self.rect = self.image.get_rect()
        #     # print("not ready")
        # else:
        #     self.image = self.game.player_img
        #     # self.rect = self.image.get_rect()
        #     # print("ready")


    def apply_speed_boost(self, amount, duration):
        self.speed_boost_active = True
        self.speed_boost_amount = amount
        self.speed += amount
        self.speed_boost_end_time = pg.time.get_ticks() + duration
    
    def apply_health_boost(self, amount):
        self.health_boost_active = True
        self.health_amount = amount
        self.health += amount

# MACE
class Mace(Sprite):
    def __init__(self, game, owner, orbit_radius=30, start_angle=0):
        self.groups = game.all_sprites, game.all_weapons
        Sprite.__init__(self, self.groups)
        self.game = game
        self.owner = owner  # Player (or any object with .pos)

        self.total_rotation = 0  # Track how much the mace has spun

        self.mace_img = pg.image.load(path.join(self.game.img_folder, "Mace_60x15.png")).convert_alpha()
        self.base_image = self.mace_img

        # Define the local pivot on the sword image (the hilt)
        # Here we say the hilt is near the left side, centered vertically
        rect = self.base_image.get_rect()
        self.local_pivot = pg.math.Vector2(rect.left, rect.centery)

        # Vector from pivot (hilt) to the image center in local space
        self.pivot_to_center = pg.math.Vector2(rect.center) - self.local_pivot

        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Orbit info
        self.orbit_radius = orbit_radius
        self.angle = start_angle      # degrees around the player
        self.spin_speed = 500         # degrees per second (how fast it orbits)

        # Extra offset to make the sword point outward properly
        # (tweak as needed; 0, 90, 180, etc.)
        self.orientation_offset = 32
        # print("spinnging sword created")

    def update(self):

        # killing the sprite after 360
        rotation_increment = self.spin_speed * self.game.dt
        self.angle += rotation_increment
        self.total_rotation += rotation_increment

        if self.total_rotation >= 450:  # One full rotation
            self.kill()
            return
        
        # 2. Compute where the sword's pivot (hilt) should be in world space
        #    Orbit in a circle around the player's center
        orbit_offset = pg.math.Vector2(self.orbit_radius, 0).rotate(self.angle)
        sword_pivot_world = self.owner.pos + pg.math.Vector2(16, 16) + orbit_offset
        # 3. Rotate the sword image around its own pivot (hilt)
        image_angle = -self.angle + self.orientation_offset
        self.image = pg.transform.rotate(self.base_image, image_angle)
    
        # 4. Rotate the pivot->center offset by the same angle so the rect lines up
        rotated_pivot_to_center = self.pivot_to_center.rotate(image_angle)

        # 5. Final sprite center = pivot_world + rotated offset
        self.rect = self.image.get_rect(center=sword_pivot_world + rotated_pivot_to_center)



        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        for mob in hits:
            if mob.hit_cd.ready():
                mob.health -= 20
                mob.hit_cd.start()

                # Knockback edited to work without game.all_mobs
                knockback_dir = mob.pos - self.owner.pos
                if knockback_dir.length() != 0:
                    knockback_dir = knockback_dir.normalize()

                mob.pos += knockback_dir * 100   # <-- push strength
        
class Axe(Sprite):
    def __init__(self, game, player):
        self.game = game
        self.groups = game.all_sprites,
        Sprite.__init__(self, self.groups)
        self.player = player

        # Load axe sprite
        self.axe_img = pg.image.load(path.join(self.game.img_folder, "Axe_5x50.png")).convert_alpha()
        self.original_image = self.axe_img
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Rotation setup
        self.angle = 0
        self.radius = 40
        self.pivot_offset = pg.math.Vector2(0, -self.radius)

        # Fade out setup
        self.cd = Cooldown(10)
        self.alpha = 1000
    def update(self):

        # Fade-out logic
        if self.alpha <= 10:
            self.kill()

        if self.cd.ready():
            self.alpha -= 100

        # Apply alpha WITHOUT filling or overwriting the sprite
        self.image = self.original_image.copy()
        self.image.set_alpha(self.alpha)

        # Rotation math
        self.angle = (self.angle + 45) % 360
        rotated_offset = self.pivot_offset.rotate(self.angle)

        # Position the axe around the player
        self.rect.center = self.player.rect.center + rotated_offset

        # Rotate the sprite itself
        rotation_angle_for_image = -self.angle - 180
        self.image = pg.transform.rotate(self.image, rotation_angle_for_image)

        # Keep center consistent after rotation
        self.rect = self.image.get_rect(center=self.rect.center)


        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        for mob in hits:
            if mob.hit_cd.ready():
                mob.health -= 50
                mob.hit_cd.start()
                
                # knockback
                knockback_dir = mob.pos - self.player.pos
                if knockback_dir.length() != 0:
                    knockback_dir = knockback_dir.normalize()
                mob.pos += knockback_dir * 30


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        # creates the mob
        # how big the mob is
        self.image = pg.Surface((32, 32))
        # mob color
        self.image = game.mob_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        # self.image.fill(RED)
        # velocity
        self.vel = vec(choice([-1,1]), choice([-1,1]))
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # mob coordinates
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        # speed
        self.hit_cd = Cooldown(500)
        self.speed = 5
        self.health = 100
        print(self.pos)
        self.cd = Cooldown(300)

    def collide_with_walls(self, dir):
        # handles collision with walls
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                # bounces off in random direction
                self.vel.x *= choice([-1,1])
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                # bounces off in random direction
                self.vel.y *= choice([-1,1])

    
    def collide_with_mobs(self, dir):
    # Handle collisions between mobs
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        for hit in hits:
            if hit != self:  # Don't collide with self
                if dir == "x":
                    if self.vel.x > 0:
                        self.pos.x = hit.rect.left - self.rect.width
                    if self.vel.x < 0:
                        self.pos.x = hit.rect.right
                    self.rect.x = self.pos.x

                if dir == "y":
                    if self.vel.y > 0:
                        self.pos.y = hit.rect.top - self.rect.height
                    if self.vel.y < 0:
                        self.pos.y = hit.rect.bottom
                    self.rect.y = self.pos.y
    
    # def collide_with_weapons(self):
    #     hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
    #     if hits == True:




    def update(self):
        if self.health <= 0:
            self.kill()
        # mob behavior
        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
            # print("I don't need to chase the player x")
        if self.game.player.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
            # print("I don't need to chase the player y")
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        # updating mob v mob collision
        self.collide_with_mobs('x')
        self.collide_with_mobs('y')
 
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface(TILESIZE)
        # self.image.fill(GOLD)
        self.image = game.coin_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        # coin behavior
        pass

class Sword(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_weapons, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE[0]*2,TILESIZE[1]//2))
        # self.image.fill(WHITE) makes the sword white instead of sprite
        # self.image = pg.Surface((16, 64))
        # self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0] 
        self.rect.y = y * TILESIZE[1]
    def update(self):
        if self.game.player.dir == vec(-1, 0):  # facing left
            self.image = self.game.sword_left_img
        elif self.game.player.dir == vec(1, 0):  # facing right
            self.image = self.game.sword_right_img
        elif self.game.player.dir == vec(0, -1):
            self.image = self.game.sword_up_img
        elif self.game.player.dir == vec(0, 1):
            self.image = self.game.sword_down_img
        self.rect.x = self.game.player.rect.x + self.game.player.dir.x * 32
        if self.game.player.dir.x < 0:
            self.rect.x = self.game.player.rect.x + self.game.player.dir.x * 64
            # pg.transform.flip(self.image, True, False)
        self.rect.y = self.game.player.rect.y



 
class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.game.all_breakable_walls.add(self)
        self.image = pg.Surface(TILESIZE)
        # self.image.fill(GREY)
        self.image = game.wall_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # print("a wall collided with a wall")
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.right
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # print('wall y collide down')
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                        
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmovable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')




class Indestructible_Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        # self.image.fill(GREY)
        self.image = game.wall_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        # print("wall created at", str(self.rect.x), str(self.rect.y))
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # print("a wall collided with a wall")
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.right
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # print('wall y collide down')
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                        
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        # print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmovable":
                                self.pos.y = hits[1].rect.bottom
                    else:
                        self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        # wall
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')



class Water_Shot(Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        # self.image.fill(RED)
        self.image = game.projectile_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        self.vel = dir
        self.pos = vec(x,y)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # Regular walls (breakable)
        hits = pg.sprite.spritecollide(self, self.game.all_breakable_walls, True)
        if hits:
            self.kill()   # break wall + remove projectile

        # Indestructible walls 
        hits2 = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits2:
            self.kill()   # projectile dies but wall stays

# ------ POTIONS -------

class Speed_Potion(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_potions
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((32, 32))
        # self.image.fill((TURQUOISE))  # cyan potion
        self.image = game.speed_potion_img
        self.rect = self.image.get_rect()

        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]

    def update(self):
        # Potion does NOT handle collision
        # Player handles picking up potions
        pass


class Health_Potion(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_potions
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((32, 32))
        # self.image.fill((255, 0, 0))  # red potion
        self.image = game.health_potion_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]