import numpy as np
import matplotlib.pyplot as plt
import pygame
import random
import classdefs as cls
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def observe(entity,spritesgroup,dist,scansgroup,ogroup,ggroup,dgroup):
    l=entity.rect.left
    lx=l-1
    r=entity.rect.right
    t=entity.rect.top
    tx=t-1
    b=entity.rect.bottom

    results = np.array([[0,0],[0,0],[0,0],[0,0]])

    rscan = cls.Scanner(r,t,1,10,"r")
    uscan = cls.Scanner(l,tx,10,1,"u")
    lscan = cls.Scanner(lx,t,1,10,"l")
    dscan = cls.Scanner(l,b,10,1,"d")
    scansgroup.add(rscan,uscan,lscan,dscan)

    for i in range(dist):
        rscan.update()
        if pygame.sprite.spritecollideany(rscan,spritesgroup):
            if pygame.sprite.spritecollideany(rscan,ogroup):
                results[0] = [1,i]
            elif pygame.sprite.spritecollideany(rscan,ggroup):
                results[0] = [2,i]
            elif pygame.sprite.spritecollideany(rscan,dgroup):
                results[0] = [3,i]
            break

    for i in range(dist):
        uscan.update()
        if pygame.sprite.spritecollideany(uscan,spritesgroup):
            if pygame.sprite.spritecollideany(uscan,ogroup):
                results[1] = [1,i]
            elif pygame.sprite.spritecollideany(uscan,ggroup):
                results[1] = [2,i]
            elif pygame.sprite.spritecollideany(uscan,dgroup):
                results[1] = [3,i]
            break

    for i in range(dist):
        lscan.update()
        if pygame.sprite.spritecollideany(lscan,spritesgroup):
            if pygame.sprite.spritecollideany(lscan,ogroup):
                results[2] = [1,i]
            elif pygame.sprite.spritecollideany(lscan,ggroup):
                results[2] = [2,i]
            elif pygame.sprite.spritecollideany(lscan,dgroup):
                results[2] = [3,i]
            break

    for i in range(dist):
        dscan.update()
        if pygame.sprite.spritecollideany(dscan,spritesgroup):
            if pygame.sprite.spritecollideany(dscan,ogroup):
                results[3] = [1,i]
            elif pygame.sprite.spritecollideany(dscan,ggroup):
                results[3] = [2,i]
            elif pygame.sprite.spritecollideany(dscan,dgroup):
                results[3] = [3,i]
            break

    for entity in scansgroup:
        entity.kill()

    return results

def onesim(maxlen):
    pygame.init()

    clock = pygame.time.Clock()

    #Sets the height and width of the environment
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # output array is num_frames*num_drones*num_coords
    posarr = np.zeros((maxlen,6,3))

    allsprites = pygame.sprite.Group()

    # 6 drones are currently hardcoded in with starting positions
    d1 = cls.Drone(100,300,0,1)
    d2 = cls.Drone(50,200,0,1)
    d3 = cls.Drone(75,250,0,1)
    d4 = cls.Drone(60,300,0,2)
    d5 = cls.Drone(90,400,0,2)
    d6 = cls.Drone(100,500,0,2)

    drones = pygame.sprite.Group()
    drones.add(d1,d2,d3,d4,d5,d6)
    allsprites.add(d1,d2,d3,d4,d5,d6)

    dronelist = [d1,d2,d3,d4,d5,d6]

    # A green 'goal' is randomly placed somehwere on the right side of the environment
    ygoal = np.random.randint(150,450)
    endgoal = cls.Goal(750,ygoal,0)

    goals = pygame.sprite.Group()
    goals.add(endgoal)
    allsprites.add(endgoal)

    goal_l = endgoal.rect.left
    goal_t = endgoal.rect.top

    # Two obstacles randomly placed in the middle of the environment
    yo1 = np.random.randint(150,450)
    o1 = cls.Obstacle(350,yo1,0,20,300,0)

    yo2 = np.random.randint(150,450)
    o2 = cls.Obstacle(550,yo2,0,20,300,0)

    obstacles = pygame.sprite.Group()
    obstacles.add(o1,o2)
    allsprites.add(o1,o2)

    # If running is ever false, the run terminates
    running = True
    counter = 0

    scans = pygame.sprite.Group()

    while running:
        # Can force exit the simulation using ESC or by closing the window
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        for entity in drones:
            x = observe(entity,allsprites,100,scans,obstacles,goals,drones)
            #print(x)


        # Drones update, according to the update function defined in Drone class
        #drones.update(SCREEN_WIDTH,SCREEN_HEIGHT)
        for entity in drones:
            prevl = entity.rect.left
            prevt = entity.rect.top
            prevdist = np.sqrt((goal_l-prevl)**2 + (goal_t-prevt)**2)

            entity.update(SCREEN_WIDTH,SCREEN_HEIGHT)
            
            nowl = entity.rect.left
            nowt = entity.rect.top
            nowdist = np.sqrt((goal_l-nowl)**2 + (goal_t-nowt)**2)

            gamma = 0.999

            reward = gamma**counter * (prevdist-nowdist)

            #print(goal_l,goal_t,prevl,prevt,prevdist,nowl,nowt,nowdist,reward)

        #print()



        screen.fill((0,0,0))

        for entity in allsprites:
            screen.blit(entity.surf, entity.rect)
            
        for entity in drones:
            # Drone is killed if it collides with an obstacle
            if pygame.sprite.spritecollideany(entity, obstacles):
                entity.kill()

            # Drone is killed if it collides with the goal (success!)
            if pygame.sprite.spritecollideany(entity,goals):
                entity.kill()

            # Both drones are killed if they collide with each other
            for entity2 in drones:
                if entity != entity2 and pygame.sprite.collide_rect(entity, entity2):
                    entity.kill()
                    entity2.kill()
    
        pygame.display.flip()

        dead = 0

        # Store results in posarr
        for i in range(len(dronelist)):
            entity = dronelist[i]
            if entity.alive():
                posarr[counter,i] = [entity.rect.left,entity.rect.top,0]
            else:
                dead += 1
                posarr[counter,i] = [-1,-1,-1]

        # Run ends early if all drones are dead
        if dead == 6:
            running = False

        # Run ends if max length has been reached
        counter += 1
        if counter >= maxlen:
            running = False

        # I'm not sure if this is helping the code run more smoothly or not
        clock.tick(60)

    pygame.quit()
    
    return posarr

def multisim(numsims,maxlen):
    multisimlist = []
    for i in range(numsims):
        x=onesim(maxlen)
        multisimlist.append(x)
    multisimlist=np.array(multisimlist)

    return multisimlist