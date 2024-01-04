import pygame
import sys
import os
import math
import sqlite3


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def check_click_account_window(pos):
    x, y = pos
    if 841 <= x <= 841 + 46 and 138 <= y <= 138 + 46:
        return "close"
    elif 585 <= x <= 585 + 46 and 449 <= y <= 449 + 46:
        return "enter from account"


def start_button(screen, event):  # кнопка старта игры
    button_radius = 50
    button_x, button_y = 60, 60
    button_color = (239, 215, 90)
    angle_a = 0
    angle_b = (2 / 3) * math.pi
    angle_c = (4 / 3) * math.pi
    point_a = (
        button_x + int(button_radius * math.cos(angle_a)),
        button_y + int(button_radius * math.sin(angle_a))
    )
    point_b = (
        button_x + int(button_radius * math.cos(angle_b)),
        button_y + int(button_radius * math.sin(angle_b))
    )
    point_c = (
        button_x + int(button_radius * math.cos(angle_c)),
        button_y + int(button_radius * math.sin(angle_c))
    )
    pygame.draw.circle(screen, button_color, (button_x, button_y), button_radius)
    pygame.draw.polygon(screen, (90, 100, 45), (point_a, point_b, point_c))


def account_button(screen, event):  # кнопка аккаунта
    button_radius = 50
    button_pos = button_x, button_y = 940, 60
    font = pygame.font.Font(None, 60)
    pygame.draw.circle(screen, (255, 0, 0), button_pos, button_radius)
    letter_surface = font.render("A", True, (255, 255, 255))
    letter_rect = letter_surface.get_rect(center=button_pos)
    screen.blit(letter_surface, letter_rect)


def main_window(screen, n, a):
    screen.blit(a[n % 17], (0, 300))
    
def check_click_main_window(pos):
    mouse_x, mouse_y = pos
    # проверка на нажатие кнопки аккаунта
    button_radius = 50
    button_pos = button_x, button_y = 940, 60
    distance = ((mouse_x - button_x) ** 2 + (mouse_y - button_y) ** 2) ** 0.5
    if distance <= button_radius:
        return "аккаунт"
    # проверка на нажатие кнопки старта
    button_radius = 50
    button_x, button_y = 60, 60
    distance = ((mouse_x - button_x) ** 2 + (mouse_y - button_y) ** 2) ** 0.5
    if distance <= button_radius:
        return "старт"   
    
# действие кнопки регистрации
def sign_up(name, password):
    con = sqlite3.connect("santa`s helper.db")
    names = list(con.cursor().execute("SELECT name FROM player"))
    names = [i[0] for i in names]
    if name in names:
        return "Этот никнейм уже занят"
    zapros = f"INSERT INTO player(name, password, level) VALUES('{name}', {password}, 1)"
    res = con.cursor().execute(zapros)
    con.commit()
    con.close()
    return "Успешная регистрация!"

# действие кнопки входа
def sign_in(name, password):
    con = sqlite3.connect("santa`s helper.db")
    zapros = f"SELECT password FROM player WHERE name='{name}'"
    res = list(con.cursor().execute(zapros))
    con.close()
    if not res:
        return "Такого аккаунта не существует"
    elif str(res[0][0]) == password:
        return "Успешная авторизация!"
    else:
        return "Неправильный логин или пароль"
    

def check_click_registration(pos):
    x, y = pos
    button = ""
    # проверка на попадание на кнопку с цифрой
    if 250 <= x <= 250 + 47 and 316 <= y <= 316 + 47:
        button = 1
    elif 314 <= x <= 314 + 47 and 316 <= y <= 316 + 47:
        button = 2
    elif 380 <= x <= 380 + 47 and 316 <= y <= 316 + 47:
        button = 3
    elif 250 <= x <= 250 + 47 and 377 <= y <= 377 + 47:
        button = 4
    elif 314 <= x <= 314 + 47 and 377 <= y <= 377 + 47:
        button = 5
    elif 380 <= x <= 380 + 47 and 377 <= y <= 377 + 47:
        button = 6
    elif 250 <= x <= 250 + 47 and 436 <= y <= 436 + 47:
        button = 7
    elif 314 <= x <= 314 + 47 and 436 <= y <= 436 + 47:
        button = 8
    elif 380 <= x <= 380 + 47 and 436 <= y <= 436 + 47:
        button = 9
    elif 314 <= x <= 314 + 47 and 498 <= y <= 498 + 47:
        button = 0
    elif 250 <= x <= 250 + 47 and 498 <= y <= 498 + 47:
        button = "del all"
    elif 380 <= x <= 380 + 47 and 498 <= y <= 498 + 47:
        button = "del one"
    # проверка на попадание на кнопку "ВОЙТИ"
    elif 497 <= x <= 497 + 275 and 317 <= y <= 317 + 80:
        button = "sign_in"
    # проверка на попадание на кнопку "Зарегистрироваться"
    elif 497 <= x <= 497 + 275 and 414 <= y <= 414 + 80:
        button = "sign_up"
    # проверка на попадание на кнопку закрытия
    elif 750 <= x <= 750 + 55 and 151 <= y <= 151 + 55:
        button = "close_registration_window"
    return button
    
        
def registration_window(screen, reg_window):
    screen.blit(reg_window, (137, 120))
    
def game():
    pygame.init()
    size = 1000, 700
    background_image = pygame.image.load("start_window.png")    
    screen = pygame.display.set_mode(size)
    running = True
    # шрифт
    font = pygame.font.Font(None, 45)
    gif_deer = []
    for n in range(17):
        image = pygame.transform.scale(load_image(f"gif{n}.webp"), (400, 400))
        gif_deer.append(image)
    reg_window = pygame.image.load("registration_window.png") # фон окна регистрации
    account_window = pygame.image.load("account.png") # фон окна аккаунта
    account = None # никто не зашёл в аккаунт
    n = 0
    nick_name = ""
    password = ""
    text_in = ""
    text_up = ""
    flag_registration_window = True
    flag_main_window = True
    flag_account_window = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # если открыто окно регистрации
                if flag_registration_window:
                    button = str(check_click_registration(event.pos))
                    if button == "close_registration_window":
                        flag_registration_window = False
                        nick_name = ""
                        password = ""
                        text_in = ""
                        text_up = ""                        
                    elif button.isdigit():
                        if len(password) < 4:
                            password += button
                    elif button == "del one":
                        password = password[:-1]
                    elif button == "del all":
                        password = ""
                    elif button == "sign_in":
                        font1 = pygame.font.Font(None, 30)
                        text = sign_in(nick_name, password)
                        if text != "Успешная авторизация!":
                            text_in = font1.render(text, 1, (128, 64, 21))
                        else:
                            flag_registration_window = False
                            flag_account_window = True
                    elif button == "sign_up":
                        font1 = pygame.font.Font(None, 30)
                        text = sign_up(nick_name, password)
                        if text != "Успешная регистрация!":
                            text_up = font1.render(text, 1, (128, 64, 21))
                        else:
                            flag_registration_window = False
                            flag_account_window = True
                # если открыто окно старта
                if flag_main_window:
                    button = check_click_main_window(event.pos)
                    if button == "старт":
                        pass # реализация старта, проверки на вход в аккаунт
                    elif button == "аккаунт":
                        flag_registration_window = True # нужна проверка на вход в аккаунт, чтобы заново не выходить/входить
                if flag_account_window:
                    button = check_click_account_window(event.pos)
                    if button == "close":
                        flag_account_window = False
                    elif button == "enter from account":
                        flag_account_window = False
                        flag_registration_window = True
            elif event.type == pygame.KEYDOWN and flag_registration_window:
                if event.key == pygame.K_BACKSPACE:
                    nick_name = nick_name[:-1]
                else:
                    simbol = event.unicode
                    if simbol.isdigit() or simbol.isalpha() and len(nick_name) < 29:
                        nick_name += simbol
        n += 1
        screen.blit(background_image, (0, 0))
        start_button(screen, event)
        account_button(screen, event)        
        main_window(screen, n, gif_deer)
        # если открыто окно регистрации
        if flag_registration_window:
            registration_window(screen, reg_window)
            text = font.render(nick_name, 1, (128, 64, 21))
            screen.blit(text, (336, 210))
            text_pas = font.render("*" * len(password), 1, (128, 64, 21))
            screen.blit(text_pas, (305, 275))
            # вывод о входе
            if text_in:
                pygame.draw.rect(screen, (255, 200, 168), (481, 526, 317, 30))
                screen.blit(text_in, (483, 528))
            # вывод о регистрации
            if text_up:
                pygame.draw.rect(screen, (255, 200, 168), (481, 526, 317, 30))
                screen.blit(text_up, (483, 528))
        # если открыто окно аккаунта
        if flag_account_window:
            screen.blit(account_window, (558, 116))
            # нарисовать аватвр игрока(залить цветом круг и поставитьт букву)
            
        clock.tick(20)
        pygame.display.update()
    pygame.quit()    
    
game()
    
    