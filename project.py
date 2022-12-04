import pygame
from gun import Gun, Bullet
from func import create_army, lose_screen
from stats import Score, Statistics
from enemys import Enemy

width = 700
height = 750
fps = 120


def run():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Space Invaders')
    explosion_sound = pygame.mixer.Channel(0)
    game_over_sound = pygame.mixer.Channel(1)
    pygame.mixer.set_num_channels(16)
    pygame.mixer.music.set_volume(0.33)
    laser = pygame.mixer.Sound('audio/laser.mp3')
    monster_laser = pygame.mixer.Sound('audio/monster_laser.mp3')
    game_over = pygame.mixer.Sound('audio/game_over.mp3')
    explosion = pygame.mixer.Sound('audio/explosion.mp3')
    next_level = pygame.mixer.Sound('audio/next_level.mp3')
    pygame.mixer.music.load('audio/bgmusic.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    statistics = Statistics()
    score = Score(screen, statistics)
    background_color = (0, 0, 0)
    enemy = Enemy(screen, 1, 0, 0)
    gun = Gun(screen)
    enemys_y = []
    bullets = []
    enemy_bullets = []
    number_of_enemys_x = int((width - 2 * enemy.rect.width) / enemy.rect.width)
    number_of_enemys_y = int((height / 2) / enemy.rect.height) - 1
    number_of_enemys = number_of_enemys_x * number_of_enemys_y
    create_army(screen, enemys_y, number_of_enemys_x, number_of_enemys_y)
    score.update_health_score()
    right_column = number_of_enemys_x
    left_column = 1
    acceleration = 0.15
    speed_factor = number_of_enemys / 2
    while (True):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
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

        screen.fill(background_color)
        score.draw_score()
        gun.update_gun_position()
        gun.draw_gun()
        flag_shoot = False
        flag_range = False
        number_in_left_column = 0
        number_in_right_column = 0

        for enemys in enemys_y:
            for enemy in enemys:
                if enemy.enemy_x_default_position == right_column * enemy.rect.width:
                    number_in_right_column += 1
                if enemy.enemy_x_default_position == left_column * enemy.rect.width:
                    number_in_left_column += 1
                enemy.update_enemy_position()
                enemy.draw_enemy()
                enemy.shoot(screen, enemy_bullets, monster_laser)
                if enemy.rect.bottom > gun.rect.top + 15:
                    explosion.play()
                    game_over.play()
                    flag_range = 1
                    break
            if flag_range:
                break
        if number_in_right_column == 0:
            for enemys in enemys_y:
                for enemy in enemys:
                    enemy.max_right += 1
            right_column -= 1
        if number_in_left_column == 0:
            for enemys in enemys_y:
                for enemy in enemys:
                    enemy.max_left += 1
            left_column += 1

        for bullet in bullets:
            is_removed = False
            bullet.update_bullet_position()
            if bullet.rect.top < 0:
                bullets.remove(bullet)
                continue
            for enemys in enemys_y:
                for enemy in enemys:
                    if enemy.type == 1:
                        amandment = 2
                    if enemy.type == 2:
                        amandment = 10
                    if enemy.type == 3:
                        amandment = 5
                    if bullet.rect.top < enemy.rect.bottom and \
                       bullet.rect.top > enemy.rect.top and \
                       bullet.rect.left > enemy.rect.left + amandment and \
                       bullet.rect.right < enemy.rect.right - amandment:
                        statistics.add_score(enemy.type)
                        score.check_highscore()
                        score.update_score()
                        enemys.remove(enemy)
                        bullets.remove(bullet)
                        number_of_enemys -= 1
                        if number_of_enemys == speed_factor:
                            speed_factor = int(speed_factor / 2)
                            for enemys in enemys_y:
                                for enemy in enemys:
                                    enemy.speed += acceleration
                            acceleration *= 2
                        is_removed = True
                        break
                if is_removed:
                    break
            for enemy_bullet in enemy_bullets:
                if is_removed:
                    break
                if (bullet.rect.top < enemy_bullet.rect.bottom and \
                   (bullet.rect.left > enemy_bullet.rect.left and bullet.rect.left < enemy_bullet.rect.right or \
                   bullet.rect.right < enemy_bullet.rect.right and bullet.rect.right > enemy_bullet.rect.left)):
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
            if (distance_to_gun <= 0.05 * x * x + 9 and x > 0 and x < 24 or \
               distance_to_gun <= 43 and x >= 24 and x < 28 or \
               distance_to_gun <= 0.05 * (x - 50) * (x - 50) + 9 and x >= 28 and x < 50):
                explosion_sound.play(explosion)
                game_over_sound.play(game_over)
                flag_shoot = True
            if flag_shoot:
                break
            enemy_bullet.draw_bullet()

        if flag_shoot:
            statistics.health -= 1
            score.update_score()
            score.update_health_score()
            if statistics.health > 0:
                bullets.clear()
                enemy_bullets.clear()
                flag_shoot = False
                pygame.time.delay(1500)
                pygame.event.clear()
                gun.move_right = False
                gun.move_left = False
        if flag_range or flag_shoot and statistics.health < 1:
            pygame.time.delay(1500)
            pygame.event.clear()
            score.update_score()
            score.update_health_score()
            screen.fill(background_color)
            score.draw_score()
            lose_screen(screen)
            while (True):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit()
                        if event.key == pygame.K_r:
                            run()
        if number_of_enemys == 0:
            next_level.play()
            right_column = number_of_enemys_x
            left_column = 1
            gun.move_right = False
            gun.move_left = False
            acceleration = 0.15
            speed_factor = number_of_enemys_x * number_of_enemys_y / 2
            for enemys in enemys_y:
                enemys.clear()
            enemys_y.clear()
            create_army(screen, enemys_y, number_of_enemys_x,
                        number_of_enemys_y)
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
