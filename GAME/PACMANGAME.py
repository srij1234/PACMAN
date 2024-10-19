import pygame
import random
import time

pygame.init()
window_size = (500, 510)
r = window_size[0] / 25
d = 0.375 * r
screen = pygame.display.set_mode(window_size)
display = screen

pygame.display.set_caption("")
bg_color = (0, 0, 0)
pclr = (255, 255, 255)
player_size = (20, 20)
player_pos = [0, 0]
player_speed = window_size[0] / 1500
game_over = False
running = True

x = window_size[0] / 2
y = window_size[0] / 2
k = 0
nk = 1
t = 0


def eat(a, b, c, d):
    global k
    ka = (a - c) ** 2
    ba = (b - d) ** 2
    z = ka + ba
    z = z ** 0.5

    p = Point(a, b)
    sides = 3
    if z <= r and (not checkInside(polygon, sides, p)):
        k += 1


white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)


def genc():
    x, y =int(random.randint(r, window_size[0] - r)),int( random.randint(r, window_size[0] - r))
    return x, y


def rou(n):
    if (n // r) % 2 == 0:
        t = n % r
    else:
        t = r - n % r
    return t


def drawr(n):
    global t
    screen.fill(bg_color)
    pygame.draw.circle(screen, pclr, (x, y), r)
    t = rou(n)
    pygame.draw.polygon(screen, (0, 0, 0), [[x - d, y], [x + r, y + t], [x + r, y - t]])


def drawl(n):
    global t
    screen.fill(bg_color)
    t = rou(n)
    pygame.draw.circle(screen, pclr, (x, y), r)
    pygame.draw.polygon(screen, (0, 0, 0), [[x + d, y], [x - r, y + t], [x - r, y - t]])


def drawd(n):
    global t
    screen.fill(bg_color)
    t = rou(n)
    pygame.draw.circle(screen, pclr, (x, y), r)
    pygame.draw.polygon(screen, (0, 0, 0), [[x, y - d], [x + t, y + r], [x - t, y + r]])


def drawu(n):
    global t
    screen.fill(bg_color)
    t = rou(n)
    pygame.draw.circle(screen, pclr, (x, y), r)
    pygame.draw.polygon(screen, (0, 0, 0), [[x, y + d], [x - t, y - r], [x + t, y - r]])


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def onLine(l1, p):
    if (
        p.x <= max(l1.p1.x, l1.p2.x)
        and p.x <= min(l1.p1.x, l1.p2.x)
        and p.y <= max(l1.p1.y, l1.p2.y)
        and p.y <= min(l1.p1.y, l1.p2.y)
    ):
        return 1
    return 0


def direction(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
        return 0
    elif val < 0:
        return 2
    return 1


def isIntersect(l1, l2):
    dir1 = direction(l1.p1, l1.p2, l2.p1)
    dir2 = direction(l1.p1, l1.p2, l2.p2)
    dir3 = direction(l2.p1, l2.p2, l1.p1)
    dir4 = direction(l2.p1, l2.p2, l1.p2)

    if dir1 != dir2 and dir3 != dir4:
        return 1

    if dir1 == 0 and onLine(l1, l2.p1):
        return 1

    if dir2 == 0 and onLine(l1, l2.p2):
        return 1

    if dir3 == 0 and onLine(l2, l1.p1):
        return 1

    if dir4 == 0 and onLine(l2, l1.p2):
        return 1

    return 0


def checkInside(poly, n, p):
    if n < 3:
        return 0

    exline = line(p, Point(9999, p.y))
    count = 0
    i = 0
    while True:
        side = line(poly[i], poly[(i + 1) % n])
        if isIntersect(side, exline):
            if direction(side.p1, p, side.p2) == 0:
                return onLine(side, p)
            count += 1

        i = (i + 1) % n
        if i == 0:
            break

    return count & 1


def reset_game():
    global x, y, k, nk, player_pos, running, game_over, t
    x, y = window_size[0] / 2, window_size[0] / 2
    k, nk = 0, 1
    player_pos = [0, 0]
    game_over = False
    t = 0
    start_game()


def game_over_screen():
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('GAME OVER', True, white, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (window_size[0] / 2, window_size[0] / 2 - 20)
    screen.blit(text, textRect)

    font_small = pygame.font.Font('freesansbold.ttf', 20)
    restart_text = font_small.render('Press SPACE to Restart', True, white, (0, 0, 0))
    restartRect = restart_text.get_rect()
    restartRect.center = (window_size[0] / 2, window_size[0] / 2 + 20)
    screen.blit(restart_text, restartRect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    reset_game()


def start_game():
    global polygon
    global x, y, k, nk, t, fin

    fin = True
    t = 0
    start = 0
    n = 0
    running = True
    while running:
        if k != nk:
            c1, c2 = genc()
            nk = k
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= player_speed
            drawu(n)
            polygon = [Point(x, y + d - 1), Point(x - t, y - r), Point(x + t, y - r)]
            eat(c1, c2, x, y)
            n += 0.3
        elif keys[pygame.K_DOWN]:
            y += player_speed
            drawd(n)
            polygon = [Point(x, y - d + 1), Point(x + t, y + r), Point(x - t, y + r)]
            eat(c1, c2, x, y)
            n += 0.3
        elif keys[pygame.K_LEFT]:
            x -= player_speed
            drawl(n)
            polygon = [Point(x + d - 1, y), Point(x - r, y + t), Point(x - r, y - t)]
            eat(c1, c2, x, y)
            n += 0.3
        elif keys[pygame.K_RIGHT]:
            x += player_speed
            drawr(n)
            polygon = [Point(x - d + 1, y), Point(x + r, y + t), Point(x + r, y - t)]
            eat(c1, c2, x, y)
            n += 0.3

        if x < r:
            x = r
        if y < r + 16:
            y = r + 16
        if y > window_size[0] - r:
            y = window_size[0] - r
        if x > window_size[0] - r:
            x = window_size[0] - r
        if fin and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            start = time.time()
            fin = False
        if fin:
            start = time.time()
        ti = 60 - int(time.time() - start)

        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(f'TIME: {ti} SCORE: {k}', True, white, (0, 0, 0))

        if ti == 0:
            game_over_screen()
            break

        textRect = text.get_rect()
        pygame.draw.circle(screen, (255, 0, 0), (c1, c2), 5)
        screen.blit(text, textRect)
        pygame.display.update()

    pygame.quit()


# Start the game for the first time
start_game()
