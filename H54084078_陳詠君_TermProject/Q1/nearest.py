from Init import *
#6441
def determine_base_station(car,BASE_STATIONS,initial): #determine the largest power of base station to connect
    index = -1
    nearest_distance = float("inf")
    for j in range(len(BASE_STATIONS)):
        base_station = BASE_STATIONS[j]
        distance = calculate_distance(car.rect.centerx , car.rect.centery , base_station.rect.centerx , base_station.rect.centery)     
        if distance < nearest_distance:
            nearest_distance = distance
            index = j
    
    frequency = BASE_STATIONS[index].frequency
    path_loss = calculate_path_loss(frequency,nearest_distance)
    P_RECEIVE = P_TRANSMIT - path_loss
    color = BASE_STATIONS[index].color
   # car.color = color
    car.P_RECEIVE = P_RECEIVE
    
    return index , P_RECEIVE , color 
                
def CREATE_CAR():        
    for i in range(4):
        for j in range(0,9):
            arrival_prob = arrival_probability()
            prob = random.randrange(0, 10**7)
            
            if(i == 0): # DOWN
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = 0
                    car_temp = CAR(x,y,0)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 1): # UP
                if prob < arrival_prob:
                    x = ( (BLOCK_SIZE[0] + ROAD_WIDTH) * j ) + BLOCK_SIZE[0]
                    y = ( BLOCK_SIZE[1] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[1]
                    car_temp = CAR(x,y,1)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 2): # RIGHT
                if prob < arrival_prob:
                    x = 0 
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,2)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
                    car_temp.current_base_station = index
                    CARS.append(car_temp)
                    CAR_SPRITE.add(car_temp)
            elif(i == 3): # LEFT
                if prob < arrival_prob:
                    x = ( BLOCK_SIZE[0] + ROAD_WIDTH ) * 10 - BLOCK_SIZE[0]
                    y = ( (BLOCK_SIZE[1] + ROAD_WIDTH) * j ) + BLOCK_SIZE[1]
                    car_temp = CAR(x,y,3)
                    index , P_RECEIVE , color = determine_base_station(car_temp,BASE_STATIONS,True)
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
        new_index , P_receive , color = determine_base_station(car,BASE_STATIONS,False)
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