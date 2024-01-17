import pygame
import sys
import os
import math
import sqlite3
import random


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


def plus_stars(k, stars, special):
    k *= 100
    s = 0
    if k >= 90:
        s = 3
    elif k >= 70:
        s = 2
    elif k >= 50:
        s = 1
    if special:
        s *= 2
    return stars + s


def check_form_gift(right_components, all_components):
    c = 0
    for i in all_components:
        if i in right_components:
            c += 1
    if len(all_components):
        return c / len(all_components)
    return 0


def render_phrase(phrase):
    phrase = phrase.split()
    new_phrase = {}
    stroka = ""
    x = 570
    y = 170
    for word in phrase:
        if len(stroka + " " + word) < 25:
            stroka += " " + word
        else:
            new_phrase[x, y] = stroka
            stroka = word
            y += 25
    new_phrase[x, y] = stroka
    return new_phrase


def add_excess_component_to_gift(button, pos, checkbox_dont, checkboxes, components, dict_excess_components):
    position = pos
    position2 = pos[0] + 90, pos[1]
    image = pygame.transform.scale(load_image(f"{button}.png"), (70, 70))
    excess_component = Component(image, image, position)
    excess_checkbox = CheckBox(checkbox_dont, checkbox_dont, position2)
    checkboxes.add(excess_checkbox)
    components.add(excess_component)
    dict_excess_components[position2] = [excess_component, excess_checkbox, button]
    return (checkboxes, components, dict_excess_components)


def search_for_free_place(comps, dict_excess_components):
    for i in range(len(comps), 14):
        if i < 7:
            pos = 0, 85 + i * 79
            pos2 = 90, 85 + i * 79
        else:
            pos = 170, 85 + (i - 7) * 79
            pos2 = 260, 85 + (i - 7) * 79
        if pos2 not in dict_excess_components:
            return pos


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


def start_again(account):
    nickname = account[0]
    con = sqlite3.connect("santa_s_helper.db")
    con.cursor().execute(f"UPDATE player SET level = 1 WHERE name = '{nickname}'")
    con.cursor().execute(f"UPDATE player SET stars = 0 WHERE name = '{nickname}'")
    con.commit()
    con.close()


def load_level(level):  # функция загрузки уровня по числу уровня
    con = sqlite3.connect("santa_s_helper.db")
    level = list(con.cursor().execute(f"SELECT * FROM client WHERE level={level}").fetchall())
    con.close()
    level = list(sorted(level, key=lambda x: x[1]))
    return level  # возвращает список клиентов, которые приходят за уровень


def load_list_image_load(n):
    list_image = []
    if n == 0:
        for i in range(16):
            image = pygame.transform.scale(pygame.image.load(f"{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 1:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"all{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 2:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"cat{i}.jpg"), (600, 600))
            list_image.append(image)
    elif n == 3:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"cattree{i}.jpg"), (500, 626))
            list_image.append(image)
    elif n == 4:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"chtree{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 5:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"cook{i}.gif"), (500, 626))
            list_image.append(image)
    elif n == 6:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"cookie{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 7:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"eat{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 8:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"faerplace{i}.gif"), (600, 600))
            list_image.append(image)
    elif n == 9:
        for i in range(1, 5):
            image = pygame.transform.scale(pygame.image.load(f"night{i}.gif"), (600, 600))
            list_image.append(image)
    return list_image


def load_receipt(comps, checkbox_uncheck, checkbox_check):
    comps_ch = [i + ".png" for i in comps]
    comps_un = [i + "un.png" for i in comps]
    comps_ch = [pygame.transform.scale(load_image(i), (70, 70)) for i in comps_ch]
    comps_un = [pygame.transform.scale(pygame.image.load(i), (70, 70)) for i in comps_un]
    checkboxes = pygame.sprite.Group()
    components = pygame.sprite.Group()
    y = 90
    dict_comps_and_checks = {}
    for i in range(len(comps)):
        if i < 7:
            pos = 0, y + i * 79
            pos2 = 90, y + i * 79
        else:
            pos = 170, y + (i - 7) * 79
            pos2 = 260, y + (i - 7) * 79
        component = Component(comps_ch[i], comps_un[i], pos)
        components.add(component)
        checkbox = CheckBox(checkbox_uncheck, checkbox_check, pos2)
        checkboxes.add(checkbox)
        dict_comps_and_checks[comps[i]] = [component, checkbox]
    return (components, checkboxes, dict_comps_and_checks, pos)


def load_finish_gif():
    finish_gif = []
    for i in range(1, 221):
        fullname = os.path.join('final gif', f"finish gif ({i}).gif")
        image = pygame.image.load(fullname)
        finish_gif.append(image)
    return finish_gif


def load_gif_dark():
    gif_darkness = []
    for i in range(1, 11):
        dark = pygame.image.load(f"dark{i}.png")
        gif_darkness.append(dark)
    for i in range(1, 19):
        image = pygame.transform.scale(pygame.image.load(f"tree{i}.jpg"), (1000, 700))
        gif_darkness.append(image)
    return gif_darkness


def load_gif_gift():
    gif_gift = []
    for i in range(6):
        gift = pygame.transform.scale(pygame.image.load(f"data\cat{i}.gif"), (500, 607))
        gif_gift.append(gift)
    return gif_gift


def load_gif_santa():
    gif_santa = []
    for i in range(44):
        santa = pygame.image.load(f"s{i}.gif")
        gif_santa.append(santa)
    return gif_santa


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
        elem = "игрушка"
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
        elem = "сладости"
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


def check_click_finish_window(pos):
    x, y = pos
    if 361 <= x <= 361 + 119 and 505 <= y <= 505 + 74:
        return "again"
    elif 531 <= x <= 531 + 119 and 505 <= y <= 505 + 74:
        return "next"


def check_click_main_window(pos):
    mouse_x, mouse_y = pos
    # проверка на нажатие кнопки аккаунта
    button_radius = 50
    button_x, button_y = 940, 60
    distance = ((mouse_x - button_x) ** 2 + (mouse_y - button_y) ** 2) ** 0.5
    if distance <= button_radius:
        return "аккаунт"
    # проверка на нажатие кнопки старта
    button_radius = 50
    button_x, button_y = 60, 60
    distance = ((mouse_x - button_x) ** 2 + (mouse_y - button_y) ** 2) ** 0.5
    if distance <= button_radius:
        return "старт"


def level_up(account, stars):
    con = sqlite3.connect("santa_s_helper.db")
    con.cursor().execute(f"UPDATE player SET level = level + 1 WHERE name = '{account[0]}'")
    con.cursor().execute(f"UPDATE player SET stars = {stars} WHERE name = '{account[0]}'")
    con.commit()
    con.close()


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
            con.cursor().execute(zapros)
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


def check_click_finish_game_window(pos):
    x, y = pos
    if 158 <= x <= 158 + 238 and 614 <= y <= 614 + 54:
        return "again"
    elif 612 <= x <= 612 + 238 and 614 <= y <= 614 + 54:
        return "over"


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
    load_window = pygame.image.load("load_window.png")
    dialog = pygame.image.load("big_dialog.png")
    receipt = pygame.image.load("receipt.png")  # картинка чека
    checkbox_check = pygame.transform.scale(pygame.image.load("check.png"), (70, 70))  # картинка чекбокса с галочкой
    checkbox_uncheck = pygame.transform.scale(pygame.image.load("uncheck.png"), (70, 70))  # картинка пустого чекбокса
    checkbox_dont = pygame.transform.scale(pygame.image.load("dont.png"), (70, 70))  # картинка чекбокса с крестиком
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Santa`s helper")
    pygame.display.set_icon(pygame.image.load("santa.bmp"))
    screen.blit(background_image, (0, 0))
    running = True
    level_duration = 360000
    all_components = ["мыло", "шоколадка", "носки", "варежки", "подушка", "кружка", "шапка", "свитер", "игрушка",
                      "календарь", "плед", "сладости", "леденец", "блокнот"]
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
    pygame.mixer.music.load("main theme.mp3")
    pygame.mixer.music.play(-1)
    sound_wrong = pygame.mixer.Sound("wrong_choice.mp3")
    sound_right = pygame.mixer.Sound("right_choice.mp3")
    start_sound = pygame.mixer.Sound("start_sound.mp3")
    sound_get_stars = pygame.mixer.Sound("sound_get_stars.mp3")
    sound_door_bell = pygame.mixer.Sound("door_bell.mp3")
    sound_fall = pygame.mixer.Sound("sound_fall.mp3")
    reg_window = pygame.image.load("registration_window.png")  # фон окна регистрации
    account_window = pygame.image.load("account.png")  # фон окна аккаунта
    assambley_window = pygame.image.load("assambley window.png")
    finish_window = pygame.image.load("finish window.png")
    day_over_window = pygame.image.load("day over.png")
    finish_background = pygame.image.load("finish background.png")
    font_message = pygame.font.Font(None, 36)
    flag_phrase = True  # флаг для единичной загрузки сообщения персонажа
    flag_phraseWHAT = False
    text_message = ""
    k = 0
    d = True
    flag_give_away = False
    gifts = []  # список изображений подарков(коробок)
    for i in range(1, 8):
        gift = pygame.image.load(f"present{i}.png")
        gifts.append(gift)
    image_width, image_height = 150, 150  # параметры картинки подарка
    image_x = 330
    image_y = 543
    moving = False

    gif_santa = load_gif_santa()
    gif_darkness = load_gif_dark()
    gif_gift = load_gif_gift()
    finish_gif = load_finish_gif()

    account = None  # никто не зашёл в аккаунт
    n = 0
    falling_image = ""  # падающий в подарок компонент подарка
    nick_name = ""
    password = ""
    text_in = ""
    text_up = ""
    flag_give_away = False  # флаг отдачи подарка клиенту (для движения подарка)
    flag_view = False  # флаг отзыва клиента
    flag_registration_window = False  # флаг окна регистрации
    flag_main_window = True  # флаг стартового окна
    flag_account_window = False  # флаг окна аккаунта
    flag_shop_window = False  # флаг окна прилавка
    flag_assambley_window = False  # флаг окна сборки подарка
    flag_character = False  # флаг персонажа-покупателя
    flag_finish_day = False  # флаг для показа окна окончания дня/уровня
    flag_load_darkness = False  # флаг потемнения, наступления ночи
    flag_wrapping_gift = False  # флаг гифки с запаковыванием подарка
    flag_finish_game = False
    darkness = 0  # счётчик картинки, отвечающей за наступление темноты
    count_gif_gift = 0  # счётчик картинки, отвечающей за запаковку подарку
    gif_x = 0  # нужно для отрисовки загрузки
    count_people = 0  # количество людей, пришедших на уровне
    flag_load = False
    EVENT_GETTING_DARK = pygame.USEREVENT + 1
    DELAY_GETTING_DARK = 200

    EVENT_WRAPPING_GIFT = pygame.USEREVENT + 1
    DELAY_WRAPPING_GIFT = 100

    EVENT_LOAD = pygame.USEREVENT + 1
    DELAY_LOAD = 25

    EVENT_FINISH_GAME = pygame.USEREVENT + 1
    DELAY_FINISH_GAME = 100
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENT_GETTING_DARK and flag_load_darkness:
                screen.blit(gif_darkness[darkness], (0, 0))
                if darkness + 1 < 28:
                    if darkness < 10:
                        stars_for_shop_window(screen, stars)
                    darkness += 1
                else:
                    flag_load_darkness = False
                    darkness = 0
                    flag_finish_day = True
                    pygame.time.set_timer(EVENT_GETTING_DARK, 0)
            elif event.type == EVENT_WRAPPING_GIFT and flag_wrapping_gift:
                # gif запаковки подарка
                screen.blit(load_window, (0, 0))
                wrapping = gif_gift[count_gif_gift % 6]
                wrap_rect = wrapping.get_rect()
                wrap_rect.center = (500, 350)
                screen.blit(wrapping, wrap_rect)
                if count_gif_gift + 1 == len(gif_gift) * 4:
                    flag_wrapping_gift = False
                    flag_give_away = True
                    image_width, image_height = 150, 150  # параметры картинки подарка
                    image_x = 330
                    image_y = 543
                    moving = False
                    flag_shop_window = True
                    flag_character = True
                    d = True
                    count_gif_gift = 0
                else:
                    count_gif_gift += 1
            elif event.type == EVENT_LOAD and flag_load:
                screen.blit(load_window, (0, 0))
                gif_load_image = list_load_image[n % len(list_load_image)]
                gif_rect = gif_load_image.get_rect()
                gif_rect.center = (500, 350)
                screen.blit(gif_load_image, gif_rect)
                start_sound.play()
                if gif_x < 352:
                    gif_x += 2
                    pygame.draw.rect(screen, (128, 64, 32), (320, 600, 360, 50), 4)
                    pygame.draw.rect(screen, (255, 192, 203), (324, 604, gif_x, 42))
                    flag_registration_window = False
                    flag_main_window = False
                    flag_account_window = False
                elif list_load_image not in (gif_santa,):
                    flag_load = False
                    flag_assambley_window = True
                    gif_x = 0
                else:
                    flag_load = False
                    flag_shop_window = True
                    level_started = True
                    account, color = account_maker(nick_name)
                    nick_name, password, level, stars = account
                    password = str(password)
                    count_people = 0
                    gif_x = 0
            elif event.type == EVENT_FINISH_GAME and flag_finish_game:
                screen.blit(finish_background, (0, 0))
                screen.blit(finish_gif[count_finish_picture], (100, 13))
                if count_finish_picture < 219:
                    count_finish_picture += 1
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
                        flag_load = True  # реализация старта, проверки на вход в аккаунт
                        pygame.time.set_timer(EVENT_LOAD, DELAY_LOAD)
                        list_load_image = gif_santa
                    elif button == "аккаунт":
                        if not account:
                            flag_registration_window = True
                        else:
                            flag_account_window = True
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
                        flag_wrapping_gift = True
                        pygame.time.set_timer(EVENT_WRAPPING_GIFT, DELAY_WRAPPING_GIFT)
                    elif button in dict_comps_and_checks and button not in components_in_gift:
                        falling_image = load_image(button + ".png")
                        x, y = 540, 0
                        dict_comps_and_checks[button][0].checked = True
                        dict_comps_and_checks[button][1].checked_checkbox = True
                        components_in_gift.append(button)
                    elif button not in components_in_gift and button:
                        falling_image = load_image(button + ".png")
                        x, y = 540, 0
                        pos = search_for_free_place(comps, dict_excess_components)
                        checkboxes, components, dict_excess_components = add_excess_component_to_gift(button, pos,
                                                                              checkbox_dont,
                                                                              checkboxes,
                                                                              components,
                                                                              dict_excess_components)
                        components_in_gift.append(button)
                    else:
                        for pos in dict_excess_components:
                            if pos[0] <= event.pos[0] <= pos[0] + 70 and pos[1] <= event.pos[1] <= pos[1] + 70:
                                dict_excess_components[pos][0].kill()
                                dict_excess_components[pos][1].kill()
                                del components_in_gift[components_in_gift.index(dict_excess_components[pos][2])]
                                del dict_excess_components[pos]
                                break
                if flag_shop_window:
                    if flag_give_away:
                        if event.button == 1:
                            if image_x <= event.pos[0] <= image_x + image_width and\
                            image_y <= event.pos[1] <= image_y + image_height:
                                moving = True
                if flag_finish_day:
                    button = check_click_finish_window(event.pos)
                    if button == "again":
                        flag_finish_day = False
                        flag_load = True
                        list_load_image = gif_santa
                        stars = account[-1]
                        pygame.time.set_timer(EVENT_LOAD, DELAY_LOAD)
                    elif button == "next":
                        level_up(account, stars)  # функция с повышением уровня и занесением в бд
                        flag_main_window = True
                        flag_finish_day = False
                        level += 1
                if flag_finish_game:
                    button = check_click_finish_game_window(event.pos)
                    if button == "again":
                        start_again(account)
                        flag_finish_game = False
                        flag_main_window = True
                        pygame.time.set_timer(EVENT_FINISH_GAME, 0)
                    elif button == "over":
                        # реализовать окончание игры (при нажатии кнопки старта запускается последний день)
                        flag_finish_game = False
                        flag_main_window = True
                        pygame.time.set_timer(EVENT_FINISH_GAME, 0)
            elif event.type == pygame.KEYDOWN and flag_registration_window:
                if event.key == pygame.K_BACKSPACE:
                    nick_name = nick_name[:-1]
                else:
                    simbol = event.unicode
                    if simbol.isdigit() or simbol.isalpha() and len(nick_name) < 29:
                        nick_name += simbol
            elif event.type == pygame.MOUSEBUTTONUP and flag_give_away:
                if event.button == 1:
                    moving = False
            elif event.type == pygame.MOUSEMOTION and flag_give_away:
                if moving:
                    offset_x = event.rel[0]
                    offset_y = event.rel[1]
                    image_x += offset_x
                    image_y += offset_y
        n += 1
        if flag_main_window:
            screen.blit(background_image, (0, 0))
            start_button(screen)
            name(screen)
            if account is None:
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
            screen.blit(nick, (661, 305))
            str_stars = font1.render(str(stars), 1, (128, 64, 21))
            screen.blit(str_stars, (717, 410))
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
                level_started = True
                flag_character = False
                flag_load_darkness = True
                pygame.time.set_timer(EVENT_GETTING_DARK, DELAY_GETTING_DARK)
            gift_rect = pygame.Rect(image_x, image_y, 150, 150)
            client_rect = pygame.Rect(284, 167, 298, 364)
            if gift_rect.colliderect(client_rect) and not moving and flag_give_away:
                flag_give_away = False
                k = check_form_gift(comps, components_in_gift)
                if k >= 0.8:
                    phrase = render_phrase(client[8])
                    sound_right.play()
                else:
                    phrase = render_phrase(client[9])
                    character_image = load_image(client[7], -1)
                    sound_wrong.play()
                flag_view = True
                text_message = ""
        if flag_character:
            client = load_level(level)[count_people]
            if flag_phrase:
                sound_door_bell.play()
                character_image = load_image(client[6], -1)
                phrase = render_phrase(client[2])
                phraseWHAT = client[3]
                flag_phrase = False
                count_strok = 0
                text_character = []
            keys_phrase = list(phrase.keys())
            appearence_person(screen, character_image, dialog)
            if phrase[keys_phrase[count_strok]]:
                text_message += phrase[keys_phrase[count_strok]][0]
                phrase[keys_phrase[count_strok]] = phrase[keys_phrase[count_strok]][1:]
            elif count_strok < len(keys_phrase) - 1:
                text_character.append((keys_phrase[count_strok], text_message))
                text_message = ""
                count_strok += 1
            for t in text_character:
                t1 = font_message.render(t[1], True, (164, 64, 21))
                screen.blit(t1, t[0])
            txt = font_message.render(text_message, True, (164, 64, 21))
            screen.blit(txt, (keys_phrase[count_strok]))
            if phraseWHAT is not None:
                button_OK(screen)
                button_what(screen)
                button = check_buttons_window2(event)
                if button == "Что?" and not flag_view:
                    phrase = render_phrase(phraseWHAT)
                    text_character = []
                    count_strok = 0
                    text_message = ""
                elif button == "ОК" and not flag_view and not flag_give_away:
                    if level == 7:
                        flag_finish_game = True
                        count_finish_picture = 0
                        falling_image = False
                        flag_character = False
                        flag_shop_window = False
                        pygame.time.set_timer(EVENT_FINISH_GAME, DELAY_FINISH_GAME)
                    else:
                        flag_load = True
                        phrase = render_phrase("...")
                        text_character = []
                        count_strok = 0
                        text_message = ""
                        list_load_image = load_list_image_load(random.randrange(10))
                        pygame.time.set_timer(EVENT_LOAD, DELAY_LOAD)
                        falling_image = False
                        flag_character = False
                        flag_shop_window = False
                elif flag_view and button == "ОК":
                    count_people += 1
                    if count_people == 6:
                        # ОСТОРОЖНО
                        flag_load_darkness = True
                        flag_character = False
                        flag_shop_window = False
                    event.pos = 0, 0
                    flag_view = False
                    flag_phrase = True
                    text_message = ""
                    stars = plus_stars(k, stars, client[5])
                    sound_get_stars.play()
            else:
                button_OK(screen)
                button = check_buttons_window2(event)
                event.pos = (0, 0)
                if button == "ОК":
                    count_people += 1
                    text_message = ""
                    flag_phrase = True
            if flag_give_away:
                screen.blit(gift_image, (image_x, image_y))
        if flag_assambley_window:
            screen.blit(assambley_window, (0, 0))
            game_level = load_level(
                level)  # в game_level лежит не числовое значение уровня, а список приходящих клиентов
            if d:
                gift_image = gifts[random.randrange(7)]
                checkboxes = pygame.sprite.Group()
                components = pygame.sprite.Group()
                dict_excess_components = {}
                components_in_gift = []
                comps = game_level[count_people][4]
                if comps is not None:
                    comps = comps.split()
                    if comps[0] == "all":
                        comps = all_components
                    components, checkboxes, dict_comps_and_checks, last_pos = load_receipt(comps, checkbox_uncheck,
                                                                                           checkbox_check)
                    d = False
                else:
                    n += 1
            if falling_image:
                sound_fall.play()
                rect = falling_image.get_rect()
                y += 20
                if rect.height > 360 - y > 0:
                    rect = pygame.Rect(0, 0, rect.width, (360 - y))
                    crop = falling_image.subsurface(rect)
                    screen.blit(crop, (x, y))
                elif y < 360:
                    screen.blit(falling_image, (x, y))
                else:
                    falling_image = False
            current_time = pygame.time.get_ticks()
            time = current_time - start_time
            clock_time = usual_clock(time)
            font_clock = pygame.font.Font(None, 34)
            clock_time = font_clock.render(clock_time, 1, (164, 64, 21))
            screen.blit(clock_time, (340, 15))
            screen.blit(receipt, (0, 0))
            checkboxes.update()
            components.update()
            checkboxes.draw(screen)
            components.draw(screen)
        if flag_finish_day:
            screen.blit(finish_window, (0, 0))
            screen.blit(day_over_window, (300, 100))
            font_score = pygame.font.Font(None, 42)
            delta_stars = font_score.render(str(stars - account[-1]), True, (128, 64, 21))
            delta_stars_rect = delta_stars.get_rect()
            delta_stars_rect.center = (500, 460)
            screen.blit(delta_stars, delta_stars_rect)
        clock.tick(20)
        pygame.display.update()
    pygame.quit()


pygame.mixer.pre_init(44100, -16, 1, 512)
game() 