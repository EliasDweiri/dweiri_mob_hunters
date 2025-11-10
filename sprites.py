import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from utils import Cooldown
from utils import Spritesheet
from random import choice
from os import path
vec = pg.math.Vector2
 
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # animated sprite
        # self.spritesheet = Spritesheet(path.join(self.game.img_folder, "")) # PUT FILES HERE
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
        self.speed = 500
        self.health = 100
        # coins
        self.coins = 0
        # cooldown
        self.cd = Cooldown(1000)
        self.weapon_cd = Cooldown(400)
        self.dir = vec(0,0)
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0
        self.last_update = 0
        self.attack_hitbox = None
        self.attacking = False


    # def load_images(self): COME BACK TO THIS
    #     self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
    #                             self.spritesheet.get_image(0, 32, 32, 32)]

        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)
        # # self.walk_frames_r
        # # self.walk_frames_l
        # # pg.transform.flip
        
    # def animate(self): COME BAKC TO THIS
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.walking:
    #         if now - self.last_update > 350:
    #             print(now)
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
                    



    # def draw_attack(self, surf):
    #     if self.attack_hitbox:
    #         pg.draw.rect(surf, (255, 200,60,140), self.attack_hitbox)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()


        # when space is pressed shoot a projectile
        # when w is pressed the player moves up
        if keys[pg.K_w]:
            self.vel.y = -self.speed * self.game.dt
            self.dir = vec(0,-1)
            # self.rect.y -= self.speed


        # one form of attacking
        if keys[pg.K_p]:
            p = Projectile(self.game, self.rect.x, self.rect.y, self.dir)


        # when a is pressed the player moves to the left
        if keys[pg.K_a]:
            self.vel.x = -self.speed * self.game.dt
            self.dir = vec(-1,0)
            

            # self.rect.x -= self.speed


        # when s is pressed the player moves down
        if keys[pg.K_s]:
            self.vel.y = self.speed * self.game.dt
            self.dir = vec(0,1)


            # self.rect.y += self.speed
        # when d is pressed the player moves to the right
        if keys[pg.K_d]:
            self.vel.x = self.speed * self.game.dt
            self.dir = vec(1,0)

        # SPIN MOVEEEEEEE, ONLY WORKS IF 15 COINS ARE COLLECTED
        # if self.coins == 1:
        # if keys[pg.K_k]:
                
        #     print("trying to spin attack")

          
        # accounting for diagonal movement
        if self.vel.x != 0 and self.vel[1] != 0:
            self.vel *= 0.7071


    def attack(self):
        if not self.attacking and self.weapon_cd.ready():
            self.weapon_cd.start()
            self.attacking = True
            print("im attacking")
            self.weapon = Sword(self.game, self.rect.x, self.rect.y)
            
            
            


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
                    self.health -= 10
                    self.cd.start()
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
                print(self.coins)

    def update(self):
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

        # if self.attacking:
        #     Sword(self.game, self.rect.x, self.rect.y)



        # if not self.cd.ready():
        #     self.image_inv = self.game.player_img
        #     # self.rect = self.image.get_rect()
        #     # print("not ready")
        # else:
        #     self.image = self.game.player_img
        #     # self.rect = self.image.get_rect()
        #     # print("ready")
 
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        # creates the mob
        self.game = game
        # how big the mob is
        self.image = pg.Surface((32, 32))
        # mob color
        self.image = game.mob_img
        # self.image.set_colorkey() USE THIS TO REMOVE A BACKGROUND ON A SPRITE
        self.rect = self.image.get_rect()
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        # velocity
        self.vel = vec(choice([-1,1]), choice([-1,1]))
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # mob coordinates
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        # speed
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
                    # self.vel.x *= choice([-1, 1])  # optional: bounce off
                    self.rect.x = self.pos.x

                if dir == "y":
                    if self.vel.y > 0:
                        self.pos.y = hit.rect.top - self.rect.height
                    if self.vel.y < 0:
                        self.pos.y = hit.rect.bottom
                    # self.vel.y *= choice([-1, 1])  # optional: bounce off
                    self.rect.y = self.pos.y



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
        self.groups = game.all_sprites, game.all_weapons
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE[0]*2,TILESIZE[1]//2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y *TILESIZE[1]
    def update(self):
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
                    print("a wall collided with a wall")
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.x += self.vel.x
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.x = hits[1].rect.left - self.rect.width
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                        
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
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
                    print('wall y collide down')
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                        hits[0].pos.y += self.vel.y
                        if len(hits) > 1:
                            if hits[1].state == "unmoveable":
                                self.pos.y = hits[1].rect.top - self.rect.height
                    else:
                        self.pos.y = hits[0].rect.top - self.rect.height
                        
                if self.vel.y < 0:
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
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

class Projectile(Sprite):
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
        print
    def update(self):
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            self.kill()
