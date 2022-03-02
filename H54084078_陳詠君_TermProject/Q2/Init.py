import pygame
import random 
import math
import matplotlib.pyplot as plt

CALL_LIST = []
INTERVAL_LIST = []

FPS = 100
BLOCK_SIZE = (50,50)
BASE_STATION_SIZE = (30,30)
ROAD_WIDTH = 15
RATIO = BLOCK_SIZE[0] / 2.5
WINDOW_SIZE = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * 10 - ROAD_WIDTH , (BLOCK_SIZE[1] + ROAD_WIDTH) * 10 - ROAD_WIDTH )

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

RUNNING_STATE = True
CLOCK = pygame.time.Clock()
#PROJECT_NAME = "THRESHOLD"
FONT_NAME = pygame.font.match_font('arial')

P_TRANSMIT = 120 #dB

LAMBDA = 1 / 4
TOTAL_SWITCH = 0
SPEED = 1.2

BLOCK_SPRITE = pygame.sprite.Group()
BASE_STATION_SPRITE = pygame.sprite.Group()
CAR_SPRITE = pygame.sprite.Group()
BLOCKS = []
BASE_STATIONS = []
CARS = []
COORDINATE = []

def CHECK_DUPLICATE(i,j,list):
    for k in range(len(list)):
        if i == list[k][0] and j == list[k][1]:
            return 1
    return 0
        
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

def overlap(time1,time2):
    if time1[0] <= time2[1] and time1[1] >= time2[0]:
        return True
    else:
        return False
def calls_per_hour():
    while True:
        x = round( random.gauss(mu = 2, sigma = 2) )
        if x >= 0:
            break
    return x