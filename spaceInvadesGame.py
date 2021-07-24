import pygame
import random

pygame.init()

window_height = 600
window_width = 800
rows = 3
cols = 10
game_over = 0
clock = pygame.time.Clock()
timer = pygame.time.get_ticks()

screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Space Invaders")

background = pygame.image.load("images/background.jpg").convert()

invaders_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerBullet_group = pygame.sprite.Group()
invaderBullet_group = pygame.sprite.Group()

playerbullet = pygame.image.load("images/user_bullet.png").convert()
invaderbullet = pygame.image.load("images/invader_bullet.png").convert()
invader = pygame.image.load("images/spaceInvaders.png").convert()
player = pygame.image.load("images/user.png").convert()
gameover = pygame.image.load("images/gameover_background.jpg").convert()

class player_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerbullet
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        self.rect.y -= 5
        if pygame.sprite.spritecollide(self, invaders_group, True):
            self.kill()

class invader_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = invaderbullet
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.rect.y += 2

        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            player.health_remanining -= 10



class Invader(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = invader
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if self.move_counter > 75:
            self.move_direction *= -1
            self.move_counter *= -1


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.last_shot = pygame.time.get_ticks()
        self.health_start = 50
        self.health_remanining = 50

    def update(self):
        speed = 3
        cooldown = 1000
        current_time = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        gameover = 0

        pygame.draw.rect(screen, (0,0,0), (self.rect.x, self.rect.bottom, self.rect.width,10))

        if self.health_remanining > 0:
            pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.bottom, int(self.rect.width*(self.health_remanining/ self.health_start)),10))
        elif self.health_remanining == 0:
            self.kill()
            gameover = 1

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        
        if key[pygame.K_RIGHT] and self.rect.right < window_width:
            self.rect.x += speed

        if key[pygame.K_SPACE] and current_time - self.last_shot > cooldown:
            bullet = player_bullet(self.rect.centerx, self.rect.top)
            playerBullet_group.add(bullet)
            self.last_shot = pygame.time.get_ticks()

        return gameover

def create_invader_bullet():
    attacking_invader = random.choice(invaders_group.sprites())
    invaderBullet = invader_bullet(attacking_invader.rect.centerx, attacking_invader.rect.centery)
    invaderBullet_group.add(invaderBullet)

def create_invaders():
    for row in range(rows):
        for col in range(cols):
            invader = Invader(100 + col * 65, 80 + row * 50)
            invaders_group.add(invader)
create_invaders()

player = Player(int(window_width/2), window_height - 100)
player_group.add(player)


game = True
while game:
    clock.tick(60)
    screen.blit(background, (0,0))
    if len(invaders_group) == 0:
        game_over = 1

    if game_over == 0:
        seconds = (pygame.time.get_ticks() - timer) / 1000
        if seconds > 5:
            create_invader_bullet()
            timer = pygame.time.get_ticks()

        invaders_group.update()
        player_group.update()
        invaderBullet_group.update()
        playerBullet_group.update()

        invaders_group.draw(screen)
        player_group.draw(screen)
        invaderBullet_group.draw(screen)
        playerBullet_group.draw(screen)
        game_over = player.update()

    elif game_over == 1:
        background = gameover

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        pygame.display.update()
        
pygame.quit()