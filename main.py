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
        global score
        key = pygame.key.get_pressed()
        self.speedx = 0
        self.speedy = 0

        if key[pygame.K_w] or key[pygame.K_UP]:
            self.speedy -= self.speed
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.speedx -= self.speed
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.speedy += self.speed
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.speedx += self.speed
        if key[pygame.K_t]: self.cheat = False
        if key[pygame.K_y]: 
            self.cheat = True
            score -= 1

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
        self.image = pygame.Surface((width * 30, height * 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_ * 30, y_ * 30)

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
        self.rect.topleft = (x_ * 30, y_ * 30)

class Secret(pygame.sprite.Sprite):
    def __init__(self, x_, y_,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_ * 30, y_ * 30)

all_spr = pygame.sprite.Group()
walls = pygame.sprite.Group()
goal_ = pygame.sprite.Group()
boosts = pygame.sprite.Group()
coins = pygame.sprite.Group()
secrets = pygame.sprite.Group()

player = Player(20, 20, 4)
goal = Finish(585, 585)
goal_.add(goal)
all_spr.add(player, goal)
lvl = 0
score = 0

def wall_gen(level):
    if level == 0:
        w = Wall(1, 0, 1, 5)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 6, 1, 5)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 12, 1, 4)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 17, 7, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 19, 7, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 10, 5, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(2, 10, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(2, 130, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(2, 15, 16, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 10, 1, 10)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 13, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 0, 1, 9)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 1, 1, 6)
        all_spr.add(w)
        walls.add(w)

        w = Wall(7, 0, 1, 7)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 0, 1, 5)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 8, 8, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(10, 10, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 6, 6, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(14, 7, 1, 7)
        all_spr.add(w)
        walls.add(w)

        w = Wall(12, 10, 1, 4)
        all_spr.add(w)
        walls.add(w)

        w = Wall(16, 5, 1, 9)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 4, 9, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 1, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 1, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(19, 1, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 0, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 0, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(18, 6, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(18, 10, 2, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(18, 12, 1, 4)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 17, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 17, 6, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 19, 6, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(18, 18, 1, 1)
        all_spr.add(w)
        walls.add(w)
    
    elif level == 1:
        w = Wall(19, 0, 1, 17)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 7, 9, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(19, 0, 1, 17)
        all_spr.add(w)
        walls.add(w)

        w = Wall(0, 17, 10, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 0, 1, 8)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 1, 1, 8)
        all_spr.add(w)
        walls.add(w)

        w = Wall(7, 1, 1, 8)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 3, 1, 8)
        all_spr.add(w)
        walls.add(w)

        w = Wall(8, 9, 6, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(2, 1, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 5, 8, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(0, 10, 7, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 3, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 1, 7, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 2, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 2, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(6, 11, 1, 5)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 15, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 12, 2, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 12, 2, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 13, 1, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(8, 11, 5, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(8, 12, 1, 4)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 15, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(19, 0, 1, 17)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 8, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(16, 9, 2, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 10, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(14, 10, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 11, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(16, 12, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 13, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 12, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(14, 13, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 14, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(16, 15, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 16, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 13, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(12, 14, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 15, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(14, 16, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 17, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(10, 13, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 14, 1, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(15, 18, 1, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(11, 17, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(12, 17, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(13, 18, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 2, 1, 2)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 5, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 8, 3, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(17, 16, 1, 3)
        all_spr.add(w)
        walls.add(w)

        w = Wall(18, 18, 2, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(1, 19, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(3, 18, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(5, 19, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(7, 18, 1, 1)
        all_spr.add(w)
        walls.add(w)

        w = Wall(9, 19, 1, 1)
        all_spr.add(w)
        walls.add(w)

def boost_gen(amount):
    if amount > 0:
        for i in range(amount):
            b = Boost(random.randint(30, 470), random.randint(30, 470))
            all_spr.add(b)
            boosts.add(b)

def coin_gen(level):
    if level == 0:
        c = Coin(10 + (1/3), 11 + (1/3))
        coins.add(c)
        all_spr.add(c)

def secret_gen(level):
    if level in (0, 0):
        s = Secret(19, 0)
        secrets.add(s)
        all_spr.add(s)

wall_gen(lvl)
boost_gen(lvl - 5)
coin_gen(lvl)
secret_gen(lvl)

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
        finished = pygame.sprite.spritecollide(player, goal_, False)
        if finished:
            lvl += 1
            player.rect.x = 0
            player.rect.y = 0
            all_spr.remove(walls)
            all_spr.remove(boosts)
            all_spr.remove(coins)
            walls.empty()
            boosts.empty()
            coins.empty()
            wall_gen(lvl)
            boost_gen(lvl - 10)
            coin_gen(lvl)
            secret_gen(lvl + 1)

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

        secret_col = pygame.sprite.spritecollide(player, secrets, True)
        if secret_col:
            all_spr.remove(walls, boosts, coins)
            walls.empty()
            boosts.empty()
            coins.empty()
            lvl -= 1
            for x in range(10):
                for y in range(10):
                    bonus = Coin(x + (1/3), y + (1/3))
                    all_spr.add(bonus)
                    coins.add(bonus)


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