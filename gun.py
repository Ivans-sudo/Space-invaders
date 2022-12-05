import pygame
from globals import gun_speed, gun_bullet_speed

class Gun():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('textures/gun.png')
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
            self.center += gun_speed
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= gun_speed
        self.rect.centerx = self.center


class Bullet():
    def __init__(self, screen, gun):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = (30, 230, 86)
        self.speed = gun_bullet_speed
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update_bullet_position(self):
        self.y -= self.speed
        self.rect.y = self.y
        self.speed += 0.005

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)