import pygame
import random 
import math
import matplotlib.pyplot as plt
RUNNING_STATE = True
CLOCK = pygame.time.Clock()
FONT_NAME = pygame.font.match_font('arial')

FPS = 100
BLOCK_SIZE = (50,50)
BASE_STATION_SIZE = (30,30)
ROAD_WIDTH = 15
RATIO = BLOCK_SIZE[0] / 2.5
WINDOW_SIZE = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * 10 - ROAD_WIDTH , (BLOCK_SIZE[1] + ROAD_WIDTH) * 10 - ROAD_WIDTH )

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192,192,192)
RED = (255, 0, 0)
ORANGE = (255,165,0)
YELLOW = (255, 204, 0)
LIME = (50,205,50)
GREEN = (0, 128, 0)
LIGHT_BLUE = (130,202,250)
BLUE = (0,131,255)
NAVY = (0,0,128)
PURPLE = (128,0,128)
PINK = (240,120,192)
BROWN = (106,48,48)
COLORS = [RED,ORANGE,YELLOW,LIME,GREEN,LIGHT_BLUE,BLUE,NAVY,PURPLE,PINK]

P_TRANSMIT = 120 #基地台傳輸端方送功率(dB)
# LAMBDA = 1 / 1200
LAMBDA = 1 / 4
TOTAL_SWITCH = 0
#SPEED = 1
SPEED = 1.2

# BLOCK
BLOCKS = []
BLOCK_SPRITE = pygame.sprite.Group()
# BASE STATION
BASE_STATIONS = []
BASE_STATION_SPRITE = pygame.sprite.Group()
COORDINATE = []    
# CAR
CARS = []
CAR_SPRITE = pygame.sprite.Group()

def CHECK_DUPLICATE(i,j,list):
    for k in range(len(list)):
        if i == list[k][0] and j == list[k][1]:
            return 1
    return 0

def draw_text(text, size, x, y, color):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    screen.blit(text_surface, text_rect)
    
def draw_line(color, start, end, width):
    pygame.draw.line(screen , color , start , end , width)  
    
def calculate_distance(car_x,car_y,base_station_x,base_station_y):
    delta_x_square = (car_x - base_station_x)**2
    delta_y_square = (car_y - base_station_y)**2
    result = (delta_x_square + delta_y_square)**(1/2)
    result = result / RATIO
    return result

def calculate_path_loss(frequency, distance):
    result = 32.45 + (20 * math.log10(frequency)) + (20 * math.log10(distance))
    return result

def check_in_map(left,right,top,bottom):
    if (right <= 0) or (left >= WINDOW_SIZE[0]) or (top >= WINDOW_SIZE[1]) or (bottom <= 0):
        return 0
    else:
        return 1

def arrival_probability():
    probability = ((LAMBDA * 1) ** 1) * (math.e ** -(LAMBDA * 1))
    probability = round(probability, 7) * (10**7)
    return probability

class BLOCK(pygame.sprite.Sprite):
    def __init__(self,i,j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(BLOCK_SIZE)
        self.color = BROWN
        self.image.fill(BROWN)
        #self.color = BLACK
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = (BLOCK_SIZE[0]+ROAD_WIDTH) * i 
        self.rect.y = (BLOCK_SIZE[1]+ROAD_WIDTH) * j 
    
    def update(self):
        return
        
class BASE_STATION(pygame.sprite.Sprite):
    def __init__(self,i,j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        color_index = random.randrange(1,11)
        self.color = COLORS[color_index-1]
        self.frequency = color_index * 100
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = ( (BLOCK_SIZE[0]+ROAD_WIDTH) * i) + (BLOCK_SIZE[0]-BASE_STATION_SIZE[0])/2
        self.rect.y = ( (BLOCK_SIZE[1]+ROAD_WIDTH) * j) + (BLOCK_SIZE[1]-BASE_STATION_SIZE[1])/2
        #print(self.rect.x , self.rect.y)
        print(i,j)
        prob = random.randrange(0,4)
        if prob == 0: #left
            self.rect.x = self.rect.x - (BLOCK_SIZE[0]-BASE_STATION_SIZE[0])/2
        elif prob == 1: #right
            self.rect.x = self.rect.x + (BLOCK_SIZE[0]-BASE_STATION_SIZE[0])/2
        elif prob == 2: #up
            self.rect.y = self.rect.y + (BLOCK_SIZE[1]-BASE_STATION_SIZE[1])/2
        elif prob == 3: #down
            self.rect.y = self.rect.y - (BLOCK_SIZE[1]-BASE_STATION_SIZE[1])/2
                    
    def update(self):
        return

class CAR(pygame.sprite.Sprite):           
    def __init__(self,i,j,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ROAD_WIDTH-5,ROAD_WIDTH-5))
        self.current_base_station = -1
        self.color = BLACK
        self.image.fill(self.color)
        # self.color = SILVER
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()  
        
        self.rect.x = i+2.5
        self.rect.y = j+2.5
        self.direction = direction
        self.P_RECEIVE = float("-inf")
                
    def check_turn(self,x,y):
        for i in range(10):
            for j in range(10):
                car_x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * i) + BLOCK_SIZE[0]
                car_y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j) + BLOCK_SIZE[1]
                if car_x == x and car_y == y:
                    return 1
        return 0
        
    def update(self):       
        check = self.check_turn(self.rect.x,self.rect.y)
        if check == 1:
            prob = random.randint(1,32)
            if prob <= 16: #前進
                self.direction = self.direction + 0 
            elif prob >= 17 and prob <= 18: #迴轉
                self.direction = self.direction + 2 
            elif prob >= 19 and prob <= 26: #左轉
                self.direction = self.direction + 1
            else: #右轉
                self.direction = self.direction - 1
            self.direction = self.direction % 4
        
        if self.direction == 0: #往上
            self.rect.y += SPEED
        elif self.direction == 1: #往下
            self.rect.y = self.rect.y - SPEED
        elif self.direction == 2: #往右
            self.rect.x = self.rect.x + SPEED
        elif self.direction == 3: #往左
            self.rect.x -= SPEED
        
        self.image.fill(self.color)

def CREATE_BLOCK_AND_BASE_STATION():
    for i in range(10):
        for j in range(10):
            block_temp = BLOCK(i,j)
            BLOCKS.append(block_temp)
            BLOCK_SPRITE.add(block_temp)
            prob = random.randrange(0,10)
            if(prob == 1):
                if ( CHECK_DUPLICATE(i,j,COORDINATE) == 0 ):
                    COORDINATE.append( (i,j) )
                    base_station_temp = BASE_STATION(i,j)
                    BASE_STATIONS.append(base_station_temp)
                    BASE_STATION_SPRITE.add(base_station_temp)