import pygame
from enemys import Enemy

def create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y):
    enemy = Enemy(screen, 1, 0, 0)
    for enemys_number in range(number_of_enemys_y):
        enemys = []
        if (enemys_number == 0 or enemys_number == 1):
            type = 2
        if (enemys_number == 2 or enemys_number == 3):
            type = 3
        if (enemys_number == 4 or enemys_number == 5):
            type = 1
        for enemy_number in range(number_of_enemys_x):
            enemy = Enemy(screen, type, (1 + enemy_number) *
                          enemy.rect.width, (1 + enemys_number) * enemy.rect.height)
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
    lose_screen_message_one = lose_font_message.render(
        'PRESS ESCAPE TO EXIT', True, lose_color)
    lose_screen_message_two = lose_font_message.render(
        'PRESS R TO RESTART', True, lose_color)
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
