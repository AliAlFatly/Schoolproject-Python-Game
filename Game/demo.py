import pygame
pygame.init()

def click():
    if pygame.mouse.get_pressed()==(True, False, False):
        return True

def mouse_over():
    mx, my = pygame.mouse.get_pos()
    if mx > 50 and mx < 100 and my > 50 and my < 100:
        return True
    else:
        return False
        #Mouse is hovering over button



aafText = "iaweruawbr"



RED = (250, 0, 0)
BLUE = (0, 0, 250)
GREEN = (0, 250, 0)
surface = pygame.display.set_mode((500, 500))
#pygame.draw.rect(surface, (250, 0, 0))
surface.fill((0, 250, 0))



def update():
    h = True
    while h:
        button_filler = pygame.Surface((50, 50))
        button_filler.fill(BLUE)
        surface.blit(button_filler, (50, 50))

r = True
while r:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                r = False
            if event.key == pygame.K_a:
                print("a-getypt")
            if event.key == pygame.K_b:
                print("b-getypt")
            if event.key == pygame.K_c:
                update()


    surface.fill((250, 250, 250))

    if mouse_over() == True:
        pygame.draw.rect(surface, GREEN, (50, 50, 50, 50))
        if click():
            print("1")
    else:
        pygame.draw.rect(surface, RED, (50, 50, 50, 50))


    pygame.draw.rect(surface, BLUE, (150, 50, 50, 50))

    pygame.display.update()
