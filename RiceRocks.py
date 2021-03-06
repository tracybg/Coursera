# Direct access via this link http://www.codeskulptor.org/#user45_aqTW3yHEWJAU8ET.py

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
time = 0
explosion_time = 0
started = False
sprite_constants = [-2, -1, 1, 2]

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
bg_soundtrack_normal = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
bg_soundtrack_upbeat = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.shoot = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = angle_to_vector(self.angle)
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + (90), self.image_center[1]], 
                              self.image_size, [self.pos[0], self.pos[1]], 
                              self.image_size, self.angle)
                        
        else:   
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              [self.pos[0], self.pos[1]], self.image_size, self.angle)            
    
    def ship_thrust(self):
        if self.thrust:
            ship_thrust_sound.play()
        
        else:
            ship_thrust_sound.rewind()            
    
    def ship_shoot(self):
        my_ship.shoot = True        
        missile_pos = [self.forward[0] * 45 + self.pos[0], self.forward[1] * 45 + self.pos[1]]
        missile_vel = [self.forward[0] * 8, self.forward[1] * 8]        
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
        
    def update(self):
        self.ship_thrust()
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] % WIDTH) + self.vel[0]
        self.pos[1] = (self.pos[1] % HEIGHT) + self.vel[1]
        self.forward = angle_to_vector(self.angle)
        
        if self.thrust == True:
            self.vel[0] += self.forward[0] * 0.5
            self.vel[1] += self.forward[1] * 0.5
        
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95      
            
            
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def collide(self, other_object):
        return dist(self.pos, other_object.pos) <= self.radius + other_object.radius        
        
    def draw(self, canvas):
        global explosion_time
        if self.animated:
            explosion_dim = 24
            current_explosion_index = explosion_time % explosion_dim
            current_explosion_center = [self.image_center[0] +  current_explosion_index * self.image_size[0], 
                                        self.image_center[1]]
            canvas.draw_image(explosion_image, current_explosion_center, 
                              self.image_size, [self.pos[0], self.pos[1]], self.image_size) 
            explosion_time += 1   
            
        
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              [self.pos[0], self.pos[1]], self.image_size, self.angle)    
    
    def update(self):
        self.age += 1
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] % WIDTH) + self.vel[0]
        self.pos[1] = (self.pos[1] % HEIGHT) + self.vel[1]
        return self.age >= self.lifespan
             
        
def draw(canvas):
    global time, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # user interface
    canvas.draw_text('Lives: ' + str(lives), (50, 50), 32, 'White')
    canvas.draw_text('Score: ' + str(score), (650, 50), 32, 'White')

    # check for collisions
    if lives > 0:
        if group_collide(rock_group, my_ship):
            lives -= 1  
        score += group_group_collide(missile_group, rock_group)
    
    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
   
    # draw splash screen if not started
    if lives == 0:
        started = False
        
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())  
    
     
# timer handler that spawns a rock 
class Randomizer():
    global WIDTH, HEIGHT
    
    def __init__(self):
        pass
    
    def rand_choice(self, lst):
        return random.choice(lst)
    
    def rand_pos(self):
        return WIDTH * random.random(), HEIGHT * random.random()
    
    def rand_vel(self, lst):
        return random.choice(lst), random.choice(lst)
    
    def rand_angle(self):
        return math.pi * random.random() * 2
    
    def rand_angle_vel(self, lst):
        return random.random() * random.choice(lst) * .1 + 0.1 

Rand = Randomizer()

def rock_spawner():
    global a_rock, started
    if len(rock_group) < 12 and started:
        a_rock = Sprite(Rand.rand_pos(), Rand.rand_vel(sprite_constants), Rand.rand_angle(), 
                    Rand.rand_angle_vel(sprite_constants), asteroid_image, asteroid_info)
        if dist(a_rock.pos, my_ship.pos) > 100:
            rock_group.add(a_rock)      

            
# helper functions to control the ship
key_map = {'left': ['angle', -1], 'right' : ['angle', 1], 'up' : ['thrust', True], 'space' : ['shoot', True]}
        
def key_to_action(key):
    for k in key_map:       
        if key == simplegui.KEY_MAP[k]:
            return key_map[k]
        
def key_down(key):
    if key_to_action(key):
        if key_to_action(key)[0] == 'angle':
            my_ship.angle_vel += key_to_action(key)[1] * 0.05
        
        elif key_to_action(key)[0] == 'thrust':
            my_ship.thrust = key_to_action(key)[1]
    
        else:        
            my_ship.ship_shoot()
    
def key_up(key):
    if key_to_action(key):
        if key_to_action(key)[0] == 'angle':
            my_ship.angle_vel = key_to_action(key)[1] * 0 
        
        elif key_to_action(key)[0] == 'thrust':
            my_ship.thrust = False

            
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True               
    restart_game()

    
# helper function to process sprite groups
def process_sprite_group(group_of_sprites, canvas):
    for sprite in list(group_of_sprites):
        sprite.update()
        sprite.draw(canvas)
        if sprite.update():
            group_of_sprites.remove(sprite)
         
    
# helper functions for collisions 
def group_collide(group, other_object):
    global explosion_group
    for g in list(group):
        if g.collide(other_object):
            group.discard(g)
            explosion = Sprite(g.pos, [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)  
            explosion_group.add(explosion)
            return True
    return False
            
def group_group_collide(group1, group2):
    collision_counter = 0
    for g in list(group1):
        if group_collide(group2, g):
            group1.discard(g)
            collision_counter += 1
            
    return collision_counter

# helper function to restart game
def restart_game():
    global time, lives, score, rock_group, missile_group, explosion_group
    bg_soundtrack_upbeat.rewind()
    score = 0
    lives = 3
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    bg_soundtrack_upbeat.play()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], math.pi * 1.5, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
restart_game()
