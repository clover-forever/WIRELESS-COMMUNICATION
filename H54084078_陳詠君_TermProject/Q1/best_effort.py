from Init import *
    #5225
def determine_base_station(car,BASE_STATIONS): #determine the largest power of base station to connect
    P_RECEIVE = 0
    LARGEST = float("-inf")
    index = -1
    for j in range(len(BASE_STATIONS)): #check
        base_station = BASE_STATIONS[j]
        frequency = base_station.frequency
        distance = calculate_distance(car.rect.centerx , car.rect.centery , base_station.rect.centerx , base_station.rect.centery)
        path_loss = calculate_path_loss(frequency,distance)
        P_RECEIVE = P_TRANSMIT - path_loss

        if P_RECEIVE > LARGEST: #handoff
            LARGEST = P_RECEIVE
            index = j

    P_RECEIVE = LARGEST
    color = BASE_STATIONS[index].color
    #car.color = color
    car.P_RECEIVE = P_RECEIVE
    return index , P_RECEIVE , color

def CREATE_CAR():        
    for i in range(4): #上下左右
        for j in range(0,9): #9個進入點(9*4=36)
            arrival_prob = arrival_probability()
            prob = random.randrange(0, 10**7)
            
            if(i == 0): # 從下面出來
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = 0
                    car_temp = CAR(x,y,0) # 0 : direction
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS)
                    #car_temp.color = color
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 1): # 從上面出來
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = ( BLOCK_SIZE[1] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[1]
                    car_temp = CAR(x,y,1)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS)
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 2): # 從右邊出來
                if prob < arrival_prob:
                    x = 0 
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,2)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS)
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 3): # 從左邊出來
                if prob < arrival_prob:
                    x = ( BLOCK_SIZE[0] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[0]
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,3)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS)
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
        base_station = BASE_STATIONS[0]
        old_index = car.current_base_station
        new_index , P_receive , color = determine_base_station(car,BASE_STATIONS)
        car.current_base_station = new_index
        #car.color = color
                        
        P_receive = round(P_receive,2)     
        text = str(P_receive) + " dB"
        car_pos = (car.rect.centerx , car.rect.centery)
        base_station_pos = ( BASE_STATIONS[new_index].rect.centerx , BASE_STATIONS[new_index].rect.centery)
        #draw_line(car.color , car_pos , base_station_pos , 1)
        #draw_text(text , 14 , car.rect.x+10 , car.rect.y-10 , car.color)
        
        if(new_index != old_index):
            TOTAL_SWITCH = TOTAL_SWITCH + 1
            print("Handoff : ",TOTAL_SWITCH)

if __name__ == "__main__":
    CREATE_BLOCK_AND_BASE_STATION()
    print(len(BASE_STATIONS))
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
        #screen.fill(BLACK)
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
