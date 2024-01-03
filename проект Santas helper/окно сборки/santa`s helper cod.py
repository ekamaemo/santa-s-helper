import pygame
import PIL.Image
import sys
import os


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


def main_window(screen, n):
    background_image = pygame.image.load("start_window.png")
    screen.blit(background_image, (0, 0))
    screen.blit(pygame.transform.scale(load_image(f"gif{n % 17}.webp"), (400, 400)), (0, 300))
    pygame.display.update()


def game():
    pygame.init()
    size = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    n = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        n += 1
        main_window(screen, n)
        clock.tick(20)
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()


game()
