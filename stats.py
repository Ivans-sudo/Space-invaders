import pygame
from gun import Gun;

class Statistics():
    def __init__(self):
        self.health = 3
        self.score = 0
        with open('highscore.txt', 'r') as file:
            self.highscore = int(file.readline())

    def add_score(self, type):
        if type == 1:
            self.score += 10
        if type == 2:
            self.score += 20
        if type == 3:
            self.score += 15
            


class Score():
    def __init__(self, screen, statistics):
        self.screen = screen
        self.statistics = statistics
        self.screen_rect = screen.get_rect()
        self.color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont('Monospaced', 36)
        self.guns = []
        self.update_score()

    def update_score(self):
        self.score_image = self.font.render(
            str('SCORE: ' + str(self.statistics.score)), True, self.color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx + 235
        self.score_rect.top = self.screen_rect.top + 15

        self.highscore_image = self.font.render(
            str('HIGHSCORE: ' + str(self.statistics.highscore)), True, self.color)
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.screen_rect.top + 15

    def update_health_score(self):
        self.guns.clear()
        for gun_number in range(self.statistics.health):
            gun = Gun(self.screen)
            gun.rect.x = 30 + gun_number * gun.rect.width
            gun.rect.top = self.screen_rect.top
            self.guns.append(gun)

    def check_highscore(self):
        if self.statistics.score > self.statistics.highscore:
            self.statistics.highscore = self.statistics.score
            with open('highscore.txt', 'w') as file:
                file.write(str(self.statistics.highscore))

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        for gun in self.guns:
            gun.draw_gun()

