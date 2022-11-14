import pygame
import sys
import random

width = 700
height = 750
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
        self.color = 30, 230, 86
        self.speed = 5
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update_bullet_position(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.speed += 0.005

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class EnemyBullet():
    def __init__(self, screen, enemy):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = 255, 255, 255
        self.speed = 1
        self.rect.centerx = enemy.rect.centerx
        self.rect.top = enemy.rect.bottom
        self.y = float(self.rect.y)

    def update_bullet_position(self):
        self.y += self.speed
        self.rect.y = self.y
        self.speed += 0.005

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Enemy():
    def __init__(self, screen, type, enemy_number):
        self.screen = screen
        self.number = enemy_number
        if type == 1:
               self.image = pygame.image.load('enemy1.png') 
        if type == 2:
               self.image = pygame.image.load('enemy2.png') 
        if type == 3:
               self.image = pygame.image.load('enemy3.png') 
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed_y = 0.1
        self.speed_x = 0.5
        self.goleft = 1

    def draw_enemy(self):
        self.screen.blit(self.image, self.rect)

    def update_enemy_position(self, enemy, number_of_enemys_x):
        if enemy.goleft:
            enemy.x += enemy.speed_x
            enemy.rect.x = enemy.x
            if enemy.rect.right + enemy.rect.width * (number_of_enemys_x - enemy.number - 1) >= width:
                enemy.goleft = 0
        else:
            enemy.x -= enemy.speed_x
            enemy.rect.x = enemy.x
            if enemy.rect.left - enemy.rect.width * enemy.number <= 0:
                enemy.goleft = 1
        enemy.y += enemy.speed_y
        enemy.rect.y = enemy.y

def create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y):
    enemy = Enemy(screen, 1, 0)
    for enemys_number in range(number_of_enemys_y):
        enemys = []
        type = random.choice((1, 2, 3))
        for enemy_number in range(number_of_enemys_x):
            enemy = Enemy(screen, type, enemy_number)
            enemy.x = (1 + enemy_number) * enemy.rect.width
            enemy.y = (1 + enemys_number) * enemy.rect.height 
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemys.append(enemy)
        enemys_y.append(enemys)

def run():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Space Invaders')
    pygame.mixer.music.set_volume(0.33)
    laser = pygame.mixer.Sound('laser.mp3')
    monster_laser = pygame.mixer.Sound('monster_laser.mp3')
    game_over = pygame.mixer.Sound('game_over.mp3')
    explosion = pygame.mixer.Sound('explosion.mp3')
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    background_color = (0, 0, 0)
    gun = Gun(screen)
    enemys_y = []
    bullets = []
    enemy_bullets = []
    enemy = Enemy(screen, 1, 0)
    number_of_enemys_x = int((width - 2 * enemy.rect.width) / enemy.rect.width)
    number_of_enemys_y = int((height / 2) / enemy.rect.height)
    create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y)
    are_you_winnin_sun = False

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
                    laser.play()
                    new_bullet = Bullet(screen, gun)
                    bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    gun.move_right = False
                if event.key == pygame.K_LEFT:
                    gun.move_left = False
        gun.update_gun_position()
        screen.fill(background_color)
        flag = False

        for enemys in enemys_y:
            for enemy in enemys:
                enemy.update_enemy_position(enemy, number_of_enemys_x)
                enemy.draw_enemy()
                probability_monster_shot = random.choice(range(1, 5000))
                if probability_monster_shot == 1:
                    monster_laser.play()
                    new_enemy_bullet = EnemyBullet(screen, enemy)
                    enemy_bullets.append(new_enemy_bullet)
                if enemy.rect.bottom > gun.rect.top:
                    explosion.play()
                    game_over.play()
                    flag = 1
                    break
            if flag:
                break
        if flag:
            break

        for bullet in bullets:
            bullet.update_bullet_position()
            for enemys in enemys_y:
                for enemy in enemys:
                    if (bullet.rect.top < enemy.rect.bottom and \
                        bullet.rect.top > enemy.rect.top and \
                        bullet.rect.left > enemy.rect.left + 2 and \
                        bullet.rect.right < enemy.rect.right - 2):
                        #-------------------------------------
                        enemys.remove(enemy)
                        bullets.remove(bullet)
            bullet.draw_bullet()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
        for enemy_bullet in enemy_bullets:
            enemy_bullet.update_bullet_position()
            x = enemy_bullet.rect.centerx - gun.rect.left
            distance_to_gun = height - enemy_bullet.rect.bottom
            if (distance_to_gun <= 0.05 * x * x + 9 and x > 0 and x < 24):
                explosion.play()
                game_over.play()
                flag = 1
                break
            if (distance_to_gun <= 43 and x >= 24 and x < 28):
                explosion.play()
                game_over.play()
                flag = 1
                break
            if (distance_to_gun <=  0.05 * (x - 50) * (x - 50) + 9 and x >= 28 and x < 50):
                explosion.play()
                game_over.play()
                flag = 1
                break
            if enemy_bullet.rect.bottom > height:
                enemy_bullets.remove(enemy_bullet)
            enemy_bullet.draw_bullet()
        if flag:
            break
        gun.draw_gun()
        pygame.display.update()

    while(True):
        #тодо нажмите пробел чтобы выйти
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sys.exit()
run()