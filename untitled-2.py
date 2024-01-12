import pygame
import sys
import os
import math
import sqlite3
import random
import time


class CheckBox(pygame.sprite.Sprite):
    def __init__(self, unchecked_image, checked_image, pos):
        super().__init__()
        
        self.image_unchecked = unchecked_image
        self.image_checked = checked_image
        self.image = unchecked_image
        self.checked_checkbox = False
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        if self.checked_checkbox:
            self.image = self.image_checked
        else:
            self.image = self.image_unchecked
            
            
class Component(pygame.sprite.Sprite):
    def __init__(self, checked_image, unchecked_image, pos):
        super().__init__()
        
        self.image_checked = checked_image
        self.image_unchecked = unchecked_image
        self.image = self.image_unchecked
        self.checked = False
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    
    def update(self):
        if self.checked:
            self.image = self.image_checked
        else:
            self.image = self.image_unchecked


def render_phrase(phrase):
    phrase = phrase.split()
    new_phrase = ""
    stroka = ""
    for word in phrase:
        if len(stroka + " " + word) < 25:
            stroka += " " + word
        else:
            new_phrase += stroka + "\n"
            stroka = word
    return new_phrase + stroka
        
    
    
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
    
    
def load_level(level): # функция загрузки уровня по числу уровня
    con = sqlite3.connect("santa_s_helper.db")
    level = list(con.cursor().execute(f"SELECT * FROM client WHERE level={level}").fetchall())
    con.close()
    level = list(sorted(level, key=lambda x: x[1]))
    return level # возвращает список клиентов, которые приходят за уровень


def load_receipt(comps, checkbox_uncheck, checkbox_check): # функция, которая создаёт спрайты нужных в подарке компонентов
    checkboxes = pygame.sprite.Group()
    components = pygame.sprite.Group()   
    if comps == "all":
        comps = ["мыло", "шоколадка", "носки", "варежки",
                 "подушка", "кружка", "шапка", "свитер", "игрушка",
                 "календарь", "плед", "сладости", "леденец", "блокнот"]
    else:
        comps = comps.split()
    comps_ch = [i + ".png" for i in comps]
    comps_un = [i + "un.png" for i in comps]
    comps_ch = [pygame.transform.scale(load_image(i), (70, 70)) for i in comps_ch]
    # список изображений компонентов, которых положили в коробку
    comps_un = [pygame.transform.scale(pygame.image.load(i), (70, 70)) for i in comps_un]
    # список изображений компонентов, которых не положили в коробку
    y = 70
    x = 0
    for i in range(len(comps)):
        if i < 7:
            pos = x, y + i * 79
            pos2 = 90, y + i * 79
        else:
            pos = 170, y + (i - 7) * 79
            pos2 = 250, y + (i - 7) * 79
        component = Component(comps_ch[i], comps_un[i], pos)
        components.add(component) # группа спрайтов с компонентами
        checkbox = CheckBox(checkbox_uncheck, checkbox_check, pos2)
        checkboxes.add(checkbox)    # группа спрайтов с чекбоксами
    return (components, checkboxes)


def stars_for_shop_window(screen, stars):
    font2 = pygame.font.Font(None, 50)    
    stars = font2.render(str(stars), 2, (128, 64, 21))
    stars_rect = stars.get_rect()
    stars_rect.center = (950, 335)
    screen.blit(stars, stars_rect)
    
    
def return_elem(pos):
    x, y = pos
    elem = ""
    if 425 <= x <= 435 + 97 and 40 <= y <= 40 + 97:
        elem = "варежки"
    elif 549 <= x <= 549 + 97 and 40 <= y <= 40 + 97:
        elem = "дракон"
    elif 661 <= x <= 661 + 97 and 40 <= y <= 40 + 97:
        elem = "календарь"
    elif 777 <= x <= 777 + 97 and 40 <= y <= 40 + 97:
        elem = "носки"
    elif 890 <= x <= 890 + 97 and 40 <= y <= 40 + 97:
        elem = "шапка"
    elif 435 <= x <= 435 + 97 and 150 <= y <= 150 + 97:
        elem = "подушка"
    elif 549 <= x <= 549 + 97 and 150 <= y <= 150 + 97:
        elem = "блокнот"
    elif 661 <= x <= 661 + 97 and 150 <= y <= 150 + 97:
        elem = "леденец"
    elif 777 <= x <= 777 + 97 and 150 <= y <= 150 + 97:
        elem = "плед"
    elif 890 <= x <= 890 + 97 and 150 <= y <= 150 + 97:
        elem = "шоколадка"
    elif 784 <= x <= 784 + 97 and 263 <= y <= 263 + 97:
        elem = "набор сладостей"
    elif 893 <= x <= 893 + 97 and 263 <= y <= 263 + 97:
        elem = "мыло"
    elif 784 <= x <= 784 + 97 and 376 <= y <= 376 + 97:
        elem = "кружка"
    elif 893 <= x <= 893 + 97 and 376 <= y <= 376 + 97:
        elem = "свитер"
    elif 813 <= x <= 194 + 813 and 548 <= y <= 548 + 120:
        elem = "ВЫДАТЬ"
    return elem


def button_OK(screen):
    button_pos = (730, 380)
    font = pygame.font.Font(None, 45)
    rect_width, rect_height = 110, 80
    rect_x, rect_y = button_pos
    pygame.draw.rect(screen, (240, 200, 200), (rect_x, rect_y, rect_width, rect_height), border_radius=100)
    letter_surface = font.render("OK", True, (128, 64, 21))
    screen.blit(letter_surface, (760, 405))
    

def button_what(screen):
    button_pos = (730, 290)
    font = pygame.font.Font(None, 45)
    rect_width, rect_height = 110, 80
    rect_x, rect_y = button_pos
    pygame.draw.rect(screen, (240, 200, 200), (rect_x, rect_y, rect_width, rect_height), border_radius=100)
    letter_surface = font.render("Что?", True, (128, 64, 21))
    screen.blit(letter_surface, (750, 315))

def check_buttons_window2(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        m_x, m_y = event.pos
        rect_width, rect_height = 110, 80
        rect_x, rect_y = (730, 290)
        rect_x2, rect_y2 = (730, 380)
        if rect_x < m_x < rect_x + rect_width and rect_y < m_y < rect_y + rect_height:
            return "Что?"
        if rect_x2 < m_x < rect_x2 + rect_width and rect_y2 < m_y < rect_y2 + rect_height:
            return "ОК"


def appearence_person(screen, image, dialog):
    screen.blit(image, (284, 167))
    screen.blit(dialog, (560, 149))
    

def usual_clock(time):
    real_minutes = time / 60000 
    if real_minutes * 100 % 100 < 25 or 75 > real_minutes * 100 % 100 > 50:
        minutes = "00"
    else:
        minutes = "30"
    game_time = 10 + time * 2 // 60000
    time = str(game_time) + ":" + minutes
    return time
    
    
def name(screen):  # название игры
    title_font = pygame.font.Font("Roboto-BlackItalic.ttf", 48)
    subtitle_font = pygame.font.Font("Roboto-CondensedItalic.ttf", 34)
    title_text = title_font.render("Santa's Helper", True, (255, 0, 0))
    title_rect = title_text.get_rect()
    title_rect.center = (500, 100)
    screen.blit(title_text, title_rect)
    subtitle_text = subtitle_font.render("Merry Christmas!", True, (23, 100, 56))
    subtitle_rect = subtitle_text.get_rect()
    subtitle_rect.center = (490, 140)
    screen.blit(subtitle_text, subtitle_rect)


def check_click_account_window(pos):
    x, y = pos
    if 841 <= x <= 841 + 46 and 138 <= y <= 138 + 46:
        return "close"
    elif 585 <= x <= 585 + 46 and 449 <= y <= 449 + 46:
        return "enter from account"


def start_button(screen):  # кнопка старта игры
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


def account_button(screen, letter="A", color=(255, 0, 0)):  # кнопка аккаунта
    button_radius = 50
    button_pos = button_x, button_y = 940, 60
    font = pygame.font.Font(None, 60)
    pygame.draw.circle(screen, color, button_pos, button_radius)
    letter_surface = font.render(letter, True, (255, 255, 255))
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
    if name and password:
        if len(password) == 4:
            con = sqlite3.connect("santa_s_helper.db")
            names = list(con.cursor().execute("SELECT name FROM player"))
            names = [i[0] for i in names]
            if name in names:
                return "Этот никнейм уже занят"
            zapros = f"INSERT INTO player(name, password, level, stars) VALUES('{name}', {password}, 1, 0)"
            res = con.cursor().execute(zapros)
            con.commit()
            con.cursor().close()
            con.close()
            return "Успешная регистрация!"
        else:
            return "Пароль должен быть из 4 цифр"
    else:
        return "Введите логин и пароль"

# действие кнопки входа
def sign_in(name, password):
    if name and password:
        con = sqlite3.connect("santa_s_helper.db")
        zapros = f"SELECT password FROM player WHERE name='{name}'"
        res = list(con.cursor().execute(zapros))
        con.close()
        if not res:
            return "Такого аккаунта не существует"
        elif str(res[0][0]) == password:
            return "Успешная авторизация!"
        else:
            return "Неправильный логин или пароль"
    else:
        return "Введите логин и пароль"
    
def account_maker(name):
    con = sqlite3.connect("santa_s_helper.db")
    gamer = con.cursor().execute(f"SELECT * FROM player WHERE name='{name}'")
    color = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    return (list(gamer)[0], color)
    

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
    shop_image = pygame.image.load("прилавок.png")
    dialog = pygame.image.load("big_dialog.png")
    receipt = pygame.image.load("receipt.png") # картинка чека
    checkbox_check = pygame.transform.scale(pygame.image.load("check.png"), (70, 70)) # картинка чекбокса с галочкой
    checkbox_uncheck = pygame.transform.scale(pygame.image.load("uncheck.png"), (70, 70)) # картинка пустого чекбокса
    checkbox_dont = pygame.transform.scale(pygame.image.load("dont.png"), (70, 70)) # картинка чекбокса с крестиком
    screen = pygame.display.set_mode(size)
    running = True
    level_duration = 360000
    # шрифт
    font = pygame.font.Font(None, 45)
    gif_deer = []
    cats = []
    for n in range(17):
        image = pygame.transform.scale(load_image(f"gif{n}.webp"), (400, 400))
        gif_deer.append(image)
    for i in range(6):
        image = pygame.transform.scale(load_image(f"cat{i % 6}.gif"), (448, 544))
        cats.append(image)
    reg_window = pygame.image.load("registration_window.png") # фон окна регистрации
    account_window = pygame.image.load("account.png") # фон окна аккаунта
    assambley_window = pygame.image.load("assambley window.png")
    
    font_message = pygame.font.Font(None, 36)
    flag_phrase = True # флаг для единичной загрузки сообщения персонажа
    flag_phraseWHAT = False
    text_message = ""
    k = 0
    
    account = None # никто не зашёл в аккаунт
    n = 0
    nick_name = ""
    password = ""
    text_in = ""
    text_up = ""
    flag_registration_window = False # флаг окна регистрации
    flag_main_window = True # флаг стартового окна
    flag_account_window = False # флаг окна аккаунта
    flag_shop_window = False # флаг окна прилавка
    flag_assambley_window = False  # флаг окна сборки подарка
    flag_character = False # флаг персонажа-покупателя
    x = 0 # нужно для отрисовки загрузки
    count_people = 0 # количество людей пришедших на уровне
    flag_load = False
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
                        text_up = ""
                        if text != "Успешная авторизация!":
                            text_in = font1.render(text, 1, (128, 64, 21))
                        else:
                            flag_registration_window = False
                            flag_account_window = True
                            account, color = account_maker(nick_name)
                            nick_name, password, level, stars = account
                            password = str(password)
                    elif button == "sign_up":
                        font1 = pygame.font.Font(None, 30)
                        text = sign_up(nick_name, password)
                        text_in = ""
                        if text != "Успешная регистрация!":
                            text_up = font1.render(text, 1, (128, 64, 21))
                        else:
                            account, color = account_maker(nick_name)
                            nick_name, password, level, stars = account
                            password = str(password)
                            flag_registration_window = False
                            flag_account_window = True
                # если открыто окно старта
                if flag_main_window:
                    button = check_click_main_window(event.pos)
                    if button == "старт" and account:
                        flag_load = True # реализация старта, проверки на вход в аккаунт
                    elif button == "аккаунт":
                        if account == None:
                            flag_registration_window = True
                        else:
                            flag_account_window = True# нужна проверка на вход в аккаунт, чтобы заново не выходить/входить
                if flag_account_window:
                    button = check_click_account_window(event.pos)
                    if button == "close":
                        flag_account_window = False
                    elif button == "enter from account":
                        flag_account_window = False
                        flag_registration_window = True
                        account = None
                if flag_assambley_window:
                    button = return_elem(event.pos)
                    if button == "ВЫДАТЬ":
                        flag_assambley_window = False
                        flag_shop_window = True
                        flag_character = True
                        if count_people < 5:
                            count_people += 1
                        
            elif event.type == pygame.KEYDOWN and flag_registration_window:
                if event.key == pygame.K_BACKSPACE:
                    nick_name = nick_name[:-1]
                else:
                    simbol = event.unicode
                    if simbol.isdigit() or simbol.isalpha() and len(nick_name) < 29:
                        nick_name += simbol
        n += 1
        if flag_main_window:
            screen.blit(background_image, (0, 0))
            start_button(screen)
            name(screen)  
            if account == None:
                account_button(screen) 
            else:
                account_button(screen, nick_name[0], color)  
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
            pygame.draw.circle(screen, color, (662 + 71, 150 + 71), 69)
            font2 = pygame.font.Font(None, 130)
            letter = font2.render(nick_name[0], 10, (128, 64, 21))
            screen.blit(letter, (710, 173))
            nick = font1.render(nick_name, 1, (128, 64, 21))
            screen.blit(nick, (661,  305))
            str_stars = font1.render(str(stars), 1, (128, 64, 21))
            screen.blit(str_stars, (717, 410))
            # нарисовать аватар игрока(залить цветом круг и поставить букву)
        
        if flag_load:
            if x < 352:
                x += 2
                screen.fill((216, 191, 200))
                screen.blit(cats[n % 6], (276, 0))
                pygame.draw.rect(screen, (128, 64, 32), (320, 550, 360, 50), 4)
                pygame.draw.rect(screen, (255, 192, 203), (324, 554, x, 42))
                flag_registration_window = False
                flag_main_window = False
                flag_account_window = False
            else:
                flag_load = False
                flag_shop_window = True
                level_started = True
                x = 0
                
        if flag_shop_window:
            screen.blit(shop_image, (0, 0))
            flag_character = True
            if level_started:
                start_time = pygame.time.get_ticks()
                level_started = False
            current_time = pygame.time.get_ticks()
            time = current_time - start_time
            time_clock = usual_clock(time)
            font_time = pygame.font.Font(None, 23) 
            time_clock = font_time.render(time_clock, 2, (128, 64, 21))
            stars_for_shop_window(screen, stars)
            screen.blit(time_clock, (934, 94))          
            if time > level_duration:
                flag_shop_window = False
                flag_main_window = True
                level_started = True
                flag_character = False
        
        if flag_character:
            client = load_level(level)[count_people]
            character_image = load_image(client[6], -1)
            appearence_person(screen, character_image, dialog)
            if flag_phrase:
                phrase = render_phrase(client[2])
                phraseWHAT = client[3] 
                flag_phrase = False# реализация проверки на уровень, нахождение персонажа и его фраз из базы данных
            if phrase:
                text_message += phrase[0]
                phrase = phrase[1:]
                txt = font_message.render(text_message, True, (164, 64, 21))
            screen.blit(txt, (570, 170))  
            if phraseWHAT != None:
                button_OK(screen)
                button_what(screen)
                button = check_buttons_window2(event)
                if button == "Что?":
                    phrase = render_phrase(phraseWHAT)
                    flag_phraseWHAT = False
                    text_message = ""
                elif button == "ОК":
                    flag_phrase = True
                    text_message = ""
                    flag_assambley_window = True
                    flag_character = False
                    flag_shop_window = False
            else:
                button_OK(screen)
                button = check_buttons_window2(event)
                event.pos = (0, 0)
                if button == "ОК":
                    count_people += 1
                    text_message = ""
                    flag_phrase = True
        
        if flag_assambley_window:
            screen.blit(assambley_window, (0, 0))
            game_level = load_level(level) # в game_level лежит не числовое значение уровня, а список приходящих клиентов
            comps = game_level[count_people][4]
            components, checkboxes = load_receipt(comps, checkbox_uncheck, checkbox_check)
            current_time = pygame.time.get_ticks()
            time = current_time - start_time
            clock_time = usual_clock(time)
            font_clock = pygame.font.Font(None, 34)
            clock_time = font_clock.render(clock_time, 1, (164, 64, 21))
            screen.blit(clock_time, (310, 15))
            screen.blit(receipt, (0, 0))
            checkboxes.update()
            components.update()
            checkboxes.draw(screen)
            components.draw(screen)            
        clock.tick(20)
        pygame.display.update()
    pygame.quit()    
    
    
game() 