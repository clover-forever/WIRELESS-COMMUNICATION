from Init import *

ENTROPY = 25 #dB

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
    

    
def determine_base_station(car,BASE_STATIONS,initial): #determine the largest power of base station to connect
    P_RECEIVE = 0
    LARGEST = float("-inf")
    old_index = -1
    new_index = -1
    return_index = -1
    if initial == True: # FIND LARGEST
        for j in range(len(BASE_STATIONS)):
            base_station = BASE_STATIONS[j]
            frequency = base_station.frequency
            distance = calculate_distance(car.rect.centerx , car.rect.centery , base_station.rect.centerx , base_station.rect.centery)
            path_loss = calculate_path_loss(frequency,distance)
            P_RECEIVE = P_TRANSMIT - path_loss
            if P_RECEIVE > LARGEST:
                LARGEST = P_RECEIVE
                new_index = j
        P_RECEIVE = LARGEST
        return_index = new_index
    elif initial == False:
        # FIND CURRENT PR
        old_index = car.current_base_station
        frequency = BASE_STATIONS[old_index].frequency
        base_station_x = BASE_STATIONS[old_index].rect.centerx
        base_station_y = BASE_STATIONS[old_index].rect.centery
        distance = calculate_distance(car.rect.centerx , car.rect.centery , base_station_x , base_station_y)
        path_loss = calculate_path_loss(frequency,distance)
        CURRENT_P_RECEIVE = P_TRANSMIT - path_loss

        # FIND LARGEST PR AND DETERMINE WHETHER SWITCH TO IT
        for j in range(len(BASE_STATIONS)): #找最大的PR
            base_station = BASE_STATIONS[j]
            frequency = base_station.frequency
            distance = calculate_distance(car.rect.centerx , car.rect.centery , base_station.rect.centerx , base_station.rect.centery)
            path_loss = calculate_path_loss(frequency,distance)
            P_RECEIVE = P_TRANSMIT - path_loss
            if P_RECEIVE > LARGEST:
                LARGEST = P_RECEIVE
                new_index = j
        if (LARGEST - CURRENT_P_RECEIVE) > ENTROPY:
            P_RECEIVE = LARGEST
            return_index = new_index
        else:
            P_RECEIVE = CURRENT_P_RECEIVE
            return_index = old_index

    color = BASE_STATIONS[return_index].color
    car.P_RECEIVE = P_RECEIVE      
    return return_index , P_RECEIVE , color


def time_intervals(n):
    times = []
    for i in range(n):
        if i == 0:
            period = random.gauss(mu = 180, sigma = 40)
            period = round(period)
            start_time = random.randrange(0,3600)
            end_time = start_time + period
            time = (start_time, end_time)
            times.append(time)
            INTERVAL_LIST.append(period)
        else:
            while True:
                count = 0
                period = random.gauss(mu = 180, sigma = 40)
                period = round(period)
                start_time = random.randrange(0,3600)
                end_time = start_time + period
                if end_time >= 3600:
                    continue
                new_time = (start_time,end_time)
                for time in times:
                    if overlap(time,new_time) == False:
                        count += 1
                if(count == len(times)):
                    times.append(new_time)
                    INTERVAL_LIST.append(period)
                    break                
    times.sort(key = lambda x: x[0])
    return times

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

def CREATE_CAR():
    for i in range(4):
        for j in range(0,9):
            arrival_prob = arrival_probability()
            prob = random.randrange(0 , 10**7)
            
            if(i == 0): # DOWN
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = 0
                    car_temp = CAR(x,y,0)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.color = BLACK
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 1): # UP
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = ( BLOCK_SIZE[1] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[1]
                    car_temp = CAR(x,y,1)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.color = BLACK
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 2): # RIGHT
                if prob < arrival_prob:
                    x = 0 
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,2)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.color = BLACK
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 3): # LEFT
                if prob < arrival_prob:
                    x = ( BLOCK_SIZE[0] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[0]
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,3)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.color = BLACK
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
def UPDATE():
    global TOTAL_SWITCH
    for car in CARS:
        if check_in_map(car.rect.left , car.rect.right , car.rect.top , car.rect.bottom) == 0:
            car.kill()
            CARS.remove(car)            
    
    for base_station in BASE_STATIONS:
        text = str(base_station.frequency) 
        draw_text(text , 11 , base_station.rect.centerx , base_station.rect.centery , WHITE)

    for i in range(len(CARS)):
        car = CARS[i]
        if car.connect == True:
            old_index = car.current_base_station
            new_index , P_receive , color = determine_base_station(car,BASE_STATIONS,False)
            car.current_base_station = new_index
            car.color = color
              
            P_receive = round(P_receive,2)     
            text = str(P_receive) + " dB"
            car_pos = (car.rect.centerx , car.rect.centery)
            base_station_pos = ( BASE_STATIONS[new_index].rect.centerx , BASE_STATIONS[new_index].rect.centery)
            #draw_line(car.color , car_pos , base_station_pos , 1)
            #draw_text(text , 14 , car.rect.x+10 , car.rect.y-10 , car.color)
            if(new_index != old_index):
                TOTAL_SWITCH = TOTAL_SWITCH + 1
                print("Handoff : ",TOTAL_SWITCH)
        
class BLOCK(pygame.sprite.Sprite):
    def __init__(self,i,j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(BLOCK_SIZE)
        self.color = BROWN
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()

        self.rect.x = (BLOCK_SIZE[0]+ROAD_WIDTH) * i
        self.rect.y = (BLOCK_SIZE[1]+ROAD_WIDTH) * j
    
    def update(self):
        return
        
class BASE_STATION(pygame.sprite.Sprite):
    def __init__(self,i,j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(BASE_STATION_SIZE)
        color_index = random.randrange(1,11)
        self.color = COLORS[color_index-1]
        self.frequency = color_index * 100
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = ( (BLOCK_SIZE[0]+ROAD_WIDTH) * i) + (BLOCK_SIZE[0]-BASE_STATION_SIZE[0])/2
        self.rect.y = ( (BLOCK_SIZE[1]+ROAD_WIDTH) * j) + (BLOCK_SIZE[1]-BASE_STATION_SIZE[1])/2
        
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
        self.rect = self.image.get_rect()  
        self.rect.x = i+2.5
        self.rect.y = j+2.5
        self.direction = direction
        self.P_RECEIVE = 0
        # new variables
        self.time_count = 0
        self.calls = 0
        self.time_intervals = []
        self.connect = False

    def check_turn(self,x,y):
        for i in range(10):
            for j in range(10):
                car_x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * i) + BLOCK_SIZE[0]
                car_y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j) + BLOCK_SIZE[1]
                if car_x == x and car_y == y:
                    return 1
        return 0
        
    def update(self):
        if self.time_count == 0:
            self.calls = calls_per_hour()
            self.time_intervals = time_intervals(self.calls)
            CALL_LIST.append(self.calls)
            
        check = self.check_turn(self.rect.x,self.rect.y)
        if check == 1:
            prob = random.randint(1,32)
            if prob <= 16:
                self.direction = self.direction + 0
            elif prob >= 17 and prob <= 18:
                self.direction = self.direction + 2 
            elif prob >= 19 and prob <= 26:
                self.direction = self.direction + 1
            else:
                self.direction = self.direction - 1
            self.direction = self.direction % 4
        
        if self.direction == 0:
            self.rect.y += SPEED
        elif self.direction == 1:
            self.rect.y -= SPEED
        elif self.direction == 2:
            self.rect.x += SPEED
        elif self.direction == 3:
            self.rect.x -= SPEED   
        
        self.time_count += 1
        if len(self.time_intervals) > 0:
            if self.time_count == self.time_intervals[0][0]:
                self.color = self.color
                self.connect = True
                #print("connect")
            if self.time_count == self.time_intervals[0][1]:
                self.color = BLACK
                self.connect = False
                self.calls -= 1
                del(self.time_intervals[0])
                #print("disconnect")
        if self.time_count == 3600:
            self.time_count = 0
        
        self.image.fill(self.color)

if __name__ == "__main__":
    pygame.init()
    #pygame.display.set_caption(PROJECT_NAME)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    CREATE_BLOCK_AND_BASE_STATION()
    # GAME LOOP
    while RUNNING_STATE == True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING_STATE = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING_STATE = False
        # CAR
        CREATE_CAR()
        # 畫面顯示
        screen.fill(SILVER)
        BLOCK_SPRITE.draw(screen)
        BASE_STATION_SPRITE.draw(screen)
        CAR_SPRITE.draw(screen)
        # UPDATE
        BLOCK_SPRITE.update()
        BASE_STATION_SPRITE.update()
        CAR_SPRITE.update()
        UPDATE()
        pygame.display.update()
    pygame.quit()
    
    figure,axes = plt.subplots(2,1,tight_layout=True)
    figure.canvas.manager.set_window_title("NORMAL DITRIBUTION")
    axes[0].hist(CALL_LIST , bins=100) #
    axes[0].set_ylabel('#',fontweight ='bold')
    axes[0].set_xlabel('# of calls/hr',fontweight ='bold')
    #axes[0].set_ylim(0,8000)
    axes[0].set_title("calls per hr")
    axes[1].hist(INTERVAL_LIST , bins=100)
    axes[1].set_ylabel('#',fontweight ='bold')
    axes[1].set_xlabel('secs',fontweight ='bold')
    axes[1].set_title("average call time")
    plt.show()