import pygame
import time
import random
import threading

pygame.init()
run = True
clock = pygame.time.Clock()
fps = 80
screen_indent = 0
indent_speed = 3
player_speed = 5
laser_speed = 5
start_health = 3
laser_per_sec = 3
cooldown = 1000 / laser_per_sec

score = 0
level = 1
lives = 5

player_width , player_height = 50 , 50
laser_width, laser_height = 25, 25
enemy_width, enemy_height = 60, 60

enemy_speed = 2
alien_laser_per_sec = 2
alien_cooldown = 1000 / alien_laser_per_sec
last_alien_shot = pygame.time.get_ticks()

#define colors:
red = (255,0,0)
green = (0,255,0)

x = 1.12
screen_width = int(500 * x)
screen_height = int(700 * x)

# Window = screen
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption(
    "Space Invaders 2P")

#load images
image_player1 = pygame.transform.scale(pygame.image.load("game_assets/RED_SHIP.png"), (player_width, player_height) )
image_player2 = pygame.transform.scale(pygame.image.load("game_assets/BLUE_SHIP.png"), (player_width, player_height) )
image_laser = pygame.transform.scale(pygame.image.load("game_assets/laser.png"), (laser_width, laser_height) )

bg = pygame.transform.scale(pygame.image.load("game_assets/galaxy_vert2.jpg"), (screen_width, screen_height))

#Create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()



def draw_bg():

    global screen_indent

    screen.fill((0,0,0))
    screen.blit(bg, (0, screen_indent))
    screen.blit(bg, (0,-screen_height + screen_indent))

    if screen_indent >= screen_height:
        screen.blit(bg, (0, -screen_height))
        screen_indent = 0

    # level , score , enemy_dimensions
    retro_font = pygame.font.Font("game_assets/retro_font.ttf", 20)
    lives_label = retro_font.render(f"Lives: {lives}", 1 ,(255,255,255))
    level_label = retro_font.render(f"Level: {level}", 1 ,(255,255,255))
    score_label = retro_font.render(f"Score: {score}", 1 ,(255,255,255))
    # enemies_label = retro_font.render(f"Enemies remaining: {len(alien_group)}", 1 ,(255,255,255))

    screen.blit(lives_label, (15, 20))
    screen.blit(level_label, (15, 50))
    screen.blit(score_label, (15, 80))
    # screen.blit(enemies_label, (15, 110))

def player1_movement(keys, player1):

    if keys[pygame.K_a] and player1.rect.x  - player_speed >= 0:   #left
        player1.rect.x -= player_speed
    if keys[pygame.K_d] and player1.rect.x + player_width + player_speed <= screen_width:   #right
        player1.rect.x += player_speed
    if keys[pygame.K_w] and player1.rect.y  - player_speed >= 0:   #up
        player1.rect.y -= player_speed
    if keys[pygame.K_s] and player1.rect.y + player_height + player_speed <= screen_height:   #dowmn
        player1.rect.y += player_speed



def player1_shoot(keys, player1):

    time_now = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and time_now - player1.last_shot > cooldown:    #shoot bullet
        bullet = Bullets(player1.rect.centerx, player1.rect.top)
        bullet_group.add(bullet)
        player1.last_shot = time_now


def player2_movement(keys, player2):

    if keys[pygame.K_LEFT] and player2.rect.x - player_speed >= 0:   #left
        player2.rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player2.rect.x + player_width + player_speed <= screen_width:   #right
        player2.rect.x += player_speed
    if keys[pygame.K_UP] and player2.rect.y  - player_speed >= 0:   #up
        player2.rect.y -= player_speed
    if keys[pygame.K_DOWN] and player2.rect.y + player_height + player_speed <= screen_height:   #dowmn
        player2.rect.y += player_speed

def player2_shoot(keys, player2):

    time_now = pygame.time.get_ticks()
    if keys[pygame.K_KP0] and time_now - player2.last_shot > cooldown:    #shoot bullet
        bullet = Bullets(player2.rect.centerx, player2.rect.top)
        bullet_group.add(bullet)
        player2.last_shot = time_now

#Create spaceship class
#use classes for inheritance control & shoot
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, image, health=start_health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):

        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 8), self.rect.width, 8 ))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 8), int(self.rect.width * (self.health_remaining /self.health_start )), 8 ))

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, image=image_laser):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= laser_speed
        if self.rect.bottom <= 0:
            self.kill()

        global score
        if pygame.sprite.spritecollide(self, alien_group, True):
            score += 1
            self.kill()

class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, image=image_laser):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += laser_speed
        if self.rect.top >= screen_height or self.rect.bottom <= 0:
            self.kill()

        if self.rect.colliderect(player1):
            self.kill()
            player1.health_remaining -= 1

        if self.rect.colliderect(player2):
            self.kill()
            player2.health_remaining -= 1

class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("game_assets/enemy" + str(random.randrange(1,4)) + ".png"), (enemy_width, enemy_height) )
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += enemy_speed

        if self.rect.top >= screen_height:
            global lives
            lives -= 1
            self.kill()

def create_aliens():
    global level, player1, player2, alien_group
    wave_length = 5 * level

    for item in range(wave_length):
        alien = Aliens(random.randrange(enemy_width//2, screen_width - enemy_width//2), random.randrange(int(-4000 * level/4), -50))
        # alien = Aliens(100 + item * 100, 100 + row *70)
        alien_group.add(alien)

def alien_collide():
    for alien in alien_group:
        if alien.rect.colliderect(player1.rect):
            alien.kill()
            player1.health_remaining -= 1

        if alien.rect.colliderect(player2.rect):
            alien.kill()
            player2.health_remaining -= 1

def main():
    global run, level, last_alien_shot , screen_indent , indent_speed

    while run:
        #event handler

        if lives < 0 or player1.health_remaining == 0 or player2.health_remaining == 0:
            pygame.display.update()
            run = False
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if len(alien_group) == 0:
            level += 1
            create_aliens()

        clock.tick(fps)

        alien_collide()
        draw_bg()

        #create random alien bullets and record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if time_now - last_alien_shot > alien_cooldown:

            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        keys = pygame.key.get_pressed()
        player1_thread = threading.Thread(target=player1_movement(keys, player1))
        player2_thread = threading.Thread(target=player2_movement(keys, player2))
        player1_shoot_thread = threading.Thread(target=player1_shoot(keys, player1))
        player2_shoot_thread = threading.Thread(target=player2_shoot(keys, player2))

        player1_thread.start()
        player2_thread.start()
        player1_shoot_thread.start()
        player2_shoot_thread.start()

        #draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)

        bullet_group.update()
        alien_group.update( )
        alien_bullet_group.update()

        #sprite updates
        player1.update()
        player2.update()

        screen_indent += indent_speed
        pygame.display.update()

    main_menu()

def main_menu():

    global run, score, level, lives

    retro_font = pygame.font.Font("game_assets/retro_font.ttf", 20)

    # last_score_label = last_score_font.render(f"Last score: {score}", 1 ,(255,255,255))
    instruction_label = retro_font.render(f"Press ENTER to play", 1 ,(255,255,255))

    # screen.blit(last_score_label, (screen_width//2 - last_score_font.get_height()//2 , screen_height//2 - 30))
    screen.blit(instruction_label, ( int(screen_width/2 - instruction_label.get_width()/2) , screen_height//2))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:

            for item in alien_group:
                item.kill()
            for item in alien_bullet_group:
                item.kill()
            for item in bullet_group:
                item.kill()
            score = 0
            level = 1
            lives = 5
            player1.health_remaining = start_health
            player2.health_remaining = start_health
            main()

create_aliens()
#create players
player1 = Spaceship(int(screen_width/4), int(3 * screen_height/4) , image_player1)
player2 = Spaceship(int(3 * screen_width/4), int(3*screen_height/4) , image_player2)
spaceship_group.add(player1)
spaceship_group.add(player2)


if __name__ == "__main__":
    main_menu()
