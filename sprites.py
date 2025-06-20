import pygame,  random
from data.constants import *
vec = pygame.math.Vector2
     
class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color, size = (6, 6)):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        particle = pygame.Surface(size)
        particle.fill((color))
        
        self.image = particle.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x + random.randint(-3, 3)
        self.rect.centery = y + random.randint(-3, 3)
        self.vel = [random.uniform(-0.75, 0.75), random.uniform(-0.75, 0.75)]
        self.life = 60
        self.alpha = 255

    def update(self):
        self.rect.centerx += self.vel[0]
        self.rect.centery += self.vel[1]
        
        self.life -= 1

        self.alpha -= 4
        self.image.set_alpha(self.alpha)

        if self.life <= 0:
            self.kill()    
            
class Portal_Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        particle = pygame.Surface((4, 4))
        particle.fill((CREDITS_BUTTON))
        
        self.image = particle.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x + random.randint(-10, 10)
        self.rect.centery = y + random.randint(-10, 10)
        self.vel = [random.uniform(-0.75, 0.75), random.uniform(-0.75, 0.75)]
        self.life = 60
        self.alpha = 255

    def update(self):
        self.rect.centerx += self.vel[0]
        self.rect.centery += self.vel[1]
        
        self.life -= 1

        self.alpha -= 4
        self.image.set_alpha(self.alpha)

        if self.life <= 0:
            self.kill()  
            
class Demo_Particle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        particle = pygame.Surface((4, 4))
        particle.fill((LIGHT_GREY))
        
        self.image = particle.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x + random.randint(-3, -1)
        self.rect.y = y - random.randint(0, 5)
        self.vel = [random.uniform(-0.75, -0.25), random.uniform(-1.5, -0.25)]
        self.life = 60
        self.alpha = 255

    def update(self):
        self.rect.centerx += self.vel[0]
        self.rect.centery += self.vel[1]
        
        self.life -= 1

        self.alpha -= 4
        self.image.set_alpha(self.alpha)

        if self.life <= 0:
            self.kill()   
            
class Background_Particle(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.background_particles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        particle = pygame.Surface((4, 4))
        particle.fill((SLATE_GREY))
        
        self.image = particle.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, DISPLAY_WIDTH - 10)
        self.rect.y = 10
        self.vel = [random.uniform(-3, 3), random.uniform(4, 8)]
        self.life = random.randint(250, 300)
        self.alpha = 255

    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        
        self.life -= 1

        self.alpha -= random.randint(1, 2)
        self.image.set_alpha(self.alpha)

        if self.life <= 0 or self.alpha <= 0:
            self.kill()     
        
class Font(pygame.sprite.Sprite):
    def __init__(self, game, font, x, y, text):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = font
        self.image = self.font.render(text, False, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
    def change_text(self, x, y, text):
        self.image = self.font.render(text, False, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE 
        
class Button_Font(pygame.sprite.Sprite):
    def __init__(self, game, font, color, x, y, text):
        self.groups = game.button_text
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = font
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.color = color
        
    def change_text(self, x, y, text):
        self.image = self.font.render(text, False, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
                     
class Entity(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.green_ball_R[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = (x * TILE_SIZE) + TILE_SIZE
        self.rect.centery = (y * TILE_SIZE) + TILE_SIZE
        self.color_list = ['green', 'red', 'blue', 'yellow']
        self.color_selector = 0
        self.frame_coutner = 0
        self.frame_rate = 0.05
        
        self.position_tracker = 0
        
        self.lvl_4_position_list = [(x, y), (21, 21), (29, 9), (41, 3), 
                                    (67, 3), (47, 11), (63, 19), (63, 35), 
                                    (49, 35), (35, 15), (35, 29), (3, 29), 
                                    (3, 17), (15, 9)]
        
        self.lvl_7_position_list = [(x, y), (27, 13), (5, 13), (5, 21), (27, 29), 
                                    (15, 35), (37, 35), (37, 29), (37, 23), (37, 17), 
                                    (37, 11), (49, 7), (67, 15), (67, 25), (65, 33)]
        
        self.lvl_11_position_list = [(x,y), (17, 25), (29, 25), (7, 17), (7, 7), (37, 7), (65, 15), (53, 25), (41, 33)]
        
        self.end_position_list = [(x, y), (45, 13), (45, 5), (65, 21), (45, 33), (3, 33)]
        
    def update(self):
        if self.game.current_level == 'end':
            self.image = self.game.mono_ball_L[0]
        else:
            self.color_selector += self.frame_rate
            if self.color_selector >= len(self.color_list):
                self.color_selector = 0
        
            self.image = self.game.ballcycle[self.color_list[int(self.color_selector)] + '_R'][0]
        
        if self.game.current_level == '4':
            if self.position_tracker >= len(self.lvl_4_position_list):
                self.position_tracker = len(self.lvl_4_position_list) - 1
                
            self.rect.centerx = (self.lvl_4_position_list[self.position_tracker][0] * TILE_SIZE) + TILE_SIZE
            self.rect.centery = (self.lvl_4_position_list[self.position_tracker][1] * TILE_SIZE) + TILE_SIZE
        
        if self.game.current_level == '7':
            if self.position_tracker >= len(self.lvl_7_position_list):
                self.position_tracker = len(self.lvl_7_position_list) - 1
                
            self.rect.centerx = (self.lvl_7_position_list[self.position_tracker][0] * TILE_SIZE) + TILE_SIZE
            self.rect.centery = (self.lvl_7_position_list[self.position_tracker][1] * TILE_SIZE) + TILE_SIZE
            
        if self.game.current_level == '11':
            if self.position_tracker >= len(self.lvl_11_position_list):
                self.position_tracker = len(self.lvl_11_position_list) - 1
                
            self.rect.centerx = (self.lvl_11_position_list[self.position_tracker][0] * TILE_SIZE) + TILE_SIZE
            self.rect.centery = (self.lvl_11_position_list[self.position_tracker][1] * TILE_SIZE) + TILE_SIZE
            
        if self.game.current_level == 'end':
            if self.position_tracker >= len(self.end_position_list):
                self.position_tracker = len(self.end_position_list) - 1
                
            self.rect.centerx = (self.end_position_list[self.position_tracker][0] * TILE_SIZE) + TILE_SIZE
            self.rect.centery = (self.end_position_list[self.position_tracker][1] * TILE_SIZE) + TILE_SIZE
        
    def within(self, x, y):
        if self.rect.centerx - 128 < x < self.rect.centerx + 128 and self.rect.centery - 128 < y < self.rect.centery + 128:
            return True
        else:
            return False

class White_Entity(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mono_ball_L[0]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.position_tracker = 0
        self.positions = [(x, y), (67, 11), (57, 19), (67, 19), (67, 31), (43, 31)]
        
    def update(self):
        if self.position_tracker >= len(self.positions):
            self.position_tracker = len(self.positions) - 1
            
        self.rect.x = self.positions[self.position_tracker][0] * TILE_SIZE
        self.rect.y = self.positions[self.position_tracker][1] * TILE_SIZE
        
    def within(self, x, y):
        if self.rect.centerx - 128 < x < self.rect.centerx + 128 and self.rect.centery - 128 < y < self.rect.centery + 128:
            return True
        else:
            return False
         
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_3
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.grey_ball_R[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = (x * TILE_SIZE) + TILE_SIZE
        self.rect.centery = (y * TILE_SIZE) + TILE_SIZE
        
        #constants for the ball settings
        self.ball_speed = 6
        self.slower_speed = 1
        self.frame_rate = 0.25
        
        #variables to keep track of the ball state
        self.color_list = ['white', 'grey', 'green', 'red', 'blue', 'yellow']
        if self.game.current_level in self.game.white_lvls:
            self.color_selector = 0
        else:
            self.color_selector = 1
    
        self.dir_state = 'idle'
        self.transparency = 255
        
        #boolean variables
        self.facing_R = True
        self.moving_R = False
        self.small_state = False
        self.is_shrunk = False
        self.using_ability = False
        
        self.shrink_sound = False
        self.grow_sound = False
        self.invisible_sound = False
        
        self.change_color_menu = False
        
        #frame counter
        self.frame_counter = 0
        
    def movement(self):
        keystate = pygame.key.get_pressed()
        if not self.change_color_menu and self.game.can_move and self.game.pause_off:
            #if the player is going left
            if keystate[pygame.K_a]:
                self.moving_R = False
                self.facing_R = False
                
                self.rect.centerx -= self.ball_speed
                self.dir_state = 'left'

            #if the player is going right
            elif keystate[pygame.K_d]:
                self.moving_R = True
                self.facing_R = True
                
                self.rect.centerx += self.ball_speed
                self.dir_state = 'right'

            #if the player is going up
            elif keystate[pygame.K_w]:
                if self.facing_R:
                    self.moving_L = True
                else:
                    self.moving_R = True
                    
                self.rect.centery -= self.ball_speed
                self.dir_state = 'up'
                
            #if the player is going down
            elif keystate[pygame.K_s]:
                if self.facing_R:
                    self.moving_L = True
                else:
                    self.moving_R = True
                    
                self.rect.centery += self.ball_speed
                self.dir_state = 'down'
            
            #if the player is not moving
            else:
                self.dir_state = 'idle'
                
        #if the player uses an ability
        if not self.change_color_menu and self.game.pause_off:
            if keystate[pygame.K_SPACE]:
                self.using_ability = True
                if self.color_list[self.color_selector] == 'green':
                    if not self.shrink_sound:
                        self.game.sfx["shrink"].play()
                        self.shrink_sound = True
                        
                    self.small_state = True
                    self.shrink()

                elif self.color_list[self.color_selector] == 'red':
                    self.ball_speed = 9
                    
                elif self.color_list[self.color_selector] == 'yellow':
                    self.ball_speed = 3
                    
                elif self.color_list[self.color_selector] == 'blue':
                    if not self.invisible_sound:
                        self.game.sfx['invisible'].play()
                        self.invisible_sound = True
                        
                    self.transparency = 100
                        
            else:
                if self.small_state:
                    self.grow()
                    
                self.reset_abilities()
                
        #player color changing panel
        if self.game.current_level not in self.game.white_lvls and not self.using_ability and self.game.can_move and self.game.pause_off:
            if keystate[pygame.K_LSHIFT]:
                self.change_color_menu = True
                
                if self.dir_state != 'idle':
                    if self.dir_state == 'left':
                        self.rect.x -= self.slower_speed
                        
                    elif self.dir_state == 'right':
                        self.rect.x += self.slower_speed
                        
                    elif self.dir_state == 'up':
                        self.rect.y -= self.slower_speed
                        
                    elif self.dir_state == 'down':
                        self.rect.y += self.slower_speed
            
            else:
                self.change_color_menu = False
                
    def animate(self):
        #player sprite animation
        if self.dir_state != 'idle':
            if self.moving_R:
                self.frame_counter += self.frame_rate
                if self.frame_counter >= len(self.game.grey_ball_R):
                    self.frame_counter = 0
                    
                if self.small_state:
                    self.image = self.game.small_ball_R[int(self.frame_counter)]
                    
                else:      
                    self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_R'][int(self.frame_counter)]
                    
            else:
                self.frame_counter += self.frame_rate
                if self.frame_counter >= len(self.game.grey_ball_R):
                    self.frame_counter = 0
                
                if self.small_state:
                    self.image = self.game.small_ball_L[int(self.frame_counter)]
                    
                else:
                    self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_L'][int(self.frame_counter)]
                    
        else:
            if self.facing_R:
                if not self.small_state:
                    self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_R'][int(self.frame_counter)]
                
            else:
                if not self.small_state:
                    self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_L'][int(self.frame_counter)]
                    
        #set the transparency of the player
        self.image.set_alpha(self.transparency)
        
    def shrink(self):
        if not self.is_shrunk:
            self.is_shrunk = True
            if self.facing_R:
                self.image = self.game.small_ball_R[int(self.frame_counter)]
            else:
                self.image = self.game.small_ball_L[int(self.frame_counter)]
                
            self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))
    
    def grow(self):
        if self.is_shrunk:
            self.is_shrunk = False
            
            if self.facing_R:
                self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_R'][int(self.frame_counter)]
                
            else:
                self.image = self.game.ballcycle[self.color_list[self.color_selector] + '_L'][int(self.frame_counter)]
                
            self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))
            
    #method that resets all the ability trackers
    def reset_abilities(self):
        if self.small_state:
            self.game.sfx["grow"].play()
            
        self.small_state = False
        self.ball_speed = 6
        self.transparency = 255
        self.using_ability = False
        self.shrink_sound = False
        self.grow_sound = False
        self.invisible_sound = False
        
    def ability_collision(self):   
        #player sensor collision detection
        hits = pygame.sprite.spritecollide(self, self.game.sensors, False)
        if hits:
            if self.transparency != 100:
                self.game.playing = False
        
        #player boost tile collision detection
        hits = pygame.sprite.spritecollide(self, self.game.boost_tiles, False)
        if hits:
            if self.ball_speed != 9:
                self.game.playing = False
                
        #player slow tile collision detection
        hits = pygame.sprite.spritecollide(self, self.game.slow_tiles, False)
        if hits:
            if self.ball_speed != 3:
                self.game.playing = False
                
        #colored laser collision detection
        hits = pygame.sprite.spritecollide(self, self.game.red_lasers, True)
        if hits:
            self.game.sfx["laser"].play()
            if self.color_list[self.color_selector] != 'red':
                self.game.playing = False
                
        hits = pygame.sprite.spritecollide(self, self.game.yellow_lasers, True)
        if hits:
            self.game.sfx["laser"].play()
            if self.color_list[self.color_selector] != 'yellow':
                self.game.playing = False
                
        hits = pygame.sprite.spritecollide(self, self.game.green_lasers, True)
        if hits:
            self.game.sfx["laser"].play()
            if self.color_list[self.color_selector] != 'green':
                self.game.playing = False
                
        hits = pygame.sprite.spritecollide(self, self.game.blue_lasers, True)
        if hits:
            self.game.sfx["laser"].play()
            if self.color_list[self.color_selector] != 'blue':
                self.game.playing = False
    
    #update method
    def update(self):
        self.movement()
        self.ability_collision()
        self.animate()
            
class Tiles(pygame.sprite.Sprite):
    def __init__(self, game, x, y, idx):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        if self.game.current_level in self.game.white_lvls and idx == 6:
            self.image = pygame.Surface((64, 64))
            self.image.fill(BLACK)
        
        elif self.game.current_level == '15' and idx == 6:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            
        else:
            self.image = self.game.tileset[idx]
            
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Wall_laser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.wall_lasers
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        if dir == 'left':
            if self.game.current_level in self.game.white_lvls:
                self.image = pygame.Surface((8, 64))
                self.image.fill(BLACK)
            else:
                self.image = self.game.left_laser
                
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = y * TILE_SIZE
            self.mask = pygame.mask.from_surface(self.image)
            
        if dir == 'right':
            if self.game.current_level in self.game.white_lvls:
                self.image = pygame.Surface((8, 64))
                self.image.fill(BLACK)
            else:
                self.image = self.game.right_laser
                
            self.rect = self.image.get_rect()
            self.rect.x = (x * TILE_SIZE) + 56
            self.rect.y = y * TILE_SIZE
            self.mask = pygame.mask.from_surface(self.image)
            
        if dir == 'ceil':
            if self.game.current_level in self.game.white_lvls:
                self.image = pygame.Surface((64, 8))
                self.image.fill(BLACK)
            else:
                self.image = self.game.ceiling_laser
                
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = y * TILE_SIZE
            self.mask = pygame.mask.from_surface(self.image)
            
        if dir == 'floor':
            if self.game.current_level in self.game.white_lvls:
                self.image = pygame.Surface((64, 8))
                self.image.fill(BLACK)
            else:
                self.image = self.game.floor_laser
                
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = (y * TILE_SIZE) + 56
            self.mask = pygame.mask.from_surface(self.image)
            
class Sensor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.sensors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((128, 128))
        self.image.fill(BLUE)
        self.image.set_alpha(50)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Boost_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.boost_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.boost_tile
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Slow_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.slow_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.slow_tile
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Colored_Laser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color, orientation):
        self._layer = LAYER_2
        if color == 'red':
            self.groups = game.all_sprites, game.red_lasers
        elif color == 'yellow':
            self.groups = game.all_sprites, game.yellow_lasers
        elif color == 'green':
            self.groups = game.all_sprites, game.green_lasers
        elif color == 'blue':
            self.groups = game.all_sprites, game.blue_lasers
            
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        if orientation == 'ver':
            if color == 'red':
                self.image = self.game.red_laser_vertical
            elif color == 'yellow':
                self.image = self.game.yellow_laser_vertical
            elif color == 'green':
                self.image = self.game.green_laser_vertical
            elif color == 'blue':
                self.image = self.game.blue_laser_vertical
            
            self.rect = self.image.get_rect()
            self.rect.x = (x * TILE_SIZE) + 22
            self.rect.y = y * TILE_SIZE
            
        elif orientation == 'hor':
            if color == 'red':
                self.image = self.game.red_laser_horizontal
            elif color == 'yellow':
                self.image = self.game.yellow_laser_horizontal
            elif color == 'green':
                self.image = self.game.green_laser_horizontal
            elif color == 'blue':
                self.image = self.game.blue_laser_horizontal  
                
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = (y * TILE_SIZE) + 22
            
class Mine(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.mine_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mine
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)
        
class Clock(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.clock_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.clock_powerup
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Clock_Visual(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.clock_visual_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.clock_visual
        self.rect = self.image.get_rect()
        self.transparency = 255
        self.image.set_alpha(self.transparency)
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.is_collected = False
        
    def update(self):
        if self.is_collected:
            self.image.set_alpha(self.transparency)
            self.transparency -= 3
            
            if self.transparency < 0:
                self.kill()

class Colors(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.colors_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.colors[self.game.player.color_list[self.game.player.color_selector]]
        self.rect = self.image.get_rect()
        if self.game.player.facing_R:
            self.rect.x = self.game.player.rect.x + TILE_SIZE
            self.rect.y = self.game.player.rect.y - TILE_SIZE
        else:
            self.rect.x = self.game.player.rect.x - TILE_SIZE
            self.rect.y = self.game.player.rect.y - TILE_SIZE
        
    def update(self):
        if self.game.player.facing_R:
            self.rect.x = self.game.player.rect.x + TILE_SIZE
            self.rect.y = self.game.player.rect.y - TILE_SIZE
        else:
            self.rect.x = self.game.player.rect.x - TILE_SIZE
            self.rect.y = self.game.player.rect.y - TILE_SIZE
            
        self.image = self.game.colors[self.game.player.color_list[self.game.player.color_selector]]
        
class Start_Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y, flipped):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if flipped:
            self.image = self.game.start_portal_flipped
        else:
            self.image = self.game.start_portal
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class End_Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y, state):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.end_portals
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if state == "flipped":
            self.image = self.game.end_portal_flipped
        elif state == "normal":
            self.image = self.game.end_portal
        elif state == "mono":
            self.image = self.game.white_portal
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Direction_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.dir_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = dir
        
        if dir == 'right':
            self.image = self.game.right_dir_tile
            self.rect = self.image.get_rect()
            self.rect.x = (x * TILE_SIZE) + 16
            self.rect.y = y * TILE_SIZE
        
        elif dir == 'left':
            self.image = self.game.left_dir_tile
            self.rect = self.image.get_rect()
            self.rect.x = (x * TILE_SIZE) + 16
            self.rect.y = y * TILE_SIZE
            
        elif dir == 'up':
            self.image = self.game.up_dir_tile
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = (y * TILE_SIZE) + 16
        
        elif dir == 'down':
            self.image = self.game.down_dir_tile
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = (y * TILE_SIZE) + 16
            
        self.image.set_alpha(255)
               
    def set_opacity(self, alpha):
        self.image = self.image.copy()
        self.image.set_alpha(alpha)

class Sequence_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, order):
        self._layer = LAYER_1
        if order == 1:
            self.groups = game.all_sprites, game.order_1
            
        elif order == 2:
            self.groups = game.all_sprites, game.order_2
            
        elif order == 3:
            self.groups = game.all_sprites, game.order_3
            
        elif order == 4:
            self.groups = game.all_sprites, game.order_4
            
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tileset[6]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Sequence_Laser(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self._layer = LAYER_2
        self.groups = game.all_sprites, game.wall_lasers
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        
        if dir == 'vertical':
            self.image = self.game.sequence_laser
            self.rect = self.image.get_rect()
            self.rect.x = (x * TILE_SIZE) + 22
            self.rect.y = y * TILE_SIZE
            
        if dir == 'horizontal':
            self.image = self.game.sequence_laser_horizontal
            self.rect = self.image.get_rect()
            self.rect.x = x * TILE_SIZE
            self.rect.y = (y * TILE_SIZE) + 22
        
    def update(self):
        if self.game.sequence == 4:
            self.kill()
      
class Pressure_Plate(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.pressure_plate_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.pressure_plate
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Color_Torch(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.torch_colors['white']
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.frame_counter = 0
        self.frame_rate = 0.02
        self.collide = False
        
    def update(self):
        hits = pygame.sprite.spritecollide(self.game.player, self.game.pressure_plate_group, False)
        if hits:
            self.collide = True
            self.frame_counter += self.frame_rate
            
            if self.game.current_level == '10' or self.game.current_level == '12':
            
                if self.frame_counter >= len(self.game.torch_list_1):
                    self.frame_counter = 0
                
                if self.game.current_level == '10':
                    self.image = self.game.torch_colors[self.game.torch_list_1[int(self.frame_counter)]]
                else:
                    self.image = self.game.torch_colors[self.game.torch_list_2[int(self.frame_counter)]]
                    
            else:
                if self.frame_counter >= len(self.game.torch_list_3):
                    self.frame_counter = 0
        
                self.image = self.game.torch_colors[self.game.torch_list_3[int(self.frame_counter)]]
                
        else:
            self.collide = False
            self.image = self.game.torch_colors['white']
            self.frame_counter = 0
            
class Orange_Entity(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.final_boss[0]

        self.rect = self.image.get_rect()
        self.rect.x = (x * TILE_SIZE) - (2* TILE_SIZE)
        self.rect.y = y * TILE_SIZE
        
        self.transparency = 255
        self.image.set_alpha(self.transparency)
        
        self.counter = 0
        
        self.frame_counter = 0
        self.frame_rate = 0.25
        
        self.show_text = False
        self.change_text = False
        
    def update(self):
        
        self.counter += 0.03
        
        if self.counter < 1.5:
            self.rect.x += 3
            self.frame_counter += self.frame_rate
            if self.frame_counter >= len(self.game.final_boss):
                self.frame_counter = 0
            
            self.image = self.game.final_boss[int(self.frame_counter)]
            
        if self.counter >= 2 and self.counter < 5:
            self.show_text = True
        else:
            self.show_text = False
            
        if self.counter >= 4 and self.counter <= 7:
            self.change_text = True
        else:
            self.change_text = False
            
        if self.counter > 7:
            self.transparency -= 3
            self.image.set_alpha(self.transparency)
            
            if self.transparency <= 0:
                self.game.can_move = True
                self.kill()
            
class Snake_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, offset):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.snake_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tileset[6]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.offset = offset
        self.active = False
        
    def update(self):
        global_time = pygame.time.get_ticks()
        if global_time >= self.offset:
            self.image = self.game.lava_tile
            self.active = True
            
class Torch(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.torch_colors[color]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
            
class Torch_Combinations(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.torch_combinations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.frame_counter = 0
        self.frame_rate = 0.01
        
    def update(self):
        self.frame_counter += self.frame_rate
        
        if self.frame_counter >= len(self.game.torch_combinations):
            self.frame_counter = 0
        
        self.image = self.game.torch_combinations[int(self.frame_counter)]
        
class Outline(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.outline
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.large_mask
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
    def update(self):
        if self.game.player.small_state:
            self.image = self.game.small_mask
        else:
            self.image = self.game.large_mask
            
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.player.rect.centerx
        self.rect.centery = self.game.player.rect.centery
        
class Torch_Outline(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.torch_outline
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.small_mask
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
         
class Cursor(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.cursor_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.cursor
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        
class Game_Cursor(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.game_cursor_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.cursor
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0] - self.game.camera.camera.x
        self.rect.y = pygame.mouse.get_pos()[1] - self.game.camera.camera.y
                    
class Logo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.logo[0]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        self.frame_counter = 0
        self.frame_rate = 0.03
        
    def update(self):
        self.frame_counter += self.frame_rate
        
        if self.frame_counter >= len(self.game.logo):
            self.frame_counter = 0
            
        self.image = self.game.logo[int(self.frame_counter)]
        
class Start_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((480, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.start_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.start_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False 
                self.game.load_level_menu()
                       
        else:
            self.start_hover = False
            
class Setting_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((416, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.setting_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.setting_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False
                self.game.load_settings_menu()
                
        else:
            self.setting_hover = False
            
class Credit_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((352, 80))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.credit_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.credit_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False
                self.game.load_credits_menu()
                            
        else:
            self.credit_hover = False
            
class Exit_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((288, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.exit_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.exit_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False
                self.game.running = False
            
        else:
            self.exit_hover = False
            
class Resume_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((480, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.resume_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()
        if self.game.saved_level != 'tut':
            if self.rect.collidepoint(self.pos):
                self.resume_hover = True
                if pygame.mouse.get_pressed()[0] == 1:
                    self.game.menu_loop = False
                    self.game.playing = False
                    self.game.map = self.game.map_dict[self.game.saved_level]
                    if self.game.saved_level == '15':
                        self.game.final_level_music()
                    else:
                        self.game.switch_tracks()
                
            else:
                self.resume_hover = False
            
class New_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((416, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.new_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.new_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False
                self.game.playing = False
                self.game.current_level = 'tut'
                self.game.save_level("tut")
                self.game.cut_scene()
                
        else:
            self.new_hover = False
            
class Back_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((352, 80))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.back_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.back_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.menu_loop = False
                self.game.main_menu()
            
        else:
            self.back_hover = False
            
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == "red":
            self.image = pygame.Surface((480, 80))
            self.image.fill(RED)
            
        elif color == "yellow":
            self.image = pygame.Surface((416, 80))
            self.image.fill(YELLOW)
            
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Return_To_Game(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((416, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.return_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.return_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.pause_off = True
                self.game.pause_on = False
            
        else:
            self.return_hover = False   
            
class Return_To_Menu(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((416, 80))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.menu_hover = False
        
    def update(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.pos):
            self.menu_hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.game.playing = False
                self.game.pause_off = True
                self.game.pause_on = False
                self.game.main_menu()
            
        else:
            self.menu_hover = False   
            
class Menu_Snake_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, idx):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tileset[6]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.idx = idx
        
    def update(self):
        if self.idx < self.game.snake_sequence:
            self.image = self.game.lava_tile
            
        else:
            self.image = self.game.tileset[6]
            
class Menu_Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tileset[6]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Menu_Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_3
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.grey_ball_R[0]
        self.rect = self.image.get_rect()
        self.rect.x = (x * TILE_SIZE) - 100
        self.rect.y = y * TILE_SIZE
        self.frame_counter = 0
        self.frame_rate = 0.25
        self.reset = False
        
    def update(self):
        self.rect.x += 5
        
        if self.reset:
            self.rect.x = -100
            self.reset = False
            
        self.frame_counter += self.frame_rate
        
        if self.frame_counter >= len(self.game.grey_ball_R):
            self.frame_counter = 0
            
        self.image = self.game.grey_ball_R[int(self.frame_counter)]
        
class Music_Vol_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.sound_buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.box = pygame.Surface((20, 20))
        self.box.fill(BLACK)
        self.image = self.box.copy()
        
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.direction = direction
        
    def update(self):
        self.pos = pygame.mouse.get_pos()
        if self.direction == 'up':
            if self.rect.collidepoint(self.pos):
                self.image.fill(START_BUTTON_SHADOW)
            else:
                self.image.fill(BLACK)
            
        if self.direction == 'down':
            if self.rect.collidepoint(self.pos):
                self.image.fill(START_BUTTON_SHADOW)

            else:
                self.image.fill(BLACK)
                
    def change_volume(self, mouse_pos):
        if self.direction == 'up':
            if self.rect.collidepoint(mouse_pos):
                self.game.sfx["select"].play()
                if self.game.current_volume < 1:
                    self.game.current_volume += 0.1
                    pygame.mixer.music.set_volume(self.game.current_volume)
                    
        elif self.direction == "down":
            if self.rect.collidepoint(mouse_pos):
                self.game.sfx["select"].play()
                if self.game.current_volume > 0:
                    self.game.current_volume -= 0.1
                    pygame.mixer.music.set_volume(self.game.current_volume)
                    
class Sfx_Vol_Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.sound_buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.box = pygame.Surface((20, 20))
        self.box.fill(BLACK)
        self.image = self.box.copy()
        
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.direction = direction
        
    def update(self):
        self.pos = pygame.mouse.get_pos()
        if self.direction == 'up':
            if self.rect.collidepoint(self.pos):
                self.image.fill(SETTINGS_BUTTON_SHADOW)
            else:
                self.image.fill(BLACK)
            
        if self.direction == 'down':
            if self.rect.collidepoint(self.pos):
                self.image.fill(SETTINGS_BUTTON_SHADOW)

            else:
                self.image.fill(BLACK)
                
    def change_volume(self, mouse_pos):
        if self.direction == 'up':
            if self.rect.collidepoint(mouse_pos):
                if self.game.current_sfx_volume < 1:
                    self.game.current_sfx_volume += 0.1
                    self.game.set_sfx_volume(self.game.current_sfx_volume)
                    
                self.game.sfx['death'].play()
                
        elif self.direction == "down":
            if self.rect.collidepoint(mouse_pos):
                if self.game.current_sfx_volume > 0:
                    self.game.current_sfx_volume -= 0.1
                    self.game.set_sfx_volume(self.game.current_sfx_volume)
                    
                self.game.sfx['death'].play()
                
class Demo_Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = self.game.jump_R
        self.rect = self.image.get_rect()

        self.walking = False
        self.idle = False
        self.facing_R = True
        self.can_move = False

        self.frame_counter = 0
        self.frame_rate = 0.1
        self.idle_rate = 0.02
        
        self.pos = vec(x, y) * TILE_SIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def movement(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        
        keystate = pygame.key.get_pressed()
        if self.can_move:
            if keystate[pygame.K_d]:
                self.facing_R = True
                self.acc.x = PLAYER_ACC
                self.walking = True
                self.idle = False
                
            elif keystate[pygame.K_a]:
                self.facing_R = False
                self.acc.x = - PLAYER_ACC
                self.walking = True
                self.idle = False
            
        # player idle animation
        if self.idle:
            self.walking = False
            self.frame_counter += self.idle_rate

            if self.frame_counter >= len(self.game.idle_R):
                self.frame_counter = 0

            if self.facing_R:
                self.image = self.game.idle_R[int(self.frame_counter)]
            else:
                self.image = self.game.idle_L[int(self.frame_counter)]

        # player walking animation
        if self.walking:
            self.frame_counter += self.frame_rate

            if self.frame_counter >= len(self.game.walkcycle_R):
                self.frame_counter = 0

            if self.facing_R:
                self.image = self.game.walkcycle_R[int(self.frame_counter)]
            else:
                self.image = self.game.walkcycle_L[int(self.frame_counter)]
            
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def collide_with_walls(self, dir):      
        if dir == "x":
            hits = pygame.sprite.spritecollide(self, self.game.floors, False)
            if hits:
                #if player is going to the right
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width

                #if player is going to the left
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right

                self.rect.x = self.pos.x
                self.vel.x = 0

        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.floors, False)
            if hits:
                #if player is going down
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height

                self.idle = True
                self.can_move = True
                self.rect.y = self.pos.y
                self.vel.y = 0

    def collide_with_portal(self):
        hits = pygame.sprite.spritecollide(self, self.game.demo_portal, False)
        if hits:
            self.game.menu_loop = False
            self.game.map = self.game.map_dict["tut"]
            self.game.switch_tracks()

    def update(self):
        self.movement()
        self.collide_with_portal()
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        
        if self.rect.x > 500 and self.rect.x < 700:
            self.game.text.change_text(14, 13, "how am I still alive")
            
        elif self.rect.x > 750 and self.rect.x < 950:
            self.game.text.change_text(24, 13, "I thought I died")
            
        elif self.rect.x > 1050 and self.rect.x < 1250:
            self.game.text.change_text(34, 13, "not again")
            
        elif self.rect.x > 1260 and self.rect.x < 1440:
            self.game.text.change_text(38, 13, "phew, atleast this bridge is sturdy")
            
        elif self.rect.x > 1750 and self.rect.x < 1900:
            self.game.text.change_text(61, 13, "here we go again")
               
        elif self.rect.x < 80:
            self.game.text.change_text(3, 13, "woah, it's a wall")
        else:
            self.game.text.change_text(0, 0, "")
        
class Floor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, idx):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.floors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tileset[idx]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Bridge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites, game.floors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bridge
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Light_Ray(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.light
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.light_ray
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Demo_Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_3
        self.groups = game.all_sprites, game.demo_portal
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.end_portal
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
class Small_Ball_Outline(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = LAYER_2
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.green_ball_R[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.player.rect.centerx
        self.rect.centery = self.game.player.rect.centery
        self.dx = 0
        self.dy = 0
        self.offset = 7
        
    def update(self):
        #calculate offset
        if self.game.player.dir_state == 'up':
            self.dx = 0
            self.dy = -self.offset
        elif self.game.player.dir_state == 'down':
            self.dx = 0
            self.dy = self.offset
        elif self.game.player.dir_state == 'right':
            self.dx = self.offset
            self.dy = 0
        elif self.game.player.dir_state == 'left':
            self.dx = -self.offset
            self.dy = 0
        else:
            self.dx = 0
            self.dy = 0
        
        #update pos
        self.rect.centerx = self.game.player.rect.centerx + self.dx
        self.rect.centery = self.game.player.rect.centery + self.dy
        
        #update image
        if self.game.player.facing_R:
            frame = self.game.green_ball_R[int(self.game.player.frame_counter)]
        else:
            frame = self.game.green_ball_L[int(self.game.player.frame_counter)]
        self.image = frame.copy()
        
        #set transparency 
        if self.game.player.small_state:
            self.image.set_alpha(40)
        else:
            self.image.set_alpha(0)
            
class Mouse_Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER_1
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.box = pygame.Surface((64, 64))
        self.box.fill(SETTINGS_BUTTON)
        self.image = self.box.copy()
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
    def update(self):
        hits = pygame.sprite.spritecollide(self, self.game.game_cursor_group, False)
        if hits:
            self.image.fill(SETTINGS_BUTTON_SHADOW)
        
        else:
            self.image.fill(SETTINGS_BUTTON)
        