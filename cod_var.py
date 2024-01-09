import pygame
import sys
import os
import sqlite3
GRAVITY = 1

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
    
def making_receipt(stroka):
    spisok = stroka.split()
    for elem in spisok:
        image = pygame.image.load(elem + ".png")
        
def load_level(level):
    con = sqlite3.connect("santa_s_helper.db")
    level = list(con.cursor().execute(f"SELECT * FROM client WHERE level={level}").fetchall())
    con.close()
    return level

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
            pos2 = 250, y + (i - 7) * 79
        component = Component(comps_ch[i], comps_un[i], pos)
        components.add(component)
        checkbox = CheckBox(checkbox_uncheck, checkbox_check, pos2)
        checkboxes.add(checkbox)   
        dict_comps_and_checks[comps[i]] = [component, checkbox]
    return (components, checkboxes, dict_comps_and_checks, pos)
    

def game():
    pygame.init()
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    comps = ["мыло", "шоколадка", "носки", "варежки", "подушка", "кружка", "шапка", "свитер", "игрушка", "календарь", "плед", "сладости", "леденец", "блокнот"]
    chcomps = [i + ".png" for i in comps]
    uncomps = [i + "un" + ".png" for i in comps]
    level = load_level(6)
    n = 4
    components_in_gift = []
    receipt = pygame.image.load("receipt.png")
    checkbox_check = pygame.transform.scale(pygame.image.load("check.png"), (70, 70))
    checkbox_uncheck = pygame.transform.scale(pygame.image.load("uncheck.png"), (70, 70))
    checkbox_dont = pygame.transform.scale(pygame.image.load("dont.png"), (70, 70))
    comps_ch = [pygame.transform.scale(load_image(i), (70, 70)) for i in chcomps]
    comps_un = [pygame.transform.scale(pygame.image.load(i), (70, 70)) for i in uncomps]
    all_components = ["мыло", "шоколадка", "носки", "варежки", "подушка", "кружка", "шапка", "свитер", "игрушка",
                      "календарь", "плед", "сладости", "леденец", "блокнот"]
    checkboxes = pygame.sprite.Group()
    components = pygame.sprite.Group()
    dict_excess_components = {}
    
    clock = pygame.time.Clock()
    running = True
    d = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = return_elem(event.pos)
                if button in dict_comps_and_checks and button not in components_in_gift:
                    dict_comps_and_checks[button][0].checked = True
                    dict_comps_and_checks[button][1].checked_checkbox = True
                    components_in_gift.append(button)
                elif button not in components_in_gift and button:
                    pos = search_for_free_place(comps, dict_excess_components)
                    checkboxes, components, dict_excess_components = add_excess_component_to_gift(button, pos, checkbox_dont, checkboxes,
                                                                                                  components, dict_excess_components)
                    components_in_gift.append(button)
                else:
                    for pos in dict_excess_components:
                        if pos[0] <= event.pos[0] <= pos[0] + 70 and pos[1] <= event.pos[1] <= pos[1] + 70:
                            dict_excess_components[pos][0].kill()
                            dict_excess_components[pos][1].kill()
                            del components_in_gift[components_in_gift.index(dict_excess_components[pos][2])]
                            del dict_excess_components[pos]
                            break
                        
        screen.blit(pygame.image.load("c,jh.png"), (0, 0))
        if n < len(level) and d:
            comps = level[n][4]
            if comps != None:
                comps = comps.split()
                if comps[0] == "all":
                    comps = all_components
                components, checkboxes, dict_comps_and_checks, last_pos = load_receipt(comps, checkbox_uncheck, checkbox_check)
                d = False
            else:
                n += 1
        screen.blit(receipt, (0, 0))
        checkboxes.update()
        components.update()
        checkboxes.draw(screen)
        components.draw(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
game()