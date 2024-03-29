import pygame
import random

WIDTH = 600
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze game")
clock = pygame.time.Clock()
font_name = pygame.font.match_font("arial")

coin_sound = pygame.mixer.Sound("coin.mp3")
tp_sound = pygame.mixer.Sound("teleport.mp3")
pygame.mixer.music.load("music.ogg")
pygame.mixer.music.set_volume(0.4)

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 0
        self.speedy = 0
        self.speed = speed
        self.cheat = False

    def update(self) -> None:
        key = pygame.key.get_pressed()
        self.speedx = 0
        self.speedy = 0

        if key[pygame.K_w]:
            self.speedy -= self.speed
        if key[pygame.K_a]:
            self.speedx -= self.speed
        if key[pygame.K_s]:
            self.speedy += self.speed
        if key[pygame.K_d]:
            self.speedx += self.speed
        if key[pygame.K_t]: self.cheat = False
        if key[pygame.K_y]: 
            self.cheat = True
            lvl -= 1

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if not self.cheat:
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0 

class Wall(pygame.sprite.Sprite):
    def __init__(self, x_, y_, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_
        self.rect.centery = y_

class Finish(pygame.sprite.Sprite):
    def __init__(self, x_, y_,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_
        self.rect.centery = y_

class Boost(pygame.sprite.Sprite):
    def __init__(self, x_, y_,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_
        self.rect.centery = y_

class Coin(pygame.sprite.Sprite):
    def __init__(self, x_, y_,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_
        self.rect.centery = y_


all_spr = pygame.sprite.Group()
walls = pygame.sprite.Group()
goal_ = pygame.sprite.Group()
boosts = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player(30, 30, 8)
goal = Finish(585, 585)
goal_.add(goal)
all_spr.add(player, goal)
lvl = 0
score = 0

def wall_gen(amount):
    wh_wall = [100, 30]
    if amount < 15:
        for i in range(amount):
            width_w = random.choice(wh_wall)
            wh_wall.pop(wh_wall.index(width_w))
            w = Wall(random.randint(100, 500), random.randint(100, 500), width_w, wh_wall[0])
            all_spr.add(w)
            walls.add(w)
            wh_wall = [100, 30]
    
    elif amount >= 15 and amount < 25:
        for i in range(amount):
            width_w = random.choice(wh_wall)
            wh_wall.pop(wh_wall.index(width_w))
            w = Wall(random.randint(50, 550), random.randint(50, 550), width_w, wh_wall[0])
            all_spr.add(w)
            walls.add(w)
            wh_wall = [100, 30]

    elif amount >= 25:
        for i in range(amount):
            width_w = random.choice(wh_wall)
            wh_wall.pop(wh_wall.index(width_w))
            w = Wall(random.randint(30, 560), random.randint(30, 560), width_w, wh_wall[0])
            all_spr.add(w)
            walls.add(w)
            wh_wall = [100, 30]

def boost_gen(amount):
    if amount > 0:
        for i in range(amount):
            b = Boost(random.randint(30, 470), random.randint(30, 470))
            all_spr.add(b)
            boosts.add(b)

def coin_gen(amount):
    if amount > 0:
        for i in range(amount):
            c = Coin(random.randint(10, 580), random.randint(10, 580))
            all_spr.add(c)
            coins.add(c)

wall_gen(lvl + 5)
boost_gen(lvl - 5)
coin_gen(lvl)

pygame.mixer.music.play(loops=-1)

# loop
run = True
while run:
    # startup
    clock.tick(FPS)
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            run = False


    # update
    all_spr.update()
    if not player.cheat:
        hits = pygame.sprite.spritecollide(player, goal_, False)
        if hits:
            lvl += 1
            player.rect.x = 0
            player.rect.y = 0
            all_spr.remove(walls)
            all_spr.remove(boosts)
            walls.empty()
            boosts.empty()
            wall_gen(lvl + 5)
            boost_gen(lvl - 10)
            coin_gen(lvl - 5)

        wall_col = pygame.sprite.spritecollide(player, walls, False)
        if wall_col:
            player.rect.x -= player.speedx
            player.rect.y -= player.speedy

        boost_col = pygame.sprite.spritecollide(player, boosts, False)
        if boost_col:
            player.rect.x += player.speedx
            player.rect.y += player.speedy
            tp_sound.play()

        coin_grab = pygame.sprite.spritecollide(player, coins, True)
        if coin_grab:
            score += 1
            coin_sound.play()

    if lvl in range(15, 100, 3):
        all_spr.remove(coins, boosts)
        coins.empty()
        boosts.empty()

    # render
    screen.fill(BLACK)
    all_spr.draw(screen)
    draw_text(screen, "X: " + str(player.rect.x), 30, WIDTH - 50, 0)
    draw_text(screen, "Y: " + str(player.rect.y), 30, WIDTH - 50, 30)
    draw_text(screen, "LEVEL: " + str(lvl), 40, WIDTH / 2, 10)
    draw_text(screen, "COINS: " + str(score), 40, WIDTH / 2, 50)
    pygame.display.flip()

pygame.quit()