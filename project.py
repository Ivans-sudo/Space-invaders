import pygame
import sys
import random

width = 700
height = 750
fps = 144
max_probability_of_shot = 1000
enemy_speed_x = 0.5
enemy_speed_y = 0.1
gun_speed_x = 0.7
bullet_speed = 5
enemy_bullet_speed = 1


class Statistics():
    def __init__(self):
        self.health = 3
        self.score = 0

    def lose_health_point(self):
        self.health -= 1
    def add_score(self):
        self.score += 10


class Score():
    def __init__(self, screen, statistics):
        self.screen = screen
        self.statistics = statistics
        self.screen_rect = screen.get_rect()
        self.color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont('Monospaced', 36)
        self.update_score(statistics)

    def update_score(self, statistics):
        self.score_image = self.font.render(str('SCORE: ' + str(statistics.score)), True, self.color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 75
        self.score_rect.top = self.screen_rect.top + 15
        
        self.health_image = self.font.render(str('HEALTH: ' + str(statistics.health)), True, self.color)
        self.health_rect = self.health_image.get_rect()
        self.health_rect.left = self.screen_rect.left + 75
        self.health_rect.top = self.screen_rect.top + 15

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.health_image, self.health_rect)

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
            self.center += gun_speed_x
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= gun_speed_x
        self.rect.centerx = self.center


class Bullet():
    def __init__(self, screen, gun):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (30, 230, 86)
        self.speed = bullet_speed
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
        self.color = (255, 255, 255)
        self.speed = enemy_bullet_speed
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
        self.speed_y = enemy_speed_y
        self.speed_x = enemy_speed_x
        self.can_go_left = True

    def draw_enemy(self):
        self.screen.blit(self.image, self.rect)

    def update_enemy_position(self, enemy, number_of_enemys_x):
        if enemy.can_go_left:
            enemy.x += enemy.speed_x
            enemy.rect.x = enemy.x
            if enemy.rect.right + enemy.rect.width * (number_of_enemys_x - enemy.number - 1) >= width:
                enemy.can_go_left = False
        else:
            enemy.x -= enemy.speed_x
            enemy.rect.x = enemy.x
            if enemy.rect.left - enemy.rect.width * enemy.number <= 0:
                enemy.can_go_left = True
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

def lose_screen(screen):
    lose_font = pygame.font.SysFont('Monospaced', 72)
    lose_font_message = pygame.font.SysFont('Monospaced', 32)
    lose_color = (30, 230, 86)
    lose_screen = lose_font.render('GAME OVER', True, lose_color)
    lose_screen_message_one = lose_font_message.render('PRESS SPACE TO EXIT', True, lose_color)
    lose_screen_message_two = lose_font_message.render('PRESS R TO RESTART', True, lose_color)
    lose_screen_rect = lose_screen.get_rect()
    lose_screen_message_one_rect = lose_screen_message_one.get_rect()
    lose_screen_message_two_rect = lose_screen_message_two.get_rect()
    screen_rect = screen.get_rect()
    lose_screen_rect.centerx = screen_rect.centerx
    lose_screen_rect.centery = screen_rect.centery - 36
    lose_screen_message_one_rect.centerx = screen_rect.centerx
    lose_screen_message_two_rect.centerx = screen_rect.centerx
    lose_screen_message_one_rect.centery = screen_rect.centery
    lose_screen_message_two_rect.centery = screen_rect.centery + 22
    screen.blit(lose_screen, lose_screen_rect)
    screen.blit(lose_screen_message_one, lose_screen_message_one_rect)
    screen.blit(lose_screen_message_two, lose_screen_message_two_rect)
    pygame.display.update()  

def run():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Space Invaders')
    explosion_sound = pygame.mixer.Channel(0)
    game_over_sound = pygame.mixer.Channel(1)
    pygame.mixer.set_num_channels(16)
    pygame.mixer.music.set_volume(0.33)
    laser = pygame.mixer.Sound('laser.mp3')
    monster_laser = pygame.mixer.Sound('monster_laser.mp3')
    game_over = pygame.mixer.Sound('game_over.mp3')
    explosion = pygame.mixer.Sound('explosion.mp3')
    next_level = pygame.mixer.Sound('next_level.mp3')
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    statistics = Statistics()
    score = Score(screen, statistics)
    background_color = (0, 0, 0)
    enemy = Enemy(screen, 1, 0)
    gun = Gun(screen)
    enemys_y = []
    bullets = []
    enemy_bullets = []
    number_of_enemys_x = int((width - 2 * enemy.rect.width) / enemy.rect.width)
    number_of_enemys_y = int((height / 2) / enemy.rect.height)
    number_of_enemys = number_of_enemys_x * number_of_enemys_y
    create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y)

    while (True):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    gun.move_right = True
                if event.key == pygame.K_LEFT:
                    gun.move_left = True
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    laser.play()
                    new_bullet = Bullet(screen, gun)
                    bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    gun.move_right = False
                if event.key == pygame.K_LEFT:
                    gun.move_left = False

        screen.fill(background_color)
        score.draw_score()
        gun.update_gun_position()
        gun.draw_gun()
        flag_shoot = False
        flag_range = False

        for enemys in enemys_y:
            for enemy in enemys:
                enemy.update_enemy_position(enemy, number_of_enemys_x)
                enemy.draw_enemy()
                probability_monster_shot = random.choice(range(1, max_probability_of_shot))
                if probability_monster_shot == 1:
                    monster_laser.play()
                    new_enemy_bullet = EnemyBullet(screen, enemy)
                    enemy_bullets.append(new_enemy_bullet)
                if enemy.rect.bottom > gun.rect.top:
                    explosion.play()
                    game_over.play()
                    flag_range = 1
                    break
            if flag_range:
                break

        for bullet in bullets:
            is_removed = False
            bullet.update_bullet_position()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)
                continue
            for enemys in enemys_y:
                for enemy in enemys:
                    if (bullet.rect.top < enemy.rect.bottom and
                        bullet.rect.top > enemy.rect.top and
                        bullet.rect.left > enemy.rect.left + 2 and
                            bullet.rect.right < enemy.rect.right - 2):
                        # -----------------------------------------
                        statistics.add_score()
                        score.update_score(statistics)
                        enemys.remove(enemy)
                        bullets.remove(bullet)
                        number_of_enemys -= 1
                        is_removed = True
                        break
                if is_removed:
                    break
            for enemy_bullet in enemy_bullets:
                if is_removed:
                    break
                if bullet.rect.top < enemy_bullet.rect.bottom and \
                    ((bullet.rect.left > enemy_bullet.rect.left and bullet.rect.left < enemy_bullet.rect.right) or
                     (bullet.rect.right < enemy_bullet.rect.right and bullet.rect.right > enemy_bullet.rect.left)):
                    # -----------------------------------------
                    bullets.remove(bullet)
                    enemy_bullets.remove(enemy_bullet)
                    break
            bullet.draw_bullet()

        for enemy_bullet in enemy_bullets:
            enemy_bullet.update_bullet_position()
            if enemy_bullet.rect.bottom > height:
                enemy_bullets.remove(enemy_bullet)
                continue
            x = enemy_bullet.rect.centerx - gun.rect.left
            distance_to_gun = height - enemy_bullet.rect.bottom
            if (distance_to_gun <= 0.05 * x * x + 9 and x > 0 and x < 24):
                explosion_sound.play(explosion)
                game_over_sound.play(game_over)
                flag_shoot = True
            if (distance_to_gun <= 43 and x >= 24 and x < 28):
                explosion_sound.play(explosion)
                game_over_sound.play(game_over)
                flag_shoot = True
            if (distance_to_gun <= 0.05 * (x - 50) * (x - 50) + 9 and x >= 28 and x < 50):
                explosion_sound.play(explosion)
                game_over_sound.play(game_over)
                flag_shoot = True
            if flag_shoot:
                break
            enemy_bullet.draw_bullet()

        if flag_shoot:
            statistics.health -= 1
            score.update_score(statistics)
            if statistics.health > 0:
                bullets.clear()
                enemy_bullets.clear()
                flag_shoot = False
                pygame.time.delay(1500)
                pygame.event.clear()
        if flag_range or flag_shoot and statistics.health < 1:
            pygame.time.delay(1500)
            pygame.event.clear()
            score.update_score(statistics)
            screen.fill(background_color)
            score.draw_score()
            lose_screen(screen)
            while (True):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            sys.exit()
                        if event.key == pygame.K_r:
                            run()
        if number_of_enemys == 0:
            next_level.play()
            for enemys in enemys_y:
                enemys.clear()
            enemys_y.clear()
            create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y)
            bullets.clear()
            enemy_bullets.clear()
            number_of_enemys = number_of_enemys_x * number_of_enemys_y
            screen.fill(background_color)
            score.draw_score()
            gun.update_gun_position()
            gun.draw_gun()
            pygame.display.update()
            pygame.time.delay(1500)
            pygame.event.clear()

        pygame.display.update()


run()
