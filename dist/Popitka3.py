import os
import sys
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
menu_color = (156, 185, 9)
title_color = (225, 0, 0)
basic_font = pygame.font.SysFont('arial', 20)
FPS = 60
WIDTH = 608
HEIGHT = 384
STEP = 32

game_over = False

x1 = 300
y1 = 300
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
big_font = pygame.font.SysFont('verdana', 45)
snake_block = 32
global snake_speed, kolvo

kolvo = 0

snake_speed = 10
fonovaya = pygame.mixer.Sound("data/fonovaya.ogg")
fonovaya2 = pygame.mixer.Sound("data/veselo.ogg")
eating = pygame.mixer.Sound("data/kushat.ogg")
proigrish = pygame.mixer.Sound("data/game-over.ogg")
icon = pygame.image.load("data/icon.png")
x1_change = 0
y1_change = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Змейка')
pygame.display.set_icon(icon)


def Your_score(score):
    global value
    value = score_font.render("Ваш счет: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def message(msg, color):
    mesg = score_font.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 3.5, HEIGHT / 4.5])


def message2(msg2, color):
    mesg2 = score_font.render(msg2, True, color)
    screen.blit(mesg2, [WIDTH / 7.5, HEIGHT / 2.7])


def message3(msg3, color):
    mesg3 = score_font.render(msg3, True, color)
    screen.blit(mesg3, [WIDTH / 9, HEIGHT / 1.9])


def message4(msg4, color):
    mesg4 = score_font.render(msg4, True, color)
    screen.blit(mesg4, [WIDTH / 9, HEIGHT / 1.47])


def load_image(name, color_key=-1):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Не удалось загрузить изображение:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = OurSnake(x, y)
    return new_player, x, y


def next_level(selected_level):
    global tile_images, direction, running, level_x, level_y
    if selected_level == 'Уровень 3':
        level = load_level('level3.txt')
        tile_images = {'wall': load_image('box2.png'), 'empty': load_image('grass.png')}
    elif selected_level == 'Уровень 1':
        level = load_level('level1.txt')
        tile_images = {'wall': load_image('kirpich.jpg'), 'empty': load_image('parket.png')}
    elif selected_level == 'Уровень 2':
        level = load_level('level2.txt')
        tile_images = {'wall': load_image('voda.jpg'), 'empty': load_image('pesok.png')}

    tiles_group.empty()
    trava_group.empty()

    OurSnake, level_x, level_y = generate_level(level)

    running = True

    direction = 'right'

    gameLoop()


def show_settings():
    global cvetzmeiki
    ochki_slojnosti = 10
    slojnost = ''
    settings_screen = pygame.Surface((WIDTH, HEIGHT))
    settings_screen.fill(menu_color)
    global snake_speed
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Настройки скорости змеи", True, white)
    text_rect = text.get_rect(center=(WIDTH // 1.4, HEIGHT // 2 - 100))
    settings_screen.blit(text, text_rect)

    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Настройки цвета змеи", True, white)
    text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT // 2 - 100))
    settings_screen.blit(text, text_rect)

    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Настройки кол-ва яблок", True, white)
    text_rect = text.get_rect(center=(WIDTH // 1.4, HEIGHT // 2 + 50))
    settings_screen.blit(text, text_rect)

    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render("Настройки типа фруктов", True, white)
    text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT // 2 + 50))
    settings_screen.blit(text, text_rect)

    font = pygame.font.SysFont("comicsansms", 20)
    current_difficult_text = font.render("Ур.Сложности: " + str(slojnost), True, white)
    current_difficult_rect = text.get_rect(center=(WIDTH // 2 - 50, HEIGHT // 2 - 160))
    settings_screen.blit(current_difficult_text, current_difficult_rect)

    # Отображение текущей скорости змеи
    current_speed_text = font.render("Текущая скорость: " + str(snake_speed) + ' ', True, white)
    current_speed_rect = current_speed_text.get_rect(center=(WIDTH // 1.4, HEIGHT // 3 + 10))
    settings_screen.blit(current_speed_text, current_speed_rect)

    # Отображение кнопок для изменения скорости змеи
    increase_speed_button_rect = pygame.Rect(WIDTH // 1.4 - 100, HEIGHT // 3 + 50, 50, 50)
    decrease_speed_button_rect = pygame.Rect(WIDTH // 1.4 + 50, HEIGHT // 3 + 50, 50, 50)


    pygame.draw.rect(settings_screen, red, increase_speed_button_rect)
    pygame.draw.rect(settings_screen, red, decrease_speed_button_rect)

    font2 = pygame.font.SysFont("comicsansms", 25)
    plus_text = font2.render("+", True, white)
    plus_rect = plus_text.get_rect(center=increase_speed_button_rect.center)
    settings_screen.blit(plus_text, plus_rect)

    minus_text = font2.render("-", True, white)
    minus_rect = minus_text.get_rect(center=decrease_speed_button_rect.center)
    settings_screen.blit(minus_text, minus_rect)

    screen.blit(settings_screen, (0, 0))

    button2_width = 100
    button2_height = 50
    button2_x = WIDTH // 10 - button2_width // 2
    button2_y = HEIGHT // 100000 + button2_height // 2
    button2_rect = pygame.Rect(button2_x, button2_y, button2_width, button2_height)

    pygame.draw.rect(screen, red, button2_rect)

    font3 = pygame.font.SysFont("comicsansms", 15)
    text = font3.render("Вернуться", True, white)
    text_rect = text.get_rect(center=button2_rect.center)
    screen.blit(text, text_rect)
    pygame.display.flip()

    red_width = 30
    red_height = 30
    red_x = WIDTH // 10 + 40 - red_width // 2
    red_y = HEIGHT // 3 - 15 + red_height // 2
    red_rect = pygame.Rect(red_x, red_y, red_width, red_height)

    pygame.draw.rect(screen, red, red_rect)

    blue_width = 30
    blue_height = 30
    blue_x = WIDTH // 4 + 40 - blue_width // 2
    blue_y = HEIGHT // 2 - 15 + blue_height // 2
    blue_rect = pygame.Rect(blue_x, blue_y, blue_width, blue_height)

    pygame.draw.rect(screen, blue, blue_rect)

    green_width = 30
    green_height = 30
    green_x = WIDTH // 4 + 40 - green_width // 2
    green_y = HEIGHT // 3 - 15 + green_height // 2
    green_rect = pygame.Rect(green_x, green_y, green_width, green_height)

    pygame.draw.rect(screen, green, green_rect)

    yellow_width = 30
    yellow_height = 30
    yellow_x = WIDTH // 10 + 40 - yellow_width // 2
    yellow_y = HEIGHT // 2 - 15 + yellow_height // 2
    yellow_rect = pygame.Rect(yellow_x, yellow_y, yellow_width, yellow_height)

    pygame.draw.rect(screen, yellow, yellow_rect)

    yabloki_width = 50
    yabloki_height = 50
    yabloki_x = WIDTH // 1.4 - yabloki_width // 2 - 70
    yabloki_y = HEIGHT // 2 + yabloki_height // 2 + 80
    yabloki_rect = pygame.Rect(yabloki_x, yabloki_y, yabloki_width, yabloki_height)

    pygame.draw.rect(screen, red, yabloki_rect)

    font2 = pygame.font.SysFont("comicsansms", 15)
    vse_text = font2.render("1", True, white)
    vse1_rect = vse_text.get_rect(center=yabloki_rect.center)
    screen.blit(vse_text, vse1_rect)
    pygame.display.flip()

    yabloki2_width = 50
    yabloki2_height = 50
    yabloki2_x = WIDTH // 1.2 - yabloki2_width // 2
    yabloki2_y = HEIGHT // 2 + yabloki2_height // 2 + 80
    yabloki2_rect = pygame.Rect(yabloki2_x, yabloki2_y, yabloki2_width, yabloki2_height)

    pygame.draw.rect(screen, red, yabloki2_rect)

    font2 = pygame.font.SysFont("comicsansms", 15)
    vse_text = font2.render("3", True, white)
    vse1_rect = vse_text.get_rect(center=yabloki2_rect.center)
    screen.blit(vse_text, vse1_rect)
    pygame.display.flip()

    yabloki3_width = 50
    yabloki3_height = 50
    yabloki3_x = WIDTH // 1.36 - yabloki3_width // 2 - 10
    yabloki3_y = HEIGHT // 2 + yabloki3_height // 2 + 80
    yabloki3_rect = pygame.Rect(yabloki3_x, yabloki3_y, yabloki3_width, yabloki3_height)

    pygame.draw.rect(screen, red, yabloki3_rect)

    font2 = pygame.font.SysFont("comicsansms", 15)
    vse_text = font2.render("2", True, white)
    vse1_rect = vse_text.get_rect(center=yabloki3_rect.center)
    screen.blit(vse_text, vse1_rect)
    pygame.display.flip()

    yab_img = pygame.image.load('data/apple.png')
    yab_rect = yab_img.get_rect()
    yab_rect.center = (WIDTH // 4, HEIGHT // 2 + 100)
    screen.blit(yab_img, yab_rect)

    ban_img = pygame.image.load('data/banan.png')
    ban_rect = ban_img.get_rect()
    ban_rect.center = (WIDTH // 4 - 50, HEIGHT // 2 + 100)
    screen.blit(ban_img, ban_rect)

    klu_img = pygame.image.load('data/klubnika.png')
    klu_rect = klu_img.get_rect()
    klu_rect.center = (WIDTH // 4 + 50, HEIGHT // 2 + 100)
    screen.blit(klu_img, klu_rect)

    vse_width = 132
    vse_height = 30
    vse_x = WIDTH // 4 - vse_width // 2 - 10
    vse_y = HEIGHT // 2 + vse_height // 2 + 115
    vse_rect = pygame.Rect(vse_x, vse_y, vse_width, vse_height)

    pygame.draw.rect(screen, red, vse_rect)

    font2 = pygame.font.SysFont("comicsansms", 15)
    vse_text = font2.render("1 Случайный", True, white)
    vse1_rect = vse_text.get_rect(center=vse_rect.center)
    screen.blit(vse_text, vse1_rect)
    pygame.display.flip()

    settings = True
    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if increase_speed_button_rect.collidepoint(event.pos):
                    if snake_speed < 30:
                        screen.fill(menu_color, current_speed_rect)
                        screen.fill(menu_color, current_difficult_rect)
                        snake_speed += 1
                        ochki_slojnosti += 1
                        current_speed_text = font.render("Текущая скорость: " + str(snake_speed) + ' ', True, white)
                        screen.blit(current_speed_text, current_speed_rect)
                        pygame.draw.rect(screen, white, increase_speed_button_rect, 1)
                        pygame.draw.rect(screen, red, decrease_speed_button_rect, 1)
                        pygame.display.flip()
                elif decrease_speed_button_rect.collidepoint(event.pos):
                    screen.fill(menu_color, current_speed_rect)
                    screen.fill(menu_color, current_difficult_rect)
                    if snake_speed > 5:
                        snake_speed -= 1
                        ochki_slojnosti -= 1
                        current_speed_text = font.render("Текущая скорость: " + str(snake_speed) + ' ', True, white)
                        screen.blit(current_speed_text, current_speed_rect)
                        pygame.draw.rect(screen, white, decrease_speed_button_rect, 1)
                        pygame.draw.rect(screen, red, increase_speed_button_rect, 1)
                        pygame.display.flip()
                elif button2_rect.collidepoint(event.pos):
                    start_screen()
                    settings = False
                elif red_rect.collidepoint(event.pos):
                    cvetzmeiki = red
                    pygame.draw.rect(screen, white, red_rect, 1)
                    pygame.draw.rect(screen, blue, blue_rect, 1)
                    pygame.draw.rect(screen, yellow, yellow_rect, 1)
                    pygame.draw.rect(screen, green, green_rect, 1)
                    pygame.display.flip()
                elif blue_rect.collidepoint(event.pos):
                    cvetzmeiki = blue
                    pygame.draw.rect(screen, white, blue_rect, 1)
                    pygame.draw.rect(screen, red, red_rect, 1)
                    pygame.draw.rect(screen, yellow, yellow_rect, 1)
                    pygame.draw.rect(screen, green, green_rect, 1)
                    pygame.display.flip()
                elif green_rect.collidepoint(event.pos):
                    cvetzmeiki = green
                    pygame.draw.rect(screen, white, green_rect, 1)
                    pygame.draw.rect(screen, blue, blue_rect, 1)
                    pygame.draw.rect(screen, yellow, yellow_rect, 1)
                    pygame.draw.rect(screen, red, red_rect, 1)
                    pygame.display.flip()
                elif yellow_rect.collidepoint(event.pos):
                    cvetzmeiki = yellow
                    pygame.draw.rect(screen, white, yellow_rect, 1)
                    pygame.draw.rect(screen, blue, blue_rect, 1)
                    pygame.draw.rect(screen, red, red_rect, 1)
                    pygame.draw.rect(screen, green, green_rect, 1)
                    pygame.display.flip()
                elif yabloki_rect.collidepoint(event.pos):
                    global kolvo
                    screen.fill(menu_color, current_difficult_rect)
                    ochki_slojnosti = ochki_slojnosti + 10
                    kolvo = 1
                    pygame.draw.rect(screen, white, yabloki_rect, 1)
                    pygame.draw.rect(screen, red, yabloki2_rect, 1)
                    pygame.draw.rect(screen, red, yabloki3_rect, 1)
                    pygame.display.flip()
                elif yabloki2_rect.collidepoint(event.pos):
                    kolvo = 3
                    screen.fill(menu_color, current_difficult_rect)
                    pygame.draw.rect(screen, white, yabloki2_rect, 1)
                    pygame.draw.rect(screen, red, yabloki_rect, 1)
                    pygame.draw.rect(screen, red, yabloki3_rect, 1)
                    pygame.display.flip()
                elif yabloki3_rect.collidepoint(event.pos):
                    kolvo = 2
                    screen.fill(menu_color, current_difficult_rect)
                    ochki_slojnosti = ochki_slojnosti + 5
                    pygame.draw.rect(screen, white, yabloki3_rect, 1)
                    pygame.draw.rect(screen, red, yabloki2_rect, 1)
                    pygame.draw.rect(screen, red, yabloki_rect, 1)
                    pygame.display.flip()
                elif yab_rect.collidepoint(event.pos):
                    global b
                    b = 1
                    pygame.draw.rect(screen, white, yab_rect, 1)
                    pygame.draw.rect(screen, menu_color, ban_rect, 1)
                    pygame.draw.rect(screen, menu_color, klu_rect, 1)
                    pygame.draw.rect(screen, menu_color, vse_rect, 1)
                elif ban_rect.collidepoint(event.pos):
                    b = 2
                    pygame.draw.rect(screen, white, ban_rect, 1)
                    pygame.draw.rect(screen, menu_color, yab_rect, 1)
                    pygame.draw.rect(screen, menu_color, klu_rect, 1)
                    pygame.draw.rect(screen, menu_color, vse_rect, 1)
                elif klu_rect.collidepoint(event.pos):
                    b = 3
                    pygame.draw.rect(screen, white, klu_rect, 1)
                    pygame.draw.rect(screen, menu_color, ban_rect, 1)
                    pygame.draw.rect(screen, menu_color, vse_rect, 1)
                    pygame.draw.rect(screen, menu_color, yab_rect, 1)
                elif vse_rect.collidepoint(event.pos):
                    b = random.randint(1, 3)
                    pygame.draw.rect(screen, white, vse_rect, 1)
                    pygame.draw.rect(screen, menu_color, ban_rect, 1)
                    pygame.draw.rect(screen, menu_color, klu_rect, 1)
                    pygame.draw.rect(screen, menu_color, yab_rect, 1)
            else:
                screen.fill(menu_color, current_difficult_rect)
                current_difficult_text = font.render("Ур.Сложности: " + str(slojnost), True, white)
                screen.blit(current_difficult_text, current_difficult_rect)
                pygame.display.flip()
                if ochki_slojnosti <=10:
                    slojnost = 'Easy'
                if ochki_slojnosti > 15:
                    slojnost = 'Normal'
                if ochki_slojnosti > 25:
                    slojnost = 'Hard'
                if ochki_slojnosti > 30:
                    slojnost = 'V.Hard'
                if ochki_slojnosti >= 35:
                    slojnost = 'Очень сложно'
                if ochki_slojnosti == 40:
                    slojnost = 'Невозможно'

        clock.tick(FPS)
        pygame.display.flip()


class OurSnake(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((snake_block, snake_block))
        global cvetzmeiki
        self.image.fill(cvetzmeiki)
        self.rect = self.image.get_rect().move(snake_block * pos_x, snake_block * pos_y)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.rect.x = round(self.rect.x / snake_block) * snake_block
        self.rect.y = round(self.rect.y / snake_block) * snake_block

    def tail(self, snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, cvetzmeiki, [x[0], x[1], snake_block, snake_block])


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global b, c
        if b == 1:
            self.image = load_image('apple.png')
            self.rect = self.image.get_rect()
        elif b == 2:
            self.image = load_image('banan.png')
            self.rect = self.image.get_rect()
        elif b == 3:
            self.image = load_image('klubnika.png')
            self.rect = self.image.get_rect()
        else:
            b = random.randint(1, 3)
        self.foodx = round(random.randrange(32, WIDTH - 2 * snake_block) / 32.0) * 32.0
        self.foody = round(random.randrange(32, HEIGHT - 2 * snake_block) / 32.0) * 32.0

    def update(self):
        self.rect.x = self.foodx
        self.rect.y = self.foody


all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
trava_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
eaten_apples = pygame.sprite.Group()



def gameLoop():
    direction = 'right'
    c = random.randint(1, 2)
    if c == 1:
        fonovaya.play(-1)
    else:
        fonovaya2.play(-1)
    snake = OurSnake(5, 5)
    player_group.add(snake)
    game_over = False
    game_close = False
    pause = False  # Флаг, указывающий, находится ли игра в режиме паузы

    wall_collision = False
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    snake_list = []
    dlinazmei = 1

    while not game_over:
        while game_close == True:
            all_sprites.draw(screen)
            message("Вы проиграли!", yellow)
            message2('  Нажмите Q для выхода', yellow)
            message3('        в меню или C для', yellow)
            message4('         повторной игры', yellow)
            Your_score(dlinazmei - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_over = False
                        game_close = False
                        snake.rect.center = [WIDTH // 2 - (snake_block // 2), HEIGHT // 2 - (snake_block // 2)]
                        dlinazmei = 1
                        fonovaya.stop()
                        fonovaya2.stop()
                        gameLoop()
                    if event.key == pygame.K_q:
                        fonovaya.stop()
                        fonovaya2.stop()
                        dlinazmei = 1
                        game_over = True
                        all_sprites.empty()
                        apples.empty()
                        eaten_apples.empty()
                        global selected_level
                        selected_level = None
                        start_screen()
                        selected_level = start_screen()
                        generate_level(level)
                        next_level(selected_level)
                        screen.fill(black)

        global kolvo, b
        if len(apples) > kolvo:
            for _ in range(len(apples) - kolvo):
                apple = Apple()
                all_sprites.remove(apple)
                apples.remove(apple)
        elif len(apples) < kolvo:
            for _ in range(kolvo - len(apples)):
                if b == 1:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 2:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 3:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 4:
                    b = random.randint(1, 3)
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
        else:
            if kolvo == 1 and len(apples) == 0:
                if b == 1:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 2:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 3:
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
                elif b == 4:
                    b = random.randint(1, 3)
                    apple = Apple()
                    all_sprites.add(apple)
                    apples.add(apple)
            elif kolvo == 2 and len(apples) < kolvo:
                for _ in range(kolvo - len(apples)):
                    if b == 1:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 2:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 3:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 4:
                        b = random.randint(1, 3)
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
            elif kolvo == 3 and len(apples) < kolvo:
                for _ in range(kolvo - len(apples)):
                    if b == 1:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 2:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 3:
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)
                    elif b == 4:
                        b = random.randint(1, 3)
                        apple = Apple()
                        all_sprites.add(apple)
                        apples.add(apple)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'right':
                    snake.speedx = -snake_block
                    snake.speedy = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT and direction != 'left':
                    snake.speedx = snake_block
                    snake.speedy = 0
                    direction = 'right'
                elif event.key == pygame.K_UP and direction != 'down':
                    snake.speedy = -snake_block
                    snake.speedx = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN and direction != 'up':
                    snake.speedy = snake_block
                    snake.speedx = 0
                    direction = 'down'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False

            all_sprites.draw(screen)
            snake.tail(snake_block, snake_list)
            Your_score(dlinazmei - 1)
            pygame.display.update()

        if snake.rect.right >= WIDTH or snake.rect.left < 0 or snake.rect.bottom >= HEIGHT or snake.rect.top < 0:
            game_close = True
        all_sprites.draw(screen)
        snake_Head = [snake.rect.x, snake.rect.y]
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        if len(snake_list) > dlinazmei:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True
                proigrish.play()
        snake.tail(snake_block, snake_list)
        Your_score(dlinazmei - 1)
        pygame.display.update()

        collide = pygame.sprite.spritecollide(snake, apples, True)
        if collide:
            snake.tail(snake_block, snake_list)
            eaten_apples.add(collide[0])
            dlinazmei += 1
            eating.play()
            if b == 1:
                apple = Apple()
                all_sprites.add(apple)
                apples.add(apple)
            elif b == 2:
                apple = Apple()
                all_sprites.add(apple)
                apples.add(apple)
            elif b == 3:
                apple = Apple()
                all_sprites.add(apple)
                apples.add(apple)
            elif b == 4:
                b = random.randint(1, 3)
                apple = Apple()
                all_sprites.add(apple)
                apples.add(apple)
        clock.tick(snake_speed)

        apple = Apple()

        if pygame.sprite.spritecollideany(apple, tiles_group):
            # Если есть столкновение, выбираем новое место спавна для яблока
            apple.foodx = round(random.randrange(32, WIDTH - 2 * snake_block) / 32.0) * 32.0
            apple.foody = round(random.randrange(32, HEIGHT - 2 * snake_block) / 32.0) * 32.0

        if pygame.sprite.spritecollideany(apple, player_group):
            apple.foodx = round(random.randrange(32, WIDTH - 2 * snake_block) / 32.0) * 32.0
            apple.foody = round(random.randrange(32, WIDTH - 2 * snake_block) / 32.0) * 32.0


        for apple in apples:
            if apple not in eaten_apples:
                all_sprites.draw(screen)
                apple.update()

        if collide_with_wall(player_group):
            game_close = True
            proigrish.play()

        pygame.display.flip()
        snake.update()
        apple.update()

    apples.empty()
    snake.update()

    pygame.quit()
    quit()


def start_screen():
    intro_text = ["                           Змейка", "",
                  "Правила игры:",
                  "Собирайте фрукты, а также",
                  "старайтесь не сталкиваться",
                  "со стенами и своим хвостом.",
                  "Для начала зайди в настройки,",
                  "а потом выбирай уровень!"]
    fon = pygame.transform.scale(load_image('zmeika1.jpeg'), (WIDTH, HEIGHT))
    screen.fill(0)
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("comicsansms", 30)
    font2 = pygame.font.SysFont("comicsansms", 20)
    text_coord = 50
    global selected_level
    selected_level = None
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += 20
        screen.blit(string_rendered, intro_rect)
    level_buttons = []
    level_names = ["Уровень 1", "Уровень 2", "Уровень 3"]
    level_button_width = 150
    level_button_height = 30
    level_button_color = (red)
    level_button_x = WIDTH // 1.2 - level_button_width // 2
    level_button_y = HEIGHT // 7

    button_width = 100
    button_height = 50
    button_x = WIDTH // 10 - button_width // 2
    button_y = HEIGHT // 100000 + button_height // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    pygame.draw.rect(screen, red, button_rect)

    font3 = pygame.font.SysFont("comicsansms", 15)
    text = font3.render("Настройки", True, white)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    for i, level_name in enumerate(level_names):
        level_button_rect = pygame.Rect(level_button_x, level_button_y + i * 40, level_button_width,
                                        level_button_height)
        level_buttons.append(level_button_rect)

    while selected_level is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем, была ли нажата кнопка выбора карты
                for i, level_button_rect in enumerate(level_buttons):
                    if level_button_rect.collidepoint(event.pos):
                        # Здесь можно добавить логику для выбора карты и уровня
                        selected_level = level_names[i]
                        next_level(selected_level)
                        screen.fill(black)
                        global game_over, game_close
                        game_over = False
                        game_close = False
                        break
                if button_rect.collidepoint(event.pos):
                    show_settings()

        # Отрисовываем кнопки выбора карты на экране
        for i, level_button_rect in enumerate(level_buttons):
            pygame.draw.rect(screen, level_button_color, level_button_rect)
            level_text_surface = font2.render(level_names[i], True, pygame.Color('white'))
            level_text_rect = level_text_surface.get_rect(center=level_button_rect.center)
            screen.blit(level_text_surface, level_text_rect)
        pygame.display.flip()
        clock.tick(FPS)

    return selected_level
    next_level()
    gameLoop()

tile_width = tile_height = 32


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'empty':
            trava_group.add(self)
        else:
            tiles_group.add(self)


def collide_with_wall(player_group):
    for player in player_group:
        if pygame.sprite.spritecollideany(player, tiles_group):
            proigrish.play()
            return True
    return False

game_over = False

start_screen()
next_level()
gameLoop()