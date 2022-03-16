import random
import pygame
from pygame import mixer
pygame.init()

# Konstanty
biela = (255, 255, 255)
cierna = (0, 0, 0)
siminustextfarba = (0, 153, 102)
siva = (128, 128, 128)
siminusfont = pygame.font.Font('freesansbold.ttf', 35)
WIDTH = 400
HEIGHT = 500
pozadie = biela
postavicka = pygame.transform.scale(pygame.image.load('doodle.png'), (65,70))
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
casovac = pygame.time.Clock()
score = 0
high_score = 0
score_last = 0
game_over = False

# Premenne
postavicka_x = 170
postavicka_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
skok = False
zmena_y = 0
zmena_x = 0
rychlost_postavicky = 3
super_skoky = 2
viac_skokov = 0

# Muzika
muzika = pygame.mixer.music.load('Doodle Jump (Original Mix).mp3')
pygame.mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Obrazovka
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Doodle Jump')

# Kolízie
def check_collisions(obj_list, s):
    global postavicka_x
    global postavicka_y
    global zmena_y
    for i in range(len(obj_list)):
        if obj_list[i].colliderect([postavicka_x + 20, postavicka_y + 60, 45, 5]) and skok == False and zmena_y > 0:
            s = True
    return s

# Pohyb postavicky na y
def update_postavicka(y_pos):
    global skok
    global zmena_y
    vyska_skoku = 10
    gravity = .4
    if skok:
        zmena_y = -vyska_skoku
        skok = False
    y_pos += zmena_y
    zmena_y += gravity
    return y_pos

# Pridavanie platforiem
def update_platformy(sak_list_ne, y_pos, zmena):
    global score
    global high_score
    if y_pos < 290 and zmena < 0:
        for i in range(len(sak_list_ne)):
            sak_list_ne[i][1] -= zmena
    else:
        pass
    for item in range(len(sak_list_ne)):
        if sak_list_ne[item][1] > 500:
            sak_list_ne[item] = [random.randint(10, 320), random.randint(-50, -10) ,70, 10]
            score += 1
            if score == high_score:
                high_score = score
    return sak_list_ne


running = True
while running:
    casovac.tick(fps)
    screen.fill(pozadie)
    screen.blit(postavicka, (postavicka_x, postavicka_y))
    blocks = []
    score_text = font.render('Score: ' + str(score), True, cierna, pozadie)
    screen.blit(score_text, (280, 0))
    high_score_text = font.render('High score: ' + str(high_score), True, cierna, pozadie)
    screen.blit(high_score_text, (280, 20))

    score_text = font.render('Big Jump: ' + str(super_skoky), True, cierna, pozadie)
    screen.blit(score_text, (10, 10))
    if game_over:
        si_minus_text = siminusfont.render('Si mínus!', True, (random.randint(1 ,255), random.randint(1 ,255), random.randint(1 ,255)), pozadie)
        screen.blit(si_minus_text, (135, 80))


    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, cierna, platforms[i], 3, 3)
        blocks.append(block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                postavicka_x = 170
                postavicka_y = 400
                pozadie = biela
                score_last = 0
                super_skoky = 2
                viac_skokov = 0
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10],
                             [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
            if event.key == pygame.K_SPACE and not game_over and super_skoky > 0:
                super_skoky -= 1
                zmena_y = -15
            if event.key == pygame.K_a:
                zmena_x = -rychlost_postavicky
            if event.key == pygame.K_d:
                zmena_x = rychlost_postavicky
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                zmena_x = 0
            if event.key == pygame.K_d:
                zmena_x = 0

    skok = check_collisions(blocks, skok)
    postavicka_x += zmena_x

    if postavicka_y < 440:
        postavicka_y = update_postavicka(postavicka_y)
    else:
        game_over = True
        zmena_y = 0
        zmena_x = 0

    platforms = update_platformy(platforms, postavicka_y, zmena_y)

    if postavicka_x < -20:
        postavicka_x = -20
    elif postavicka_x > 330:
        postavicka_x = 330

    if zmena_x > 0:
        postavicka = pygame.transform.scale(pygame.image.load('doodle.png'), (65, 70))
    elif zmena_x < 0:
        postavicka = pygame.transform.flip(pygame.transform.scale(pygame.image.load('doodle.png'), (65, 70)), 1, 0)

    if score > high_score:
        high_score = score

    if score - score_last > 4:
        score_last = score
        pozadie = (random.randint(1 ,255), random.randint(1 ,255), random.randint(1 ,255))

    if score - viac_skokov > 50:
        viac_skokov = score
        super_skoky += 1

    pygame.display.flip()
pygame.quit()
