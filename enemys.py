import pygame
import random


class EnemyBullet():
    def __init__(self, screen, enemy):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (255, 255, 255)
        self.speed = 3
        self.rect.centerx = enemy.rect.centerx
        self.rect.centery = enemy.rect.centery
        self.y = float(self.rect.y)

    def update_bullet_position(self):
        self.y += self.speed
        self.rect.y = self.y
        self.speed += 0.005

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Enemy():
    def __init__(self, screen, type, enemy_x_default_position, enemy_y_default_position):
        self.max_right = 1
        self.max_left = 1
        self.enemy_x_default_position = enemy_x_default_position
        self.enemy_y_default_position = enemy_y_default_position
        self.screen = screen
        self.type = type
        if type == 1:
            self.image = pygame.image.load('textures/enemy1.png')
        if type == 2:
            self.image = pygame.image.load('textures/enemy2.png')
        if type == 3:
            self.image = pygame.image.load('textures/enemy3.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = 0.5
        self.can_go_left = True
        self.can_go_down = False

    def draw_enemy(self):
        self.screen.blit(self.image, self.rect)

    def update_enemy_position(self):
        if self.can_go_down and self.rect.y <= self.enemy_y_default_position + self.rect.height:
            self.y += self.speed
            self.rect.y = self.y
            return
        self.enemy_y_default_position = self.rect.y
        self.can_go_down = False
        if self.can_go_left:
            self.x += self.speed
            self.rect.x = self.x
            if self.rect.x >= self.enemy_x_default_position + self.max_right * self.rect.width:
                self.can_go_left = False
                self.can_go_down = True
        else:
            self.x -= self.speed
            self.rect.x = self.x
            if self.rect.x <= self.enemy_x_default_position - self.max_left * self.rect.width:
                self.can_go_left = True
                self.can_go_down = True

    def shoot(self, screen, enemy_bullets, monster_laser):
        probability_monster_shot = random.choice(
            range(1, 1400))
        if probability_monster_shot == 1:
            monster_laser.play()
            new_enemy_bullet = EnemyBullet(screen, self)
            enemy_bullets.append(new_enemy_bullet)