#import modules
import pygame, sys
from data.constants import *
from data.sprites import *
from data.tools import *
             
#game class
class Game():
    #default method
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init() 
        
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Swift-2-v1.0.0')
        self.running = True
        self.increment = False
        
        #variable to keep track of current track
        self.current_track = None
        
        #create timer
        self.timer = pygame.USEREVENT
        pygame.time.set_timer(self.timer, 1000)
        
        #for particles
        self.spawn_timer = 0
        
        #temp directories
        self.img_dir = "Swift_2/data/img/"
        self.map_dir = "Swift_2/data/maps/"
        self.font_dir = "Swift_2/data/font/"
        self.save_dir = "Swift_2/data/save/"
        self.sfx_dir = "Swift_2/data/sfx/"
        self.music_dir = "Swift_2/data/music/"
        
        #final directories
        # self.img_dir = "data/img/"
        # self.map_dir = "data/maps/"
        # self.font_dir = "data/font/"
        # self.save_dir = "data/save/"
        # self.sfx_dir = "data/sfx/"
        # self.music_dir = "data/music/"
        
        #get the current level
        self.current_level = self.load_level()
        
        #rest times for each level
        self.reset_timer = {
            'tut' : 0,
            '1' : 0,
            '2' : 80,
            '3' : 45,
            '4' : 0,
            '5' : 80,
            '6' : 80,
            '7' : 0,
            '8' : 0,
            '9' : 80,
            '10' : 120,
            '11' : 0,
            '12' : 80,
            '13' : 90,
            '14' : 0,
            '15' : 0,
            'end' : 0
        }
        
        #get the count down timer for the current level
        self.count_down = self.reset_timer[self.current_level]
        
        #list of levels with no timer
        self.no_timer = ['tut', '1', '4', '7', '8', '11', '14', '15', 'end']
        
        #list of levels with direction tiles
        self.dir_tile_lvls = ['5', '6', '12', '13', '14', '15']
        
        #list of levels with dimmed environment
        self.dim_lvls = ['12', '13', '14']
        
        #list of white (dream) levels
        self.white_lvls = ['4', '7', '11', 'end']
        
        #variable for lvl 12 and 13
        self.alpha_lvl = 0
        
        #variable for level 14
        self.death_counter = -1
        
        #variable for sequence tiles
        self.sequence  = 0
        self.collide_1 = False
        self.collide_2 = False
        self.collide_3 = False
        self.collide_4 = False
        
        #boolean for pause menu
        self.pause_on = False
        self.pause_off = True
        
        #varaible for level 15
        self.can_move = True
        self.delay = 3800
        self.wave_speed = 120
        
        self.snake_path = [
            (0,6),(0,8),(2,6),(2,8),(4,6),(4,8),(6,6),(6,8),(8,6),(8,8),(10,6),(10,8),(12,6),(12,8),(14,6),
            (14,8),(16,6),(16,8),(18,6),(18,8),(16,10),(18,10),(16,12),(18,12),(16,14),(18,14),(20,12),
            (20,14),(22,12),(22,14),(24,12),(24,14),(26,12),(26,14),(28,12),(28,14),(30,12),(30,14),
            (32,12),(32,14),(34,12),(34,14),(36,12),(36,14),(38,12),(38,14),(38,16),(36,16),(38,18),
            (36,18),(38,20),(36,20),(38,22),(36,22),(38,24),(36,24),(38,26),(36,26),(34,24),(34,26),
            (32,24),(32,26),(30,24),(30,26),(28,24),(28,26),(26,24),(26,26),(24,24),(24,26),(22,24),
            (22,26),(20,24),(20,26),(18,24),(18,26),(16,24),(16,26),(14,26),(14,24),(16,22),(14,22),
            (16,20),(14,20),(16,18),(14,18),(12,18),(12,20),(10,18),(10,20),(8,18),(8,20),(6,18),
            (6,20),(4,18),(4,20),(2,18),(2,20),(2,22),(4,22),(2,24),(4,24),(2,26),(4,26),(2,28),
            (4,28),(2,30),(4,30),(2,32),(4,32),(2,34),(4,34),(2,36),(4,36),(6,34),(6,36),(8,34),(8,36),
            (10,34),(10,36),(12,34),(12,36),(14,34),(14,36),(16,34),(16,36),(18,34),(18,36),(20,34),
            (20,36),(22,34),(22,36),(24,34),(24,36),(26,34),(26,36),(28,34),(28,36),(30,34),(30,36),
            (32,34),(32,36),(34,34),(34,36),(36,34),(36,36),(38,34),(38,36),(40,34),(40,36),(42,34),
            (42,36),(44,34),(44,36),(46,34),(46,36),(48,36),(48,34),(46,32),(48,32),(46,30),(48,30),
            (46,28),(48,28),(46,26),(48,26),(46,24),(48,24),(46,22),(48,22),(50,22),(50,24),(52,22),
            (52,24),(54,22),(54,24),(56,22),(56,24),(58,24),(58,22),(56,20),(58,20),(56,18),(58,18),
            (56,16),(58,16),(56,14),(58,14),(56,12),(58,12),(56,10),(58,10),(56,8),(58,8),(56,6),
            (58,6),(60,6),(60,8),(62,6),(62,8),(64,6),(64,8),(66,6),(66,8),(68,6),(68,8),(68,10),(66,10),
            (68,12),(66,12),(68,14),(66,14),(68,16),(66,16),(68,18),(66,18),(68,20),(66,20),(68,22),
            (66,22),(68,24),(66,24),(68,26),(66,26),(68,28),(66,28),(68,30),(66,30),(68,32),(66,32),
            (64,30),(64,32),(62,30),(62,32),(60,30),(60,32),(58,30),(58,32),(56,30),(56,32),(54,30),
            (54,32),(54,34),(56,34),(54,36),(56,36),(58,36),(60,36),(62,36),(64,36),(66,36),(68,36),
            (68,38),(66,38),
            
            (68, 40), (66, 40), (68, 42), (66, 42), (68, 44), (66, 44), (68, 46), (66, 46), (68, 48), (66, 48), 
            (68, 50), (66, 50), (64, 48), (64, 50), (62, 48), (62, 50), (60, 48), (60, 50), (58, 48), (58, 50), 
            (56, 48), (56, 50), (54, 48), (54, 50), (54, 52), (56, 52), (54, 54), (56, 54), (54, 56), (56, 56), 
            (54, 58), (56, 58), (54, 60), (56, 60), (54, 62), (56, 62), (58, 60), (58, 62), (60, 60), (60, 62), 
            (62, 60), (62, 62), (64, 60), (64, 62), (66, 60), (66, 62), (68, 60), (68, 62), (68, 64), (66, 64), 
            (68, 66), (66, 66), (68, 68), (66, 68), (68, 70), (66, 70), (68, 72), (66, 72), (68, 74), (66, 74), 
            (68, 76), (66, 76), (64, 74), (64, 76), (62, 74), (62, 76), (60, 74), (60, 76), (58, 74), (58, 76), 
            (56, 74), (56, 76), (54, 74), (54, 76), (52, 74), (52, 76), (50, 74), (50, 76), (48, 74), (48, 76), 
            (46, 76), (46, 74), (48, 72), (46, 72), (48, 70), (46, 70), (48, 68), (46, 68), (48, 66), (46, 66), 
            (48, 64), (46, 64), (48, 62), (46, 62), (48, 60), (46, 60), (44, 60), (44, 62), (42, 60), (42, 62), 
            (40, 60), (40, 62), (38, 62), (38, 60), (38, 58), (40, 58), (38, 56), (40, 56), (38, 54), (40, 54), 
            (38, 52), (40, 52), (38, 50), (40, 50), (38, 48), (40, 48), (42, 48), (42, 50), (44, 48), (44, 50), 
            (46, 48), (46, 50), (48, 50), (48, 48), (48, 46), (46, 46), (48, 44), (46, 44), (48, 42), (46, 42), 
            (44, 42), (44, 44), (42, 42), (42, 44), (40, 42), (40, 44), (38, 42), (38, 44), (36, 42), (36, 44), 
            (34, 42), (34, 44), (32, 42), (32, 44), (30, 42), (30, 44), (28, 42), (28, 44), (26, 42), (26, 44), 
            (24, 42), (24, 44), (22, 42), (22, 44), (20, 42), (20, 44), (18, 42), (18, 44), (16, 42), (16, 44), 
            (14, 42), (14, 44), (12, 42), (12, 44), (10, 42), (10, 44), (8, 42), (8, 44), (6, 42), (6, 44), 
            (4, 42), (4, 44), (2, 42), (2, 44), (2, 46), (4, 46), (2, 48), (4, 48), (2, 50), (4, 50), (2, 52), 
            (4, 52), (6, 50), (6, 52), (8, 50), (8, 52), (10, 50), (10, 52), (12, 50), (12, 52), (10, 54), 
            (12, 54), (10, 56), (12, 56), (14, 54), (14, 56), (16, 54), (16, 56), (14, 58), (16, 58), 
            (14, 60), (16, 60), (18, 58), (18, 60), (20, 58), (20, 60), (18, 62), (20, 62), (18, 64), 
            (20, 64), (22, 62), (22, 64), (24, 62), (24, 64), (24, 66), (22, 66), (24, 68), (22, 68), 
            (24, 70), (22, 70), (20, 70), (18, 70), (16, 70), (14, 70), (12, 70), (10, 70), (12, 68), 
            (10, 68), (12, 66), (10, 66), (12, 64), (10, 64), (8, 64), (8, 66), (6, 64), (6, 66), (4, 64), 
            (4, 66), (2, 64), (2, 66), (2, 68), (4, 68), (2, 70), (4, 70), (2, 72), (4, 72), (2, 74), 
            (4, 74), (2, 76), (4, 76), (6, 74), (6, 76), (8, 74), (8, 76), (10, 74), (10, 76), (12, 74), 
            (12, 76), (14, 74), (14, 76), (16, 74), (16, 76), (18, 74), (18, 76), (20, 74), (20, 76), 
            (22, 74), (22, 76), (24, 74), (24, 76), (26, 74), (26, 76), (28, 74), (28, 76), (30, 74), 
            (30, 76), (32, 74), (32, 76), (34, 74), (34, 76), (36, 74), (36, 76), (38, 74), (38, 76), 
            (40, 76), (40, 74), (40, 72), (38, 72), (40, 70), (38, 70), (40, 68), (38, 68), (36, 68), 
            (36, 70), (34, 68), (34, 70), (32, 68), (32, 70), (30, 70), (30, 68), (32, 66), (30, 66), 
            (32, 64), (30, 64), (32, 62), (30, 62), (32, 60), (30, 60), (32, 58), (30, 58), (32, 56), 
            (30, 56), (32, 54), (30, 54), (32, 52), (30, 52), (32, 50), (30, 50), (32, 48), (30, 48), 
            (28, 48), (28, 50), (26, 48), (26, 50), (24, 48), (24, 50), (22, 48), (22, 50)
        ]

        #load the game assets
        self.load_assets()
        
        #load audio files
        self.load_audio()
        
        #set the initial vol of the music and sfx
        self.current_volume = 0
        pygame.mixer.music.set_volume(self.current_volume)
        
        self.current_sfx_volume = 0
        self.set_sfx_volume(self.current_sfx_volume)
        
    def save_level(self, level):
        filename = self.save_dir + "level_data.txt"
        with open(filename, "w") as file:
            file.write(str(level))
            
    def load_level(self):
        filename = self.save_dir + "level_data.txt"
        with open(filename, "r") as file:
            return file.read()
        
    def switch_tracks(self):
        if self.current_track == self.track_1:
            next_track = self.track_2
        else:
            next_track = self.track_1

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music_dir + next_track)
        pygame.mixer.music.play(-1)   
        self.current_track = next_track
        
    def final_level_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music_dir + self.boss_music)
        pygame.mixer.music.play(-1)        

    def set_sfx_volume(self, volume):
        for sound in self.sfx.values():
            sound.set_volume(volume)
        
    def reset(self):
        self.collide_1 = False
        self.collide_2 = False
        self.collide_3 = False
        self.collide_4 = False
        self.sequence = 0
        
    #method for loading game assets
    def load_assets(self):
        #moving player walkcycle sprites
        walkcycle = SpriteSheet(pygame.image.load(self.img_dir + "walkcycle_spritesheet.png"), (16,16), 6)
        
        self.walkcycle_R = []
        for row in range (3):
            for col in range(3):
                img = walkcycle.get_image(col, row, False)
                self.walkcycle_R.append(img)
        
        del self.walkcycle_R[8]
                
        self.walkcycle_L = []
        for row in range (3):
            for col in range(3):
                img = walkcycle.get_image(col, row, True)
                self.walkcycle_L.append(img)
          
        del self.walkcycle_L[8] 
        
        #moving player idle sprites
        idle = SpriteSheet(pygame.image.load(self.img_dir + "idle_spritesheet.png"), (16,16), 6)
        
        self.idle_R = []
        
        for row in range(2):
            img = idle.get_image(0, row, False)
            self.idle_R.append(img)
            
        self.idle_L = []
        
        for row in range(2):
            img = idle.get_image(0, row, True)
            self.idle_L.append(img)
        
        #moving player jump sprite
        jump = pygame.image.load(self.img_dir + "jump.png").convert()
        self.jump = pygame.transform.scale(jump, (96,96))
        self.jump.set_colorkey(BLACK)
        
        self.jump_R = self.jump
        self.jump_L = pygame.transform.flip(self.jump, True, False)
        
        #player ball state sprites - grey
        grey_ball = SpriteSheet(pygame.image.load(self.img_dir + "grey_ball_spritesheet.png"), (16, 16), 4)
        
        self.grey_ball_R = []
        
        for col in range(6):
            img = grey_ball.get_image(col, 0, False)
            self.grey_ball_R.append(img)
        
        self.grey_ball_L = []
        
        for col in range(6):
            img = grey_ball.get_image(col, 0, True)
            self.grey_ball_L.append(img)
            
        #player ball state sprites - green
        green_ball = SpriteSheet(pygame.image.load(self.img_dir + "green_ball_spritesheet.png"), (16, 16), 4)
        
        self.green_ball_R = []
        
        for col in range(6):
            img = green_ball.get_image(col, 0, False)
            self.green_ball_R.append(img)
            
        self.green_ball_L = []
        
        for col in range(6):
            img = green_ball.get_image(col, 0, True)
            self.green_ball_L.append(img)
        
        #player ball state sprites - yellow    
        yellow_ball = SpriteSheet(pygame.image.load(self.img_dir + "yellow_ball_spritesheet.png"), (16, 16), 4)
        
        self.yellow_ball_R = []
        
        for col in range(6):
            img = yellow_ball.get_image(col, 0, False)
            self.yellow_ball_R.append(img)
            
        self.yellow_ball_L = []
        
        for col in range(6):
            img = yellow_ball.get_image(col, 0, True)
            self.yellow_ball_L.append(img)
        
        #player ball state sprites - blue
        blue_ball = SpriteSheet(pygame.image.load(self.img_dir + "blue_ball_spritesheet.png"), (16, 16), 4)
        
        self.blue_ball_R = []
        
        for col in range(6):
            img = blue_ball.get_image(col, 0, False)
            self.blue_ball_R.append(img)
            
        self.blue_ball_L = []
        
        for col in range(6):
            img = blue_ball.get_image(col, 0, True)
            self.blue_ball_L.append(img)
            
        #player ball state sprites - red
        red_ball = SpriteSheet(pygame.image.load(self.img_dir + "red_ball_spritesheet.png"), (16, 16), 4)
        
        self.red_ball_R = []
        
        for col in range(6):
            img = red_ball.get_image(col, 0, False)
            self.red_ball_R.append(img)
            
        self.red_ball_L = []
        
        for col in range(6):
            img = red_ball.get_image(col, 0, True)
            self.red_ball_L.append(img)
            
        #player ball state - greyscale
        mono_ball = SpriteSheet(pygame.image.load(self.img_dir + "mono_ball.png"), (16, 16), 4)
        
        self.mono_ball_R = []
        
        for col in range(6):
            img = mono_ball.get_image(col, 0, False)
            self.mono_ball_R.append(img)
            
        self.mono_ball_L = []
        
        for col in range(6):
            img = mono_ball.get_image(col, 0, True)
            self.mono_ball_L.append(img)   
                    
        #dictionary for player ball sprite lists
        self.ballcycle = {
            "grey_L": self.grey_ball_L,
            "grey_R": self.grey_ball_R,
            "green_L": self.green_ball_L,
            "green_R": self.green_ball_R,
            "yellow_L": self.yellow_ball_L,
            "yellow_R": self.yellow_ball_R,
            "blue_L": self.blue_ball_L,
            "blue_R": self.blue_ball_R,
            "red_L": self.red_ball_L,
            "red_R": self.red_ball_R,
            "white_L" : self.mono_ball_L,
            "white_R" : self.mono_ball_R
        }
        
        small_ball = SpriteSheet(pygame.image.load(self.img_dir + "small_ball_spritesheet.png"), (4, 4), 4)
        
        #player ball state - small
        self.small_ball_R = []
        
        for col in range(6):
            img = small_ball.get_image(col, 0, False)
            self.small_ball_R.append(img)
            
        self.small_ball_L = []
        
        for col in range(6):
            img = small_ball.get_image(col, 0, True)
            self.small_ball_L.append(img)  
        
        #final boss ball state
        final_boss = SpriteSheet(pygame.image.load(self.img_dir + "final_boss.png"), (16, 16), 4)
        
        self.final_boss = []
        
        for col in range(6):
            img = final_boss.get_image(col, 0, False)
            self.final_boss.append(img)
        
        #game tile spritesheet
        tilesheet = SpriteSheet(pygame.image.load(self.img_dir + "tile_spritesheet.png"), (16, 16), 4)
        
        self.tileset = []
        
        for row in range(5):
            for col in range(5):
                img = tilesheet.get_image(col, row, False)
                self.tileset.append(img)
                
        #wall laser sprites
        self.floor_laser = pygame.transform.scale(pygame.image.load(self.img_dir + "wall_laser.png").convert(), (64, 8))
        self.floor_laser.set_colorkey(BLACK)
        self.ceiling_laser = pygame.transform.flip(self.floor_laser, False, True)
        self.right_laser = pygame.transform.rotate(self.floor_laser, -90)
        self.left_laser = pygame.transform.rotate(self.floor_laser, 90)
        
        #boost tile
        self.boost_tile = pygame.transform.scale(pygame.image.load(self.img_dir + "boost_tile.png").convert(), (64, 64))
        self.boost_tile.set_colorkey(BLACK)
        
        #slow tile
        self.slow_tile = pygame.transform.scale(pygame.image.load(self.img_dir + "slow_tile.png").convert(), (64, 64))
        self.slow_tile.set_colorkey(BLACK)
        
        #colored lasers
        colored_lasers_img = pygame.image.load(self.img_dir + "colored_lasers.png").convert()
        colored_lasers_vertical = SpriteSheet(colored_lasers_img, (5, 32), 4)
        colored_lasers_horizontal = SpriteSheet(pygame.transform.rotate(colored_lasers_img, -90), (32, 5), 4)
        
        self.red_laser_vertical = colored_lasers_vertical.get_image(0, 0, False)
        self.yellow_laser_vertical = colored_lasers_vertical.get_image(1, 0, False)
        self.green_laser_vertical = colored_lasers_vertical.get_image(2, 0, False)
        self.blue_laser_vertical = colored_lasers_vertical.get_image(3, 0, False)

        self.red_laser_horizontal = colored_lasers_horizontal.get_image(0, 0, False)
        self.yellow_laser_horizontal = colored_lasers_horizontal.get_image(0, 1, False)
        self.green_laser_horizontal = colored_lasers_horizontal.get_image(0, 2, False)
        self.blue_laser_horizontal = colored_lasers_horizontal.get_image(0, 3, False)
        
        #mine
        self.mine = pygame.transform.scale(pygame.image.load(self.img_dir + "mine.png").convert(), (16, 16))
        self.mine.set_colorkey(BLACK)
        
        #clock powerup
        self.clock_powerup = pygame.transform.scale(pygame.image.load(self.img_dir + "clock.png"), (32, 32))
        self.clock_visual = pygame.transform.scale(pygame.image.load(self.img_dir + "clock_visual.png"), (32, 32))
        
        #portals
        self.start_portal = pygame.transform.scale(pygame.image.load(self.img_dir + "start_portal.png").convert(), (64, 64))
        self.start_portal.set_colorkey(BLACK)
        self.start_portal_flipped = pygame.transform.flip(self.start_portal, True, False)

        self.end_portal = pygame.transform.scale(pygame.image.load(self.img_dir + "end_portal.png").convert(), (64, 64))
        self.end_portal.set_colorkey(BLACK)
        self.end_portal_flipped = pygame.transform.flip(self.end_portal, True, False)

        self.white_portal = pygame.transform.scale(pygame.image.load(self.img_dir + "white_portal.png").convert(), (64, 64))
        self.white_portal.set_colorkey(BLACK)
        
        #color changing menu
        color_changer = SpriteSheet(pygame.image.load(self.img_dir + "color_changer.png"), (16, 16), 4)
        
        self.colors = {
            'grey' : color_changer.get_image(0, 0, False),
            'green' : color_changer.get_image(1, 0, False),
            'red' : color_changer.get_image(2, 0, False),
            'blue' : color_changer.get_image(3, 0, False),
            'yellow' : color_changer.get_image(4, 0, False)
        }
        
        #direction tiles 
        self.right_dir_tile = pygame.transform.scale(pygame.image.load(self.img_dir + "direction_tile.png").convert(), (32, 128))
        self.right_dir_tile.set_colorkey(BLACK)        
        self.left_dir_tile = pygame.transform.flip(self.right_dir_tile, True, False)        
        self.up_dir_tile = pygame.transform.rotate(self.right_dir_tile, 90)
        self.down_dir_tile = pygame.transform.rotate(self.left_dir_tile, 90)
        
        #torches
        torches = SpriteSheet(pygame.image.load(self.img_dir + "torches_spritesheet.png"), (16, 16), 4)

        self.torches = []
        
        for row in range (2):
            for col in range(5):
                img = torches.get_image(col, row, False)
                self.torches.append(img)
        
        #torch dictionary 
        self.torch_colors = {
            'magenta' : self.torches[0],
            'orange' : self.torches[1],
            'light_yellow' : self.torches[2],
            'dark_blue' : self.torches[3],
            'teal' : self.torches[4],
            'red' : self.torches[5],
            'yellow' : self.torches[6],
            'green' : self.torches[7],
            'blue' : self.torches[8],
            'white' : self.torches[9]
        }
        
        self.torch_list_1 = ['blue', 'red', 'yellow', 'green', 'white']
        self.torch_list_2 = ['yellow', 'green', 'red', 'blue', 'white']
        self.torch_list_3 = ['red', 'green', 'red', 'blue', 'yellow', 'blue', 'white']
                
        #torch color combination visuals
        torch_combinations = SpriteSheet(pygame.image.load(self.img_dir + "torch_combinations.png"), (48, 16), 4)
        
        self.torch_combinations = []
        for row in range(4):
            img = torch_combinations.get_image(0, row, False)
            self.torch_combinations.append(img)
            
        #sequence lasers
        self.sequence_laser = pygame.transform.scale(pygame.image.load(self.img_dir + "sequence_laser.png").convert(), (20, 128))
        self.sequence_laser.set_colorkey(BLACK)
        
        self.sequence_laser_horizontal = pygame.transform.rotate(self.sequence_laser, 90)
        
        #pressure plate
        self.pressure_plate = pygame.transform.scale(pygame.image.load(self.img_dir + "pressure_plate.png").convert(), (64, 64))
        self.pressure_plate.set_colorkey(BLACK)
        
        #lava tile
        self.lava_tile = pygame.transform.scale(pygame.image.load(self.img_dir + "lava_brick.png").convert(), (64, 64))
        self.lava_tile.set_colorkey(BLACK)
        
        #player masks (for dimmed environment)
        self.small_mask = pygame.transform.scale(pygame.image.load(self.img_dir + "small_outline.png").convert_alpha(), (64, 64))
        self.large_mask = pygame.transform.scale(pygame.image.load(self.img_dir + "large_outline.png").convert_alpha(), (192, 192))
         

         
        #logo
        logo = SpriteSheet(pygame.image.load(self.img_dir + "logo_spritesheet.png").convert(), (108, 30), 6)
        self.logo = []
        for row in range(7):
            img = logo.get_image(0, row, False)
            self.logo.append(img)
            
        #cursor
        self.cursor = pygame.transform.scale(pygame.image.load(self.img_dir + "cursor.png").convert(), (16, 16))
        self.cursor.set_colorkey(BLACK)
        
        #bridge
        self.bridge = pygame.transform.scale(pygame.image.load(self.img_dir + "bridge.png").convert(), (128, 32))
        self.bridge.set_colorkey(BLACK)
        
        #light ray
        self.light_ray = pygame.transform.scale(pygame.image.load(self.img_dir + "light_ray.png").convert_alpha(), (300, 640))
        
        #font
        self.font = pygame.font.Font(self.font_dir + 'dogica.ttf', 15)
        self.button_font = pygame.font.Font(self.font_dir + 'dogica.ttf', 40)
        self.warning_font = pygame.font.Font(self.font_dir + 'dogica.ttf', 10)
        
        #text list for level 4
        self.lvl_4_text = [
            (12, 4, "why are you here?"),
            (24, 22, "I see"),
            (32, 9, "it is clear now"),
            (44, 3, "you share the same fate as me"),
            (63, 3, "I know"),
            (50, 11, "you are trying to escape"),
            (53, 19, "there is no escape"),
            (54.5, 35, "this is your fate"),
            (45, 35, "give up"),
            (37.5, 15, "give in"),
            (31, 29, "death"),
            (6, 29, "is inevitable"),
            (2.75, 20, "I know"),
            (7, 9, "because I am YOU")
        ]
        
        #text list for level 7
        self.lvl_7_text = [
            (9, 4, "so this is the path you have chosen"),
            (22, 14, "die now"),
            (8, 14, "or suffer longer"),
            (8, 22, "I see you chose the latter"),
            (23, 30, "foolish"),
            (18, 36, "arrogant"),
            (27, 36, "must I repeat myself"),
            (36.75, 32, "there"),
            (37.5, 26, "is"),
            (37.5, 20, "no"),
            (36.5, 14, "escape"),
            (46, 8, "fine"),
            (58, 16, "have it your way"),
            (56, 26, "for it does not matter"),
            (53, 34, "you will see soon enough")
        ]
        
        self.lvl_11_text = [(14.5, 34, "die"),
                            (20, 26, "die"),
                            (27, 26, "DIE"),
                            (10, 18, "why must you defy your fate?"),
                            (10, 8, "I should have know better"),
                            (34, 8, "fine"),
                            (50, 16, "let us see how long you last"),
                            (55.5, 26, "when the world around you"),
                            (44, 34, "fades to black")]
        
        #text list for level 14
        self.lvl_14_text = [
            (61, 4, "impossible"),
            (57, 12, "you should have died"),
            (60, 20, "fine"),
            (58, 20, "you asked for this"),
            (51, 32, "if you want to change your fate"),
            (46, 32, "you'll have to beat me first")
        ]
        
        #text for epilogue
        self.end_text = [
            (18, 6, "maybe I was wrong"),
            (32, 14, "maybe this isn't your fate"),
            (48, 6, "your ability to persist"),
            (55, 22, "it takes some guts"),
            (29, 34, "I know one thing for certain now"),
            (6, 34, "the only person who can change your fate, is YOU")
        ]
        
        #dimmed background
        self.blur = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.blur.fill((0, 0, 0, 200))
        
        self.map_dict = {
            'tut' : Map(self.map_dir + "tut.txt"),
            '1' : Map(self.map_dir + "lvl_1.txt"),
            '2' : Map(self.map_dir + "lvl_2.txt"),
            '3' : Map(self.map_dir + "lvl_3.txt"),
            '4' : Map(self.map_dir + "lvl_4.txt"),
            '5' : Map(self.map_dir + "lvl_5.txt"),
            '6' : Map(self.map_dir + "lvl_6.txt"),
            '7' : Map(self.map_dir + "lvl_7.txt"),
            '8' : Map(self.map_dir + "lvl_8.txt"),
            '9' : Map(self.map_dir + "lvl_9.txt"),
            '10' : Map(self.map_dir + "lvl_10.txt"),
            '11' : Map(self.map_dir + "lvl_11.txt"),
            '12' : Map(self.map_dir + "lvl_12.txt"),
            '13' : Map(self.map_dir + "lvl_13.txt"),
            '14' : Map(self.map_dir + "lvl_14.txt"),
            '15' : Map(self.map_dir + "lvl_15.txt"),
            'end' : Map(self.map_dir + "end.txt")    
        }
        
        #load the initial map
        self.map = self.map_dict[self.current_level]

    def load_audio(self):
        #game music
        self.track_1 = "track_1.ogg"
        self.track_2 = "track_2.ogg"
        self.boss_music = "boss_music.ogg"
        
        #sfx
        self.sfx = {
            "death" : pygame.mixer.Sound(self.sfx_dir + "death.wav"),
            "laser" : pygame.mixer.Sound(self.sfx_dir + "laser_break.wav"),
            "grow": pygame.mixer.Sound(self.sfx_dir + "player_grow.wav"),
            "shrink" : pygame.mixer.Sound(self.sfx_dir + "player_shirnk.wav"),
            "invisible" : pygame.mixer.Sound(self.sfx_dir + "player_invisible.wav"),
            "select" : pygame.mixer.Sound(self.sfx_dir + "select.wav")
        }

    #method for creating new instance of objects
    def new(self):
        #create new groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.wall_lasers = pygame.sprite.Group()
        self.sensors = pygame.sprite.Group()
        self.slow_tiles = pygame.sprite.Group()
        self.boost_tiles = pygame.sprite.Group()
        self.red_lasers = pygame.sprite.Group()
        self.yellow_lasers = pygame.sprite.Group()
        self.green_lasers = pygame.sprite.Group()
        self.blue_lasers = pygame.sprite.Group()
        self.end_portals = pygame.sprite.Group()
        self.mine_group = pygame.sprite.Group()
        self.clock_group = pygame.sprite.Group()
        self.colors_group = pygame.sprite.Group()
        self.clock_visual_group = pygame.sprite.Group()
        self.dir_tiles = pygame.sprite.Group()
        self.pressure_plate_group = pygame.sprite.Group()
        self.order_1 = pygame.sprite.Group()
        self.order_2 = pygame.sprite.Group()
        self.order_3 = pygame.sprite.Group()
        self.order_4 = pygame.sprite.Group()
        self.snake_tiles = pygame.sprite.Group()
        self.outline = pygame.sprite.Group()
        self.torch_outline = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.button_text = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.game_cursor_group = pygame.sprite.Group()
        
        #cursor object
        Cursor(self)
        
        #text in the tutorial level
        if self.current_level == 'tut':
            Font(self, self.font, 14, 6, "hold WASD to move")
            Font(self, self.font, 30, 13, "hold l-shift to open the color panel")
            Font(self, self.font, 30, 14, "press space to cycle between colors")
            Font(self, self.font, 48, 3, "lasers will break upon impact")
            Font(self, self.font, 48, 4, "if you are the same color")
            Font(self, self.font, 45, 23, "hold space to use an ability")
            Font(self, self.font, 45, 24, "red's ability is to boost")
            Font(self, self.font, 21, 35, "yellow's ability")
            Font(self, self.font, 21, 36, "is to slow")
            Font(self, self.font, 6, 27, "blue's ability")
            Font(self, self.font, 6, 28, "makes you invisible")
            Font(self, self.font, 12, 21, "green's ability")
            Font(self, self.font, 12, 22, "makes you small")
        
        #text in level 1
        elif self.current_level == '1':
            Font(self, self.font, 7, 36.75, "This is a dead end, way to go!")
            Font(self, self.font, 53, 35, "starting from the next level")
            Font(self, self.font, 53, 36, "each level will be timed!")
            
        #text in level 5
        elif self.current_level == '5':
            Font(self, self.font, 10, 2.75, "travel in the same direction")
            Font(self, self.font, 10, 3.75, "as the arrow to pass it")
            Font(self, self.font, 10, 4.75, "(You can be any color/form)")
            
        #text in level 6
        elif self.current_level == '6':
            Font(self, self.font, 15.25, 4, "red")
            Font(self, self.font, 19.5, 4, "or")
            Font(self, self.font, 23, 4, "blue")
        
        #snake tiles
        if self.current_level == '15':
            self.current_time = pygame.time.get_ticks()
            
            for i, (col, row) in enumerate(self.snake_path):      
                Snake_Tile(self, col, row, offset = self.current_time + self.delay + i * self.wave_speed)
                
        #loop through the map data
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "0":
                    #player sprite
                    self.player = Player(self, col, row)
                    
                    if self.current_level in self.dim_lvls:
                        #light mask
                        self.mask = Outline(self, col, row)
                    
                    if self.current_level not in self.white_lvls:
                        #color panel
                        Colors(self)
                        Small_Ball_Outline(self)
                        
                elif tile == "1":
                    #topleft outside corner
                    Tiles(self, col, row, 0)
                    
                elif tile == "2":
                    #floor
                    Tiles(self, col, row, 1)
                    
                elif tile == "3":
                    #topright outside corner
                    Tiles(self, col, row, 2)
                    
                elif tile == "4":
                    #floor and topleft inside corner
                    Tiles(self, col, row, 3)
                    
                elif tile == "5":
                    #floor and topright inside corner
                    Tiles(self, col, row, 4)
                    
                elif tile == "6":
                    #right wall
                    Tiles(self, col, row, 5)
                    
                elif tile == "7":
                    #background griebling
                    Tiles(self, col, row, 6)
                    
                elif tile == "8":
                    #left wall
                    Tiles(self, col, row, 7)
                    
                elif tile == "9":
                    #ceiling and bottom left inside corner
                    Tiles(self, col, row, 8)
                    
                elif tile == "a":
                    #ceiling and bottom right inside corner
                    Tiles(self, col, row, 9)
                    
                elif tile == "b":
                    #bottom left outside corner
                    Tiles(self, col, row, 10)
                
                elif tile == "c":
                    #ceiling
                    Tiles(self, col, row, 11)
                    
                elif tile == "d":
                    #botom right outside corner
                    Tiles(self, col, row, 12)
                    
                elif tile == "e":
                    #topleft inside corner
                    Tiles(self, col, row, 13)
                    
                elif tile == "f":
                    #topright inside corner
                    Tiles(self, col, row, 14)
                    
                elif tile == "g":
                    #triple corner - right wall
                    Tiles(self, col, row, 15)
                    
                elif tile == "h":
                    #triple corner - left wall 
                    Tiles(self, col, row, 16)
                    
                elif tile == "i":
                    #floor and ceiling
                    Tiles(self, col, row, 17)
                    
                elif tile == "j":
                    #bottom left inside corner
                    Tiles(self, col, row, 18)
                    
                elif tile == "k":
                    #bottom right inside corner
                    Tiles(self, col, row, 19)
                    
                elif tile == "l":
                    #griebling low 
                    Tiles(self, col, row, 20)
                    
                elif tile == "m":
                    #griebling high
                    Tiles(self, col, row, 21)
                    
                elif tile == "n":
                    #griebling
                    Tiles(self, col, row, 22)
                    
                elif tile == "o":
                    #double inside corner - left
                    Tiles(self, col, row, 23)
                    
                elif tile == "p":
                    #double inside corner - right
                    Tiles(self, col, row, 24)
                    
                elif tile == "q":
                    #left wall laser and background griebling                    
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'left')
                                   
                elif tile == 'r':
                    #right wall laser and background griebling                   
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'right')
                                        
                elif tile == 's':
                    #ceiling laser and background griebling                   
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'ceil')
                                        
                elif tile == 't':
                    #floor laser and background griebling                    
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'floor')
                    
                elif tile == 'u':
                    #bottom right corner lasers and background griebling                   
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'floor')
                    Wall_laser(self, col, row, 'right')
                    
                elif tile == 'v':
                    #bottom left corner lasers and background griebling                    
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'floor')
                    Wall_laser(self, col, row, 'left')
                    
                elif tile == 'w':
                    #top right corner lasers and background griebling                    
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, row, 'right')
                    
                elif tile == 'x':
                    #top left corner lasers and background griebling
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, row, 'left')
                    
                elif tile == 'y':
                    #floor and ceiling lasers and background griebling
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'floor')
                    Wall_laser(self, col, row, 'ceil')
                    
                elif tile == 'z':
                    #left and right wall lasers and background griebling
                    Tiles(self, col, row, 6)
                    Wall_laser(self, col, row, 'left')
                    Wall_laser(self, col, row, 'right')
                    
                elif tile == 'A':
                    #sensor 
                    Tiles(self, col, row, 6)
                    Tiles(self, (col + 2), row, 6)
                    Tiles(self, col, (row + 2), 6)
                    Tiles(self, (col + 2), (row + 2), 6)
                    Sensor(self, col, row)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, (col + 2), row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    Wall_laser(self, (col + 2), (row + 2), 'floor')
                    
                elif tile == 'B':
                    #boost tiles
                    Boost_Tile(self, col, row)
                    Boost_Tile(self, col, (row + 2))
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'C':
                    #slow tiles
                    Slow_Tile(self, col, row)
                    Slow_Tile(self, col, (row + 2))
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'D':
                    #red vertical laser
                    Colored_Laser(self, col, row, 'red', 'ver')
                    Tiles(self, col, row, 6)
                    Tiles(self, col, (row + 2), 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'E':
                    #red horizontal laser
                    Colored_Laser(self, col, row, 'red', 'hor')
                    Tiles(self, col, row, 6)
                    Tiles(self, (col + 2), row, 6)
                    Wall_laser(self, col, row, 'left')
                    Wall_laser(self, (col + 2), row, 'right')
                    
                elif tile == 'F':
                    #yellow vertical laser
                    Colored_Laser(self, col, row, 'yellow', 'ver')
                    Tiles(self, col, row, 6)
                    Tiles(self, col, (row + 2), 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'G':
                    #yellow horizontal laser
                    Colored_Laser(self, col, row, 'yellow', 'hor')
                    Tiles(self, col, row, 6)
                    Tiles(self, (col + 2), row, 6)
                    Wall_laser(self, col, row, 'left')
                    Wall_laser(self, (col + 2), row, 'right')
                    
                elif tile == 'H':
                    #green vertical laser
                    Colored_Laser(self, col, row, 'green', 'ver')
                    Tiles(self, col, row, 6)
                    Tiles(self, col, (row + 2), 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'I':
                    #green horizontal laser
                    Colored_Laser(self, col, row, 'green', 'hor')
                    Tiles(self, col, row, 6)
                    Tiles(self, (col + 2), row, 6)
                    Wall_laser(self, col, row, 'left')
                    Wall_laser(self, (col + 2), row, 'right')
                
                elif tile == 'J':
                    #blue vertical laser
                    Colored_Laser(self, col, row, 'blue', 'ver')
                    Tiles(self, col, row, 6)
                    Tiles(self, col, (row + 2), 6)
                    Wall_laser(self, col, row, 'ceil')
                    Wall_laser(self, col, (row + 2), 'floor')
                    
                elif tile == 'K':
                    #blue horizontal laser
                    Colored_Laser(self, col, row, 'blue', 'hor')
                    Tiles(self, col, row, 6)
                    Tiles(self, (col + 2), row, 6)
                    Wall_laser(self, col, row, 'left')
                    Wall_laser(self, (col + 2), row, 'right')
                    
                elif tile == 'L':
                    #start portal
                    if self.current_level == '2':
                        Start_Portal(self, col + 1, row, False)
                    else:
                        Start_Portal(self, col, row, False)
                
                elif tile == 'M':
                    #end portal
                    if self.current_level == '3':
                        End_Portal(self, col, row, "flipped")
                    
                    elif self.current_level == '15':
                        End_Portal(self, col, row, "mono")
                        
                    else:
                        End_Portal(self, col, row, "normal")
                    
                elif tile == 'N':
                    if self.current_level == '8':
                        #red torch
                        Torch(self, col, row, 'red')
                        
                    elif self.current_level == '9':
                        Torch(self, col, row, 'teal')
                        
                    else:
                        #mines
                        Tiles(self, col, row, 6)
                        Tiles(self, (col + 2), row, 6)
                        Tiles(self, col, (row + 2), 6)
                        Tiles(self, (col + 2), (row + 2), 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, (col + 2), row, 'ceil')
                        Wall_laser(self, col, (row + 2), 'floor')
                        Wall_laser(self, (col + 2), (row + 2), 'floor')
                        Mine(self, col + 0.75, row + 1)
                        Mine(self, col + 0.75, row + 2.5)
                        Mine(self, col + 2.75, row + 1.75)
                    
                elif tile == 'O':
                    if self.current_level == '8':
                        #yellow torch
                        Torch(self, col, row, 'yellow')
                    
                    elif self.current_level == '9':
                        Torch(self, col, row, 'dark_blue')
    
                    elif self.current_level == '15':
                        self.orange_entity = Orange_Entity(self, col, row)
                        
                    else:
                        #clock powerup
                        Tiles(self, col, row, 6)
                        Clock_Visual(self, col + 0.5, row + 0.5)
                        Clock(self, col + 0.5, row + 0.5)
                    
                elif tile == 'P':
                    if self.current_level in self.dir_tile_lvls:
                        #right direction tile
                        Tiles(self, col, row, 6)
                        Tiles(self, col, row + 2, 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, (row + 2), 'floor')
                        Direction_Tile(self, col, row, "right")
                        
                    elif self.current_level == '9':
                        Torch(self, col, row, 'light_yellow')
                        
                    else:
                        #triple inside corner wall lasers
                        Tiles(self, col, row, 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, row, 'floor')
                        Wall_laser(self, col, row, 'left')
                    
                elif tile == 'Q':
                    if self.current_level in self.dir_tile_lvls:
                        #left direction tile
                        Tiles(self, col, row, 6)
                        Tiles(self, col, row + 2, 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, (row + 2), 'floor')
                        Direction_Tile(self, col, row, "left")
                    
                    elif self.current_level == '9':
                        Torch_Combinations(self, col, row)
                    
                    else:
                        #triple inside corner wall lasers
                        Tiles(self, col, row, 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, row, 'floor')
                        Wall_laser(self, col, row, 'right')
                    
                elif tile == 'R':
                    if self.current_level in self.white_lvls:
                        #entity
                        self.entity = Entity(self, col, row)
                        
                    elif self.current_level == '8':
                        #green torch
                        Torch(self, col, row, 'green')
                        
                    elif self.current_level == '9':
                        Torch(self, col, row, 'orange')
                        
                    else:
                        #up direction tile
                        Tiles(self, col, row, 6)
                        Tiles(self, col + 2, row, 6)
                        Wall_laser(self, col, row, 'left')
                        Wall_laser(self, col + 2, row, 'right')
                        Direction_Tile(self, col, row, "up")
                        
                elif tile == "S":
                    if self.current_level == '8':
                        #blue torch
                        Torch(self, col, row, 'blue')
                    
                    elif self.current_level == '9':
                        Torch(self, col, row, 'magenta')
                        
                    else:
                        #down direction tile
                        Tiles(self, col, row, 6)
                        Tiles(self, col + 2, row, 6)
                        Wall_laser(self, col, row, 'left')
                        Wall_laser(self, col + 2, row, 'right')
                        Direction_Tile(self, col, row, "down")
                
                elif tile == "T":
                    if self.current_level == '14':
                        if self.death_counter >= 3:
                            self.dir = "right"
                        else:
                            self.dir = "left"
                        
                        #direction tile for level 10
                        Tiles(self, col, row, 6)
                        Tiles(self, col, row + 2, 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, (row + 2), 'floor')
                        Direction_Tile(self, col, row, self.dir)
                        
                    else:
                        #order 1 sequence tile
                        Sequence_Tile(self, col, row, 1)
                        Wall_laser(self, col, row, 'floor')
                
                elif tile == 'U':
                    if self.current_level == '14':
                        if self.death_counter == 1:
                            #white entity
                            White_Entity(self, col, row)
                            Font(self, self.font, col + 3, row + 1, "see, I told you")
                        
                        if self.death_counter == 2:
                            #white entity
                            White_Entity(self, col, row)
                            Font(self, self.font, col + 3, row + 1, "no escape")
                            
                        if self.death_counter >= 3:
                            #white entity
                            self.white_entity = White_Entity(self, col + 43, row - 10)
                            
                    else:
                        #order 2 sequence tile
                        Sequence_Tile(self, col, row, 2)
                        Wall_laser(self, col, row, 'floor')
                            
                elif tile == 'V':
                    #order 3 sequence tile
                    Sequence_Tile(self, col, row, 3)
                    Wall_laser(self, col, row, 'floor')
                
                elif tile == 'W':
                    #order 4 sequence tile
                    Sequence_Tile(self, col, row, 4)
                    Wall_laser(self, col, row, 'floor')
                    
                elif tile == 'X':
                    if self.current_level == '12' or self.current_level == '13':
                        #horizontal
                        Sequence_Laser(self, col, row, 'horizontal')
                        Tiles(self, col, row, 6)
                        Tiles(self, col + 2, row, 6)
                        Wall_laser(self, col, row, 'left')
                        Wall_laser(self, col + 2, row, 'right')
                        
                    else:
                        #vertical sequence laser
                        Sequence_Laser(self, col, row, 'vertical')
                        Tiles(self, col, row, 6)
                        Tiles(self, col, (row + 2), 6)
                        Wall_laser(self, col, row, 'ceil')
                        Wall_laser(self, col, (row + 2), 'floor')
                        
                elif tile == 'Y':
                    Pressure_Plate(self, col, row)
                    
                elif tile == 'Z':
                    self.color_torch = Color_Torch(self, col, row)
                    
                    if self.current_level == '12' or self.current_level == '13':
                        Torch_Outline(self, col, row)
                        
                elif tile == '!':
                    Mouse_Block(self, col, row)
                        
        Button_Font(self, self.button_font, START_BUTTON, 420, 170, "Resume")
        Button_Font(self, self.button_font, START_BUTTON_SHADOW, 417, 167, "Resume")
        
        Button_Font(self, self.button_font, SETTINGS_BUTTON, 420, 323, "Main Menu")
        Button_Font(self, self.button_font, SETTINGS_BUTTON_SHADOW, 417, 320, "Main Menu")
                              
        self.return_game_button = Return_To_Game(self, 400, 150)
        self.return_menu_button = Return_To_Menu(self, 400, 300)
        
        self.return_game_button_bkgd = pygame.Surface((self.return_game_button.image.get_width() + 16, self.return_game_button.image.get_height() + 16))
        self.return_menu_button_bkgd = pygame.Surface((self.return_menu_button.image.get_width() + 16, self.return_menu_button.image.get_height() + 16))
        
        #create camera
        self.camera = Camera(self.map.width, self.map.height)
        
        self.game_cursor = Game_Cursor(self)
        
        #entity text
        if self.current_level == '4':
            self.text = Font(self, self.font, self.lvl_4_text[self.entity.position_tracker][0], self.lvl_4_text[self.entity.position_tracker][1], self.lvl_4_text[self.entity.position_tracker][2])
            
        if self.current_level == '7':
            self.text = Font(self, self.font, self.lvl_7_text[self.entity.position_tracker][0], self.lvl_7_text[self.entity.position_tracker][1], self.lvl_7_text[self.entity.position_tracker][2])
            
        if self.current_level == '11':
            self.text = Font(self, self.font, self.lvl_11_text[self.entity.position_tracker][0], self.lvl_11_text[self.entity.position_tracker][1], self.lvl_11_text[self.entity.position_tracker][2])    
            
        if self.current_level == '14' and self.death_counter >= 3:
            self.text = Font(self, self.font, self.lvl_14_text[self.white_entity.position_tracker][0], self.lvl_14_text[self.white_entity.position_tracker][1], self.lvl_14_text[self.white_entity.position_tracker][2])
        
        if self.current_level == '15':
            self.text = Font(self, self.font, 6, 8, "")
            
        if self.current_level == 'end':
            self.text = Font(self, self.font, self.end_text[self.entity.position_tracker][0], self.end_text[self.entity.position_tracker][1], self.end_text[self.entity.position_tracker][2])
            
    #method for updating the game
    def update(self):
        #update the sprite group and camera
        self.all_sprites.update()
        self.colors_group.update()
        self.background_particles.update()
        self.game_cursor_group.update()
        
        if self.pause_on:
            self.buttons.update()
            self.button_text.update()
            self.cursor_group.update()
        
        if self.current_level in self.dim_lvls:
            self.outline.update()
            self.camera.update(self.mask)
            
        self.camera.update(self.player)
        
        #spawn particles
        self.spawn_timer += 1
        if self.spawn_timer >= 3:
            self.spawn_timer = 0
            if self.player.dir_state != 'idle':
                if self.player.ball_speed == 9:
                    Particle(self, self.player.rect.centerx, self.player.rect.centery, LIGHT_RED)
                    
                elif self.player.ball_speed == 3:
                    Particle(self, self.player.rect.centerx, self.player.rect.centery, YELLOW)
                    
                elif self.player.small_state:
                    Particle(self, self.player.rect.centerx, self.player.rect.centery, GREEN, size = (4, 4))
                    
                else:
                    Particle(self, self.player.rect.centerx, self.player.rect.centery, SLATE_GREY)
                
            if self.current_level not in self.white_lvls:
                Background_Particle(self)
        
        #if the current level is the epilogue
        if self.current_level == 'end':
            self.text.change_text(self.end_text[self.entity.position_tracker][0], self.end_text[self.entity.position_tracker][1], self.end_text[self.entity.position_tracker][2])
            
            if self.entity.within(self.player.rect.centerx, self.player.rect.centery):
                self.entity.position_tracker += 1
                
            if self.entity.position_tracker >= len(self.entity.end_position_list):
                if pygame.sprite.collide_rect(self.player, self.entity):
                    self.playing = False
                    self.main_menu()
                    
        #if the current level is 15 (final level)        
        if self.current_level == '15':
            #for entity in level 15
            if self.orange_entity.show_text:
                self.text.change_text(6, 8, "there is no escape this time")
            elif self.orange_entity.change_text:
                self.text.change_text(6, 8, "I will make sure of it")
            else:
                self.text.change_text(6, 8, "")
                
            #lava tile collision detection
            hits = pygame.sprite.spritecollide(self.player, self.snake_tiles, False)
            for hit in hits:
                if hit.active:
                    self.playing = False    
                    
        #for moving entity in level 14
        if self.current_level == '14' and self.death_counter >= 3:
            self.text.change_text(self.lvl_14_text[self.white_entity.position_tracker][0], self.lvl_14_text[self.white_entity.position_tracker][1], self.lvl_14_text[self.white_entity.position_tracker][2])
            
            if self.white_entity.within(self.player.rect.centerx, self.player.rect.centery):
                self.white_entity.position_tracker += 1
                
            if self.white_entity.position_tracker >= len(self.white_entity.positions):
                if pygame.sprite.collide_rect(self.player, self.white_entity):
                    self.playing = False
                    self.current_level = '15'
                    self.save_level(self.current_level)
                    self.can_move = False
                    self.map = Map(self.map_dir + 'lvl_15.txt')
                    self.final_level_music()
                    
        #for moving the entity in level 11
        if self.current_level == '11':
            self.text.change_text(self.lvl_11_text[self.entity.position_tracker][0], self.lvl_11_text[self.entity.position_tracker][1], self.lvl_11_text[self.entity.position_tracker][2])
            
            if self.entity.within(self.player.rect.centerx, self.player.rect.centery):
                self.entity.position_tracker += 1
                
            if self.entity.position_tracker >= len(self.entity.lvl_11_position_list):
                if pygame.sprite.collide_rect(self.player, self.entity):
                    self.playing = False
                    self.current_level = '12'
                    self.save_level(self.current_level)
                    self.count_down = self.reset_timer[self.current_level]
                    self.map = Map(self.map_dir + 'lvl_12.txt') 
                    self.switch_tracks()
                    
        #for moving the entity in level 7
        if self.current_level == '7':
            self.text.change_text(self.lvl_7_text[self.entity.position_tracker][0], self.lvl_7_text[self.entity.position_tracker][1], self.lvl_7_text[self.entity.position_tracker][2])
            
            if self.entity.within(self.player.rect.centerx, self.player.rect.centery):
                self.entity.position_tracker += 1
                
            if self.entity.position_tracker >= len(self.entity.lvl_7_position_list):
                if pygame.sprite.collide_rect(self.player, self.entity):
                    self.playing = False
                    self.current_level = '8'
                    self.save_level(self.current_level)
                    self.map = Map(self.map_dir + 'lvl_8.txt')
                    self.switch_tracks()
                    
        #for moving the entity in level 4
        if self.current_level == '4':
            self.text.change_text(self.lvl_4_text[self.entity.position_tracker][0], self.lvl_4_text[self.entity.position_tracker][1], self.lvl_4_text[self.entity.position_tracker][2])
            
            if self.entity.within(self.player.rect.centerx, self.player.rect.centery):
                self.entity.position_tracker += 1
                
            if self.entity.position_tracker >= len(self.entity.lvl_4_position_list):
                if pygame.sprite.collide_rect(self.player, self.entity):
                    self.playing = False
                    self.current_level = '5'
                    self.save_level(self.current_level)
                    self.count_down = self.reset_timer[self.current_level]
                    self.map = Map(self.map_dir + 'lvl_5.txt')
                    self.switch_tracks()
                
        #laser collision detection
        hits = pygame.sprite.spritecollide(self.player, self.wall_lasers, False)
        if hits:
            self.playing = False
                
        #end portal collision  
        hits = pygame.sprite.spritecollide(self.player, self.end_portals, False)
        if hits:
            if self.current_level == 'tut':
                self.playing = False
                self.current_level = '1'
                self.map = Map(self.map_dir + "lvl_1.txt")
                
            elif self.current_level == '1':
                self.playing = False
                self.current_level = '2'
                self.map = Map(self.map_dir + 'lvl_2.txt')
                
            elif self.current_level == '2':
                self.playing = False
                self.current_level = '3'
                self.map = Map(self.map_dir + 'lvl_3.txt')
            
            elif self.current_level == '3':
                self.playing = False
                self.current_level = '4'
                self.map = Map(self.map_dir + 'lvl_4.txt')
                
            elif self.current_level == '5':
                self.playing = False
                self.current_level = '6'
                self.map = Map(self.map_dir + 'lvl_6.txt')
                
            elif self.current_level == '6':
                self.playing = False
                self.current_level = '7'
                self.map = Map(self.map_dir + 'lvl_7.txt')
                
            elif self.current_level == '8':
                self.playing = False
                self.current_level = '9'
                self.map = Map(self.map_dir + 'lvl_9.txt')

            elif self.current_level == '9':
                self.playing = False
                self.current_level = '10'
                self.map = Map(self.map_dir + 'lvl_10.txt')                    
            
            elif self.current_level == '10':
                self.playing = False
                self.current_level = '11'
                self.map = Map(self.map_dir + 'lvl_11.txt')
                
            elif self.current_level == '12':
                self.playing = False
                self.current_level = '13'
                self.map = Map(self.map_dir + 'lvl_13.txt')
                
            elif self.current_level == '13':
                self.playing = False
                self.current_level = '14'
                self.alpha_lvl = 200
                self.map = Map(self.map_dir + 'lvl_14.txt')
                
            elif self.current_level == '15':
                self.playing = False
                self.current_level = 'end'
                self.map = Map(self.map_dir + 'end.txt')                
        
            self.count_down = self.reset_timer[self.current_level]
            self.save_level(self.current_level)
            self.switch_tracks()
                
        #mine collision
        hits = pygame.sprite.spritecollide(self.player, self.mine_group, False)
        if hits:
            self.playing = False
            
        #clock collision
        hits = pygame.sprite.spritecollide(self.player, self.clock_group, True)
        if hits:
            self.count_down += 30
            self.sfx["select"].play()
            
        hits = pygame.sprite.spritecollide(self.player, self.clock_visual_group, False)
        for hit in hits:
            hit.is_collected = True
           
        #direction tile collisions 
        for tile in self.dir_tiles:
            if pygame.sprite.collide_rect(self.player, tile):
                tile.set_opacity(100)
                
                if tile.dir == "right":
                    if self.player.dir_state != 'right': 
                        self.playing = False

                elif tile.dir == "left":
                    if self.player.dir_state != 'left':
                        self.playing = False
        
                elif tile.dir == "up":
                    if self.player.dir_state != 'up': 
                        self.playing = False

                elif tile.dir == "down":
                    if self.player.dir_state != 'down':
                        self.playing = False
             
            else:
                tile.set_opacity(255)
                
        #sequence tile collisions
        if not self.collide_1:
            hits = pygame.sprite.spritecollide(self.player, self.order_1, False)
            if hits:
                if self.sequence == 0:
                    self.sequence = 1
                else:
                    self.sequence = 0
                      
                self.collide_1 = True
                
        if not self.collide_2:   
            hits = pygame.sprite.spritecollide(self.player, self.order_2, False)
            if hits:
                if self.sequence == 1:
                    self.sequence = 2
                else:
                    self.sequence = 0
                    
                self.collide_2 = True
        
        if not self.collide_3:
            hits = pygame.sprite.spritecollide(self.player, self.order_3, False)
            if hits:
                if self.sequence == 2:
                    self.sequence = 3     
                else:
                    self.sequence = 0
                    
                self.collide_3 = True
        
        if not self.collide_4:  
            hits = pygame.sprite.spritecollide(self.player, self.order_4, False)
            if hits:
                if self.sequence == 3:
                    self.sequence = 4
                else:
                    self.sequence = 0
            
                self.collide_4 = True
                
        #if self.playing is false
        if not self.playing:
            if self.current_level == '14':
                self.death_counter += 1 
            
            if self.current_level == '15':
                self.can_move = False
                
            #play death sfx
            self.sfx["death"].play()
            
            #reset timer and sequence for puzzle
            self.count_down = self.reset_timer[self.current_level]
            self.reset()
                   
    #method for handing input
    def events(self):
        for event in pygame.event.get():
            #exit the game 
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    #if the player is inside the color panel
                    if self.player.change_color_menu:
                        if self.player.color_selector == len(self.player.color_list) - 1:
                            self.player.color_selector = 2
                            
                        else:
                            self.player.color_selector += 1
                            
                if event.key == pygame.K_ESCAPE:
                    if self.pause_off:
                        self.pause_off = False
                        self.pause_on = True
                        
                    elif self.pause_on:
                        self.pause_on = False
                        self.pause_off = True
                    
            #decrement the count down timer
            if self.current_level not in self.no_timer and self.pause_off:
                if event.type == self.timer:
                    if self.count_down >= 0:
                        self.count_down -= 1
                                
    #method that will control the play state                
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()
            
    #method that will draw the sprites to the screen
    def draw(self):
        #fill the screen with a color
        if self.current_level in self.white_lvls:
            self.screen.fill(WHITE)
            
        else:
            self.screen.fill(DARK_GREY)

        #draw the sprites to the screen
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
             
        #draw the color panel to the screen
        if self.player.change_color_menu:
            for sprite in self.colors_group:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.background_particles.draw(self.screen)
                
        #dimmer environment
        if self.current_level in self.dim_lvls:
            darkness = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, self.alpha_lvl))
            
            if self.current_level == '12' or self.current_level == '13':
                if self.alpha_lvl <= 200:
                    self.alpha_lvl += 2
                    
                if self.color_torch.collide:
                    for sprite in self.torch_outline:
                        darkness.blit(sprite.image, self.camera.apply(sprite), special_flags=pygame.BLEND_RGBA_SUB)    
                                           
            elif self.current_level == '14':
                if self.alpha_lvl >= 0:
                    self.alpha_lvl -= 2
                
            if self.alpha_lvl < 0:
                self.alpha_lvl = 0
                
            for sprite in self.outline:
                darkness.blit(sprite.image, self.camera.apply(sprite), special_flags=pygame.BLEND_RGBA_SUB)
                
            self.screen.blit(darkness, (0, 0))
            
        #draw the count down timer
        if self.current_level not in self.no_timer:
            pygame.draw.rect(self.screen, BLACK, (self.screen.get_width() - 80, 25, 80, 35))
            
            #reset timer when it reaches 0
            if self.count_down < 0:
                self.playing = False
                self.count_down = self.reset_timer[self.current_level]
                
            if self.count_down >= 0:
                display_seconds = self.count_down % 60
                display_minutes = int(self.count_down / 60) % 60
                
            time = self.font.render(f'{display_minutes}:{display_seconds:02}', False, WHITE)
            self.screen.blit(time, (self.screen.get_width() - 70, 35))
        
        if self.pause_on:
            self.screen.blit(self.blur, (0, 0))
            
            if self.return_game_button.return_hover:
                self.return_game_button_bkgd.fill(LIGHT_GREY)
            else:
                self.return_game_button_bkgd.fill(SLATE_GREY)
                
            if self.return_menu_button.menu_hover:
                self.return_menu_button_bkgd.fill(LIGHT_GREY)
            else:
                self.return_menu_button_bkgd.fill(SLATE_GREY)
                
            self.screen.blit(self.return_game_button_bkgd, (self.return_game_button.rect.x - 8, self.return_game_button.rect.y - 8))
            self.screen.blit(self.return_menu_button_bkgd, (self.return_menu_button.rect.x - 8, self.return_menu_button.rect.y - 8))    
            
            self.buttons.draw(self.screen)
            self.button_text.draw(self.screen)
            
            self.cursor_group.draw(self.screen)
            
        for sprite in self.game_cursor_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        #update the display 
        pygame.display.flip()
        
    def main_menu(self):
        self.menu_loop = True
        self.snake_sequence = -5
        self.player_particles = 0
        self.menu_map = Map(self.map_dir + "main_menu.txt")
        
        self.switch_tracks()
        
        self.menu_snake_path = [
            (0,14),(0,16),(2,14),(2,16),(4,14),(4,16),
            (6,14),(6,16),(8,14),(8,16),(10,14),(10,16),
            (12,14),(12,16),(14,14),(14,16),(16,14),(16,16),
            (18,14),(18,16),(20,14),(20,16),(22,14),(22,16),
            (24,14),(24,16),(26,14),(26,16),(28,14),(28,16),
            (30,14),(30,16),(32,14),(32,16),(34,14),(34,16),
            (36,14),(36,16),(38,14),(38,16)
        ]
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.Group()
        self.button_text = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
        
        #cursor
        Cursor(self)
        
        #button text
        Button_Font(self, self.button_font, START_BUTTON, 850, 110, "Start")
        Button_Font(self, self.button_font, START_BUTTON_SHADOW, 847, 107, "Start")
        
        Button_Font(self, self.button_font, SETTINGS_BUTTON, 930, 235, "Settings")
        Button_Font(self, self.button_font, SETTINGS_BUTTON_SHADOW, 927, 232, "Settings")
        
        Button_Font(self, self.button_font, CREDITS_BUTTON, 960, 365, "Credits")
        Button_Font(self, self.button_font, CREDITS_BUTTON_SHADOW, 957, 362, "Credits")
        
        Button_Font(self, self.button_font, EXIT_BUTTON, 1025, 495, "Exit")
        Button_Font(self, self.button_font, EXIT_BUTTON_SHADOW, 1022, 492, "Exit")
        
        Font(self, self.font, 36.5, 0.5, "v.1.0.0")
    
        for i, (col, row) in enumerate(self.menu_snake_path):      
            Menu_Snake_Tile(self, col, row, i)
    
        for row, tiles in enumerate(self.menu_map.data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                    self.menu_player = Menu_Player(self, col, row)
                    
                elif tile == '1':
                    #background griebling
                    Menu_Tile(self, col, row) 
                    
                elif tile == '2':
                    Logo(self, col, row)
                    
                elif tile == '3':
                    self.start_button = Start_Button(self, col, row - 0.3)
                    
                elif tile == '4':
                    self.setting_button = Setting_Button(self, col, row - 0.3)
                    
                elif tile == '5':
                    self.credit_button = Credit_Button(self, col, row - 0.3)
                    
                elif tile == '6':
                    self.exit_button = Exit_Button(self, col, row - 0.3)
                   
        #buttons 
        self.start_button_bkgd = pygame.Surface((self.start_button.image.get_width() + 8, self.start_button.image.get_height() + 16))
        self.setting_button_bkgd = pygame.Surface((self.setting_button.image.get_width() + 8, self.setting_button.image.get_height() + 16))
        self.credit_button_bkgd = pygame.Surface((self.credit_button.image.get_width() + 8, self.credit_button.image.get_height() + 16))
        self.exit_button_bkgd = pygame.Surface((self.exit_button.image.get_width() + 8, self.exit_button.image.get_height() + 16))
        
        while self.menu_loop:
            self.clock.tick(FPS)
            self.screen.fill(DARKER_GREY)
            
            #start button background
            if self.start_button.start_hover:
                self.start_button_bkgd.fill(LIGHT_GREY)
            else:
                self.start_button_bkgd.fill(SLATE_GREY)
                
            if self.setting_button.setting_hover:
                self.setting_button_bkgd.fill(LIGHT_GREY)
            else:
                self.setting_button_bkgd.fill(SLATE_GREY)
                
            if self.credit_button.credit_hover:
                self.credit_button_bkgd.fill(LIGHT_GREY)
            else:
                self.credit_button_bkgd.fill(SLATE_GREY)
                
            if self.exit_button.exit_hover:
                self.exit_button_bkgd.fill(LIGHT_GREY)
            else:
                self.exit_button_bkgd.fill(SLATE_GREY)
                
            self.all_sprites.draw(self.screen)
            
            self.screen.blit(self.start_button_bkgd, (self.start_button.rect.x - 8, self.start_button.rect.y - 8))
            self.screen.blit(self.setting_button_bkgd, (self.setting_button.rect.x - 8, self.setting_button.rect.y - 8))
            self.screen.blit(self.credit_button_bkgd, (self.credit_button.rect.x - 8, self.credit_button.rect.y - 8))
            self.screen.blit(self.exit_button_bkgd, (self.exit_button.rect.x - 8, self.exit_button.rect.y - 8))
            
            self.buttons.draw(self.screen)
            self.button_text.draw(self.screen)
            self.cursor_group.draw(self.screen)
            self.background_particles.draw(self.screen)
    
            #update
            self.all_sprites.update()
            self.cursor_group.update()
            self.buttons.update()
            self.background_particles.update()
            
            self.snake_sequence += 0.15
            if self.snake_sequence >= len(self.menu_snake_path):
                self.snake_sequence = - 5
                self.menu_player.reset = True
                
            #spawn particles
            self.spawn_timer += 1
            if self.spawn_timer >= 10:
                self.spawn_timer = 0   
                Background_Particle(self)
                
            self.player_particles += 1
            if self.player_particles >= 3:
                self.player_particles = 0
                Particle(self, self.menu_player.rect.centerx, self.menu_player.rect.centery, SLATE_GREY)
                
            pygame.display.flip()
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    self.running = False
                    
    def load_level_menu(self):
        self.menu_loop = True
        self.map = Map(self.map_dir + "level_menu.txt")
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.Group()
        self.button_text = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
        self.saved_level = self.load_level()
        
        #reset death counter
        if self.saved_level == '14':
            self.death_counter = -1
            self.alpha_lvl = 200
            
        elif self.saved_level == '12':
            self.alpha_lvl = 0
        
        elif self.saved_level == '13':
            self.alpha_lvl = 200
            
        elif self.saved_level == '15':
            self.can_move = False
            
        #cursor
        Cursor(self)
        
        #button text
        Button_Font(self, self.button_font, START_BUTTON, 40, 110, "Resume")
        Button_Font(self, self.button_font, START_BUTTON_SHADOW, 37, 107, "Resume")
        
        if self.saved_level != 'tut':
            Button_Font(self, self.warning_font, WHITE, 290, 120, f"Current Level:{self.saved_level}")
        
        Button_Font(self, self.button_font, SETTINGS_BUTTON, 40, 233, "Start new")
        Button_Font(self, self.button_font, SETTINGS_BUTTON_SHADOW, 37, 231, "Start new")
        
        Button_Font(self, self.warning_font, RED, 40, 277, "(this will erase your previous save)")
        
        Button_Font(self, self.button_font, CREDITS_BUTTON, 40, 365, "Back")
        Button_Font(self, self.button_font, CREDITS_BUTTON_SHADOW, 37, 362, "Back")
        
        Font(self, self.font, 36.5, 0.5, "v.1.0.0")
    
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #background griebling
                    Menu_Tile(self, col, row) 
                    
                elif tile == '2':
                    self.resume_button = Resume_Button(self, col, row - 0.3)
                    
                elif tile == '3':
                    self.new_button = New_Button(self, col, row - 0.3)
                    
                elif tile == '4':
                    self.back_button = Back_Button(self, col, row - 0.3)
                    
        #buttons 
        self.resume_button_bkgd = pygame.Surface((self.resume_button.image.get_width() + 8, self.resume_button.image.get_height() + 16))
        self.greyed_out = pygame.Surface((self.resume_button.image.get_width() + 8, self.resume_button.image.get_height() + 16), pygame.SRCALPHA)
        self.greyed_out.fill((0, 0, 0, 100))
        self.new_button_bkgd = pygame.Surface((self.new_button.image.get_width() + 8, self.new_button.image.get_height() + 16))
        self.back_button_bkgd = pygame.Surface((self.back_button.image.get_width() + 8, self.back_button.image.get_height() + 16))

        while self.menu_loop:
            self.clock.tick(FPS)
            self.screen.fill(DARKER_GREY)
            
            #resume button background
            if self.resume_button.resume_hover:
                self.resume_button_bkgd.fill(LIGHT_GREY)
            else:
                self.resume_button_bkgd.fill(SLATE_GREY)
                
            if self.new_button.new_hover:
                self.new_button_bkgd.fill(LIGHT_GREY)
            else:
                self.new_button_bkgd.fill(SLATE_GREY)
                
            if self.back_button.back_hover:
                self.back_button_bkgd.fill(LIGHT_GREY)
            else:
                self.back_button_bkgd.fill(SLATE_GREY)
                
            self.all_sprites.draw(self.screen)
            
            self.screen.blit(self.resume_button_bkgd, (self.resume_button.rect.x, self.resume_button.rect.y - 8))
            self.screen.blit(self.new_button_bkgd, (self.new_button.rect.x, self.new_button.rect.y - 8))
            self.screen.blit(self.back_button_bkgd, (self.back_button.rect.x, self.back_button.rect.y - 8))
            
            self.buttons.draw(self.screen)
            self.button_text.draw(self.screen)
            
            if self.saved_level == 'tut':
                self.screen.blit(self.greyed_out, (self.resume_button.rect.x, self.resume_button.rect.y - 8))
                
            self.cursor_group.draw(self.screen)
            self.background_particles.draw(self.screen)
    
            #update
            self.all_sprites.update()
            self.cursor_group.update()
            self.buttons.update()
            self.background_particles.update()
            
            #spawn particles
            self.spawn_timer += 1
            if self.spawn_timer >= 10:
                self.spawn_timer = 0   
                Background_Particle(self)
                
            pygame.display.flip()
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    self.running = False
                    
    def load_credits_menu(self):
        self.menu_loop = True
        self.map = Map(self.map_dir + "credits_menu.txt")
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.Group()
        self.button_text = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
         
        #cursor
        Cursor(self)
        
        Button_Font(self, self.button_font, CREDITS_BUTTON, 40, 365, "Back")
        Button_Font(self, self.button_font, CREDITS_BUTTON_SHADOW, 37, 362, "Back")
        
        
        Button_Font(self, self.font, WHITE, 60, 110, "Thank You to my friends")
        Button_Font(self, self.font, WHITE, 10, 140, "- Angie,Julian,Edward,Connor -")
        
        Button_Font(self, self.font, WHITE, 10, 245, "font made by Roberto Mocci")
        Button_Font(self, self.font, WHITE, 10, 275, "sfx made using bfxr.net")
        
        Font(self, self.font, 36.5, 0.5, "v.1.0.0")
    
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #background griebling
                    Menu_Tile(self, col, row) 
                    
                elif tile == '2':
                    self.red = Block(self, col, row, "red")
                    
                elif tile == '3':
                    self.yellow = Block(self, col, row, "yellow")
                    
                elif tile == '4':
                    self.back_button = Back_Button(self, col, row - 0.3)
                    
        #buttons 
        self.red_block_bkgd = pygame.Surface((self.red.image.get_width() + 8, self.red.image.get_height() + 16))
        self.red_block_bkgd.fill(SLATE_GREY)
        self.yellow_block_bkgd = pygame.Surface((self.yellow.image.get_width() + 8, self.yellow.image.get_height() + 16))
        self.yellow_block_bkgd.fill(SLATE_GREY)
        self.back_button_bkgd = pygame.Surface((self.back_button.image.get_width() + 8, self.back_button.image.get_height() + 16))

        while self.menu_loop:
            self.clock.tick(FPS)
            self.screen.fill(DARKER_GREY)
            
            if self.back_button.back_hover:
                self.back_button_bkgd.fill(LIGHT_GREY)
            else:
                self.back_button_bkgd.fill(SLATE_GREY)
                
            self.all_sprites.draw(self.screen)
            
            self.screen.blit(self.red_block_bkgd, (self.red.rect.x, self.red.rect.y - 8))
            self.screen.blit(self.yellow_block_bkgd, (self.yellow.rect.x, self.yellow.rect.y - 8))
            self.screen.blit(self.back_button_bkgd, (self.back_button.rect.x, self.back_button.rect.y - 8))
            
            self.buttons.draw(self.screen)
            self.button_text.draw(self.screen)
        
            self.cursor_group.draw(self.screen)
            self.background_particles.draw(self.screen)
    
            #update
            self.all_sprites.update()
            self.cursor_group.update()
            self.buttons.update()
            self.background_particles.update()
            
            #spawn particles
            self.spawn_timer += 1
            if self.spawn_timer >= 10:
                self.spawn_timer = 0   
                Background_Particle(self)
                
            pygame.display.flip()
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    self.running = False    
                    
    def load_settings_menu(self):
        self.menu_loop = True
        self.map = Map(self.map_dir + "settings_menu.txt")
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.buttons = pygame.sprite.Group()
        self.button_text = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
        self.sound_buttons = pygame.sprite.Group()
      
        #cursor
        Cursor(self)
        
        #button text
        Button_Font(self, self.button_font, CREDITS_BUTTON, 40, 365, "Back")
        Button_Font(self, self.button_font, CREDITS_BUTTON_SHADOW, 37, 362, "Back")
        
        Button_Font(self, self.button_font, START_BUTTON, 40, 117, "Music")
        Button_Font(self, self.button_font, START_BUTTON_SHADOW, 38, 114, "Music")
        
        Button_Font(self, self.button_font, SETTINGS_BUTTON, 40, 243, "Sfx")
        Button_Font(self, self.button_font, SETTINGS_BUTTON_SHADOW, 37, 240, "Sfx")
        
        #music volume adjuster
        self.down = Music_Vol_Button(self, 318, 125, 'down')
        self.up = Music_Vol_Button(self, 410, 125, 'up')
        
        self.volume_text = Button_Font(self, self.font, WHITE, 360, 128, str(int(self.current_volume * 10)))
        Button_Font(self, self.font, WHITE, 413, 127, '+')
        Button_Font(self, self.font, WHITE, 321, 127, '-')
        
        self.volume_box = pygame.Surface((38, 32))
        self.volume_box.fill(BLACK)
        
        #sfx volume adjuster
        self.down_2 = Sfx_Vol_Button(self, 260, 250, 'down')
        self.up_2 = Sfx_Vol_Button(self, 348, 250, 'up')
        
        self.sfx_text = Button_Font(self, self.font, WHITE, 300, 252, str(int(self.current_sfx_volume * 10)))
        Button_Font(self, self.font, WHITE, 351, 253, '+')
        Button_Font(self, self.font, WHITE, 263, 253, '-')
        
        self.sfx_box = pygame.Surface((38, 32))
        self.sfx_box.fill(BLACK)
        
        #version info
        Font(self, self.font, 36.5, 0.5, "v.1.0.0")

        #tilemap objecs
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #background griebling
                    Menu_Tile(self, col, row) 
                    
                elif tile == '2':
                    self.red = Block(self, col, row, "red")
                    
                elif tile == '3':
                    self.yellow = Block(self, col, row, "yellow")
                    
                elif tile == '4':
                    self.back_button = Back_Button(self, col, row - 0.3)
                    
        #buttons 
        self.red_block_bkgd = pygame.Surface((self.red.image.get_width() + 8, self.red.image.get_height() + 16))
        self.red_block_bkgd.fill(SLATE_GREY)
        self.yellow_block_bkgd = pygame.Surface((self.yellow.image.get_width() + 8, self.yellow.image.get_height() + 16))
        self.yellow_block_bkgd.fill(SLATE_GREY)
        self.back_button_bkgd = pygame.Surface((self.back_button.image.get_width() + 8, self.back_button.image.get_height() + 16))

        while self.menu_loop:
            self.clock.tick(FPS)
            self.screen.fill(DARKER_GREY)
            
            if self.back_button.back_hover:
                self.back_button_bkgd.fill(LIGHT_GREY)
            else:
                self.back_button_bkgd.fill(SLATE_GREY)
                
            self.all_sprites.draw(self.screen)
            
            self.screen.blit(self.red_block_bkgd, (self.red.rect.x, self.red.rect.y - 8))
            self.screen.blit(self.yellow_block_bkgd, (self.yellow.rect.x, self.yellow.rect.y - 8))
            self.screen.blit(self.back_button_bkgd, (self.back_button.rect.x, self.back_button.rect.y - 8))
            
            self.buttons.draw(self.screen)
            self.screen.blit(self.volume_box, (355, 120))
            self.screen.blit(self.sfx_box, (295, 245))
            self.sound_buttons.draw(self.screen)
            self.button_text.draw(self.screen)
        
            self.cursor_group.draw(self.screen)
            self.background_particles.draw(self.screen)
    
            #update
            self.all_sprites.update()
            self.cursor_group.update()
            self.buttons.update()
            self.background_particles.update()
            self.sound_buttons.update()
            
            #spawn particles
            self.spawn_timer += 1
            if self.spawn_timer >= 10:
                self.spawn_timer = 0
                Background_Particle(self)
                
            self.volume_text.change_text(360, 128, str(round(self.current_volume * 10)))
            self.sfx_text.change_text(300, 252, str(round(self.current_sfx_volume * 10)))
            
            pygame.display.flip()
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    self.running = False   
                if event.type == pygame.MOUSEBUTTONUP:
                    self.up.change_volume(event.pos)
                    self.down.change_volume(event.pos)
                    
                    self.up_2.change_volume(event.pos)
                    self.down_2.change_volume(event.pos)        
                    
    def cut_scene(self):
        self.menu_loop = True
        self.map = Map(self.map_dir + "cut_scene.txt")
        self.switch_tracks()
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.floors = pygame.sprite.Group()
        self.demo_portal = pygame.sprite.Group()
        self.background_particles = pygame.sprite.Group()
        self.light = pygame.sprite.Group()

        self.particle_counter = 0
        self.portal_particle_counter = 0
        
        #tilemap objecs
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '0':
                   self.demo_player = Demo_Player(self, col, row)
                    
                elif tile == "1":
                    #topleft outside corner
                    Floor(self, col, row, 0)
                    
                elif tile == "2":
                    #floor
                    Floor(self, col, row, 1)
                    
                elif tile == "3":
                    #topright outside corner
                    Floor(self, col, row, 2)
                    
                elif tile == "4":
                    #floor and topleft inside corner
                    Floor(self, col, row, 3)
                    
                elif tile == "5":
                    #floor and topright inside corner
                    Floor(self, col, row, 4)
                    
                elif tile == "6":
                    #right wall
                    Floor(self, col, row, 5)
                    
                elif tile == "7":
                    #background griebling
                    Menu_Tile(self, col, row)
                    
                elif tile == "8":
                    #left wall
                    Floor(self, col, row, 7)
                    
                elif tile == "9":
                    #ceiling and bottom left inside corner
                    Floor(self, col, row, 8)
                    
                elif tile == "a":
                    #ceiling and bottom right inside corner
                    Floor(self, col, row, 9)
                    
                elif tile == "b":
                    #bottom left outside corner
                    Floor(self, col, row, 10)
                
                elif tile == "c":
                    #ceiling
                    Floor(self, col, row, 11)
                    
                elif tile == "d":
                    #botom right outside corner
                    Floor(self, col, row, 12)
                    
                elif tile == "e":
                    #topleft inside corner
                    Floor(self, col, row, 13)
                    
                elif tile == "f":
                    #topright inside corner
                    Floor(self, col, row, 14)
                    
                elif tile == "j":
                    #bottom left inside corner
                    Floor(self, col, row, 18)
                    
                elif tile == "k":
                    #bottom right inside corner
                    Floor(self, col, row, 19)
                    
                elif tile == "l":
                    #griebling low 
                    Floor(self, col, row, 20)
                    
                elif tile == "m":
                    #griebling high
                    Floor(self, col, row, 21)
                    
                elif tile == "n":
                    #griebling
                    Floor(self, col, row, 22)
                    
                elif tile == 'o':
                    Menu_Tile(self, col, row)
                    Menu_Tile(self, col + 2, row)
                    Bridge(self, col, row)
                    
                elif tile == 'p':
                    Light_Ray(self, col, row)
                    
                elif tile == 'q':
                    self.demo = Demo_Portal(self, col, row)
            
        self.text = Font(self, self.font, 0, 0, "")
        
        self.camera = Camera(self.map.width, self.map.height)
        
        while self.menu_loop:
            self.clock.tick(FPS)
            
            #draw
            self.screen.fill(DARK_GREY)

            #draw the sprites to the screen
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
                
            darkness = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, 100))
            
            self.background_particles.draw(self.screen)
            
            #update
            self.all_sprites.update()
            self.background_particles.update()
            self.camera.update(self.demo_player)
            
            #spawn particles
            self.spawn_timer += 1
            if self.spawn_timer >= 5:
                self.spawn_timer = 0   
                Background_Particle(self)
                
            self.portal_particle_counter += 1
            if self.portal_particle_counter >= 10:
                self.portal_particle_counter = 0
                Portal_Particle(self, self.demo.rect.centerx, self.demo.rect.centery)
                
            self.particle_counter += 1
            if self.particle_counter >= 3:
                self.particle_counter = 0 
                if not self.demo_player.idle and self.demo_player.can_move:
                    Demo_Particle(self, self.demo_player.rect.centerx, self.demo_player.rect.y + self.demo_player.image.get_height())
              
            for sprite in self.light:
                darkness.blit(sprite.image, self.camera.apply(sprite), special_flags=pygame.BLEND_RGBA_SUB)
                
            self.screen.blit(darkness, (0, 0))
            
            pygame.display.flip()
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_loop = False
                    self.running = False   
               
#create a new game object
g = Game()

g.main_menu()

#loop as long as the game is running
while g.running:
    g.new()
    g.run()

#close the game
pygame.quit()
sys.exit()     