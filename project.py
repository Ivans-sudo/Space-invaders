import pygame
import sys

width = 700
height = 800
fps = 144

class Gun():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.move_right = False
        self.move_left = False

    def draw_gun(self):
        self.screen.blit(self.image, self.rect)

    def update_gun_position(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += 0.7
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= 0.7
        self.rect.centerx = self.center
        
class Bullet():
    def __init__(self, screen, gun):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = 255, 255, 255
        self.speed = 0.75
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update_bullet_position(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.speed += 0.005

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Enemy():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('enemy1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = 0.2

    def draw_enemy(self):
        self.screen.blit(self.image, self.rect)

    def update_enemy_position(self):
        self.y += self.speed
        self.rect.y = self.y

def create_army(screen, enemys_y):
    enemy = Enemy(screen)
    enemy_width = enemy.rect.width
    enemy_height = enemy.rect.height
    number_of_enemys_x = int((width - 2 * enemy_width) / enemy_width)
    number_of_enemys_y = int((height / 2) / enemy_height)
    for enemys_number in range(number_of_enemys_y):
        enemys = []
        for enemy_number in range(number_of_enemys_x):
            enemy = Enemy(screen)
            enemy.x = (1 + enemy_number) * enemy_width
            enemy.y = (1 + enemys_number) * enemy_height 
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemys.append(enemy)
        enemys_y.append(enemys)

def run():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Space Invaders')
    pygame.mixer.music.set_volume(0.025)
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    background_color = (0, 0, 0)
    gun = Gun(screen)
    enemys_y = []
    bullets = []
    create_army(screen, enemys_y)
    while (True):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    gun.move_right = True
                if event.key == pygame.K_LEFT:
                    gun.move_left = True
                if event.key == pygame.K_UP:
                    new_bullet = Bullet(screen, gun)
                    bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    gun.move_right = False
                if event.key == pygame.K_LEFT:
                    gun.move_left = False
        gun.update_gun_position()
        screen.fill(background_color)
        for enemys in enemys_y:
            for enemy in enemys:
                enemy.update_enemy_position()
                enemy.draw_enemy()
        for bullet in bullets:
            bullet.update_bullet_position()

            for enemys in enemys_y:
                for enemy in enemys:
                    if (bullet.rect.top < enemy.rect.bottom and \
                        bullet.rect.top > enemy.rect.top and \
                        bullet.rect.left > enemy.rect.left and \
                        bullet.rect.right < enemy.rect.right):
                        #-------------------------------------
                        enemys.remove(enemy)
                        bullets.remove(bullet)

            bullet.draw_bullet()
            
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
        gun.draw_gun()
        pygame.display.update()

run()