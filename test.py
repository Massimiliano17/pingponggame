# Разработай свою игру в этом файле!
from pygame import *
init()
class  GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_picture, player_w, player_h, player_x, player_y):
        super().__init__(player_picture, player_w, player_h, player_x, player_y)
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        if self.rect.x <= width - 80 and self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
        walls_touched = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)
        
        if self.rect.y <= height - 80 and self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y
        walls_touched = sprite.spritecollide(self, walls, False)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)

class Enemy(Player):
    def move(self):
        self.rect.x += self.speed_x
        walls_touched = sprite.spritecollide(self, walls, False)
        if walls_touched != []:
            self.speed_x *= -1
        if enemy.rect.x > 620:
            self.speed_x *= -1

width = 700
height = 500

background = transform.scale(image.load("background.jpg"), (width, height))
window = display.set_mode((width, height))
display.set_caption("Лабиринт")
run = True

player = Player("ronaldo.png", 80, 80, 80, 400)
enemy = Enemy("messi.png", 80, 80, 610, 300)
enemy.speed_x = -5
final_sprite = GameSprite("ballon d'or.png", 80,80, 620, 420)

walls = sprite.Group()
wall1 = GameSprite("water.jpg", 400, 100, 100, 150)
wall2 = GameSprite("water.jpg", 100, 370, 300, 250)
walls.add(wall1)
walls.add(wall2)

finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.speed_x = -5
            elif e.key == K_RIGHT:
                player.speed_x = 5
            elif e.key == K_UP:
                player.speed_y = -5
            elif e.key == K_DOWN:
                player.speed_y = 5
        if e.type == KEYUP:
            if e.key == K_LEFT:
                player.speed_x = 0
            elif e.key == K_RIGHT:
                player.speed_x = 0
            elif e.key == K_UP:
                player.speed_y = 0
            elif e.key == K_DOWN:
                player.speed_y = 0
    if not finish:
        window.blit(background, (0,0)) 
        player.reset()
        enemy.reset()
        final_sprite.reset()
        wall2.reset()       
        wall1.reset()
        player.update()
        enemy.move()
        if sprite.collide_rect(player, enemy):
            finish = True
            img = transform.scale(image.load("lose.jpg"), (width, height)) #Поражение
            s = mixer.Sound("ankaramessi.ogg")
            s.play()
            window.blit(img, (0,0))
        if sprite.collide_rect(player, final_sprite):
            finish = True
            img = transform.scale(image.load("win.jpg"), (width, height)) #Победа
            s = mixer.Sound("sui.ogg")
            s.play()
            window.blit(img, (0,0))
    display.update()