import pygame, sys, time

screen_w = 800
screen_h = 600
eye_width = 60
mouth_width = 10

white = [255, 255, 255]
red = [255, 0, 0]
black = [0,0,0]

l_eye_x = 230
l_eye_y = 270
r_eye_x = 570
r_eye_y = 270
default_spd = 5
dy = default_spd
dx = default_spd


pygame.init()
screen = pygame.display.set_mode([screen_w,screen_h])

clock = pygame.time.Clock()

pygame.display.set_caption("Baymax Interface")
pygame.display.flip()

def default_pos():
    global l_eye_x, l_eye_y, r_eye_y, r_eye_x, dx, dy
    l_eye_x = 230
    l_eye_y = 270
    r_eye_x = 570
    r_eye_y = 270
    dy = 0
    dx = 0

def screen_saver_movement():
    global l_eye_x, l_eye_y, r_eye_y, r_eye_x, dx, dy, default_spd

    if(dx == 0 or dy == 0):
        dx = default_spd
        dy = default_spd

    if (l_eye_x < eye_width):
        dx = abs(dx)

    elif(r_eye_x > screen_w - eye_width) :
        dx = -abs(dx)

    if(l_eye_y < eye_width or r_eye_y < eye_width) :
        dy = abs(dy)

    elif(l_eye_y > screen_h - eye_width or r_eye_y > screen_h - eye_width) :
        dy = -abs(dy)


    l_eye_x += dx
    l_eye_y += dy
    r_eye_x += dx
    r_eye_y += dy




i = 0
running = True
while running:
    screen.fill(white)

    if (i < 500) :
        screen_saver_movement()

    elif(i >= 500 and i < 1000) :
        default_pos()

    else:
        i = 0
   


    # Drawing baymax eyes 0----0
    pygame.draw.line(screen, black, (l_eye_x,l_eye_y), (r_eye_x,r_eye_y), mouth_width)

    pygame.draw.circle(screen,black,(l_eye_x,l_eye_y), eye_width)
    pygame.draw.circle(screen,black,(r_eye_x,r_eye_y), eye_width)

    #clock.tick(60)
    i += 1

    pygame.display.update()
