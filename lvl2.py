from pygame import *
import math
import random
font.init()
mixer.init()
win_width=1080
win_height=720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
display.set_caption('Hotline Zhytomyr')
window = display.set_mode((win_width, win_height))
back=image.load('ground.jpg')
back2=image.load('ground2.jpg')
back2=image.load('ground3.jpg')

back=transform.scale(back,(win_width, win_height))
back2=transform.scale(back,(win_width, win_height))
back3=transform.scale(back,(win_width, win_height))

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Button:
    def __init__(self, x, y, width, height, color, text='', text_color=(0, 0, 0), font_size=32):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font.Font(None, font_size)
    
    def draw(self, surface):
        draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Mc(GameSprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed, pos): 
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed=player_x_speed
        self.y_speed=player_y_speed
        self.original_image = image.load('hero.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (player_x, player_y))
    def update(self):
        if gg.rect.x <= win_width-80 and gg.x_speed > 0 or gg.rect.x >= 0 and gg.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if gg.rect.y <= win_height-80 and gg.y_speed > 0 or gg.rect.y >= 0 and gg.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

        if gg.rect.x <= win_width-80 and gg.x_speed > 0 or gg.rect.x >= 0 and gg.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched2 = sprite.spritecollide(self, barriers2, False)
        if self.x_speed > 0:
            for p in platforms_touched2:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched2:
                self.rect.left = max(self.rect.left, p.rect.right)
        if gg.rect.y <= win_height-80 and gg.y_speed > 0 or gg.rect.y >= 0 and gg.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched2 = sprite.spritecollide(self, barriers2, False)
        if self.y_speed > 0:
            for p in platforms_touched2:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def rotate(self, player_x, player_y):
        direction = Vector2(player_x, player_y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self, mousepos):
        dx = mousepos[0] - self.rect.centerx
        dy = mousepos[1] - self.rect.centery
        if abs(dx) > 0 or abs(dy) > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, image_path, x, y, size_x, size_y, speed, right_distance, down_distance, left_distance, up_distance):
        super().__init__(image_path, x, y, size_x, size_y)
        self.speed = speed
        self.right_distance = right_distance
        self.down_distance = down_distance
        self.left_distance = left_distance
        self.up_distance = up_distance
        self.direction = "right"
        self.distance_left = right_distance

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
            self.distance_left -= self.speed
            if self.distance_left <= 0:
                self.distance_left = self.down_distance
                self.direction = "down"
        elif self.direction == "down":
            self.rect.y += self.speed
            self.distance_left -= self.speed
            if self.distance_left <= 0:
                self.distance_left = self.left_distance
                self.direction = "left"
        elif self.direction == "left":
            self.rect.x -= self.speed
            self.distance_left -= self.speed
            if self.distance_left <= 0:
                self.distance_left = self.up_distance
                self.direction = "up"
        elif self.direction == "up":
            self.rect.y -= self.speed
            self.distance_left -= self.speed
            if self.distance_left <= 0:
                self.distance_left = self.right_distance
                self.direction = "right"
            

class Bullet(GameSprite):
    def __init__(self, x, y, dx, dy):
        sprite.Sprite.__init__(self)
        self.image = transform.smoothscale(image.load('bullet.png').convert_alpha(), (7,7))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 100
        self.pos = Vector2(x, y)
        self.dir = Vector2(dx, dy).normalize()
    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

BLACK = (255, 255, 255)

move_sound = mixer.Sound("walk_grass.wav")
shot = mixer.Sound("shot.wav")

speed = 2
barriers = sprite.Group()
barriers2 = sprite.Group()
barriers3 = sprite.Group()
bullets = sprite.Group()
bad = sprite.Group()
bad2 = sprite.Group()
bad3 = sprite.Group()


car1=GameSprite('car1.png', 650, 270, 250, 120)
car2=GameSprite('car2.png', 400, 60, 250, 120)
car3=GameSprite('car3.png', 320, 190, 100, 170)
car4=GameSprite('car4.png', 700, 400, 150, 270)
car5=GameSprite('car5.png', 40, 350, 300, 170)

wall1=GameSprite('wall_v.jpg', 150, 400, 30, 500)
wall2=GameSprite('wall.jpg', 400, 60, 250, 40)
wall3=GameSprite('wall_v.jpg', 320, 190, 40, 270)
wall4=GameSprite('wall_v.jpg', 820, 190, 40, 270)

wall5=GameSprite('wall3.jpg', 520, 0, 40, 270)
wall6=GameSprite('wall3.jpg', 320, 220, 40, 270)
wall7=GameSprite('wall3.jpg', 620, 390, 40, 270)
wall8=GameSprite('tank.png', 720, 0, 600, 250)

barriers.add(car1)
barriers.add(car2)
barriers.add(car3)
barriers.add(car4)
barriers.add(car5)

gg = Mc('hero.png', 80, win_height - 80, 80, 80, 0, 0, 220)
enemy = Enemy('enemy.png', 650, 100, 70, 80, 10, 300, 100, 300, 100)
enemy1 = Enemy('enemy.png', 320, 390, 70, 80, 15, 300, 200, 300, 200)
enemy3 = Enemy('enemy.png', 360, 180, 70, 80, 20, 300, 300, 300, 300)
enemy4 = Enemy('enemy.png', 200, 600, 70, 80, 25, 600, 0, 600, 0)
enemy5 = Enemy('mil.png', 400, 180, 70, 80, 20, 0, 300, 0, 300)
enemy6 = Enemy('mil.png', 750, 380, 70, 80, 20, 200, 200, 200, 200)
enemy7 = Enemy('mil.png', 100, 100, 70, 80, 25, 100, 600, 100, 600)
endup = GameSprite('gpu.png', win_width - 85, 200, 40, 20)
endup2 = GameSprite('gpu.png', 80, 200, 40, 20)
endup3 = GameSprite('gpu.png', 900, 600, 40, 20)

bad.add(enemy)
bad.add(enemy1)
bad2.add(enemy3)
bad2.add(enemy4)
bad3.add(enemy5)
bad3.add(enemy6)
bad3.add(enemy7)
b1=Button(500, 100, 100, 50, WHITE, 'Play')
b2=Button(500, 300, 100, 50, WHITE, 'Options')
b3=Button(500, 500, 100, 50, WHITE, 'Quit')

b4=Button(500, 100, 100, 50, WHITE, 'LEVEL 1')
b5=Button(500, 300, 100, 50, WHITE, 'LEVEL 2')
b6=Button(500, 500, 100, 50, WHITE, 'LEVEL 3')

b7=Button(500, 500, 100, 50, WHITE, 'Back')
b8=Button(500, 300, 100, 50, WHITE, '+')
b9=Button(500, 100, 100, 50, WHITE, '-')

left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
sound_on = False
st_m=0
lvl=0
finish = False
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
                run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                st_m=0
        if st_m == 0:
            if e.type == QUIT:
                    run = False
            elif e.type == MOUSEBUTTONDOWN:
                if b1.rect.collidepoint(mouse.get_pos()):
                    st_m=1
                elif b2.rect.collidepoint(mouse.get_pos()):
                    st_m=2
                elif b3.rect.collidepoint(mouse.get_pos()):
                    run = False
            if not finish:
                window.fill((0, 0, 0))
                window.blit(window, (0, 0))
                b1.draw(window)
                b2.draw(window)
                b3.draw(window)
                time.delay(24)
                display.update()
        elif st_m == 1:
            if e.type == QUIT:
                    run = False
            elif e.type == MOUSEBUTTONDOWN:
                if b4.rect.collidepoint(mouse.get_pos()):
                    st_m=4
                    lvl=1
                elif b5.rect.collidepoint(mouse.get_pos()):
                    st_m=4
                    lvl=2
                elif b6.rect.collidepoint(mouse.get_pos()):
                    st_m = 4
                    lvl=3
            if not finish:
                window.blit(window, (0, 0))
                b4.draw(window)
                b5.draw(window)
                b6.draw(window)
                time.delay(24)
                display.update()
        elif st_m == 2:
            if e.type == QUIT:
                    run = False
            elif e.type == MOUSEBUTTONDOWN:
                if b7.rect.collidepoint(mouse.get_pos()):
                    st_m = 0
                elif b8.rect.collidepoint(mouse.get_pos()):
                    print('')
                elif b9.rect.collidepoint(mouse.get_pos()):
                    print('')
            if not finish:
                window.blit(window, (0, 0))
                b7.draw(window)
                b8.draw(window)
                b9.draw(window)
                time.delay(24)
                display.update()
        elif st_m == 4:
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_a:
                    left_pressed = True
                    if not sound_on:
                        move_sound.play(-1)
                        sound_on = True
                elif e.key == K_d:
                    right_pressed = True
                    if not sound_on:
                        move_sound.play(-1)
                        sound_on = True
                elif e.key == K_w:
                    up_pressed = True
                    if not sound_on:
                        move_sound.play(-1)
                        sound_on = True
                elif e.key == K_s:
                    down_pressed = True
                    if not sound_on:
                        move_sound.play(-1)
                        sound_on = True
            elif e.type == KEYUP:
                if e.key == K_a:
                    left_pressed = False
                    if sound_on and (up_pressed or right_pressed or down_pressed):
                        pass
                    elif sound_on and (not up_pressed or not right_pressed or not down_pressed):
                        move_sound.stop()
                        sound_on = False
                elif e.key == K_d:
                    right_pressed = False
                    if sound_on and (up_pressed or right_pressed or left_pressed):
                        pass
                    elif sound_on and (not up_pressed or not right_pressed or not left_pressed):
                        move_sound.stop()
                        sound_on = False
                elif e.key == K_w:
                    up_pressed = False
                    if sound_on and (left_pressed or right_pressed or down_pressed):
                        pass
                    elif sound_on and (not left_pressed or not right_pressed or not down_pressed):
                        move_sound.stop()
                        sound_on = False
                elif e.key == K_s:
                    down_pressed = False
                    if sound_on and (up_pressed or right_pressed or left_pressed):
                        pass
                    elif sound_on and (not up_pressed or not right_pressed or not left_pressed):
                        move_sound.stop()
                        sound_on = False
                while e.key == K_a and e.key == K_d and e.key == K_w and e.key == K_s:
                    sound = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    gg.fire(mouse.get_pos())
                    shot.play()
            gg.rotate(*mouse.get_pos())
            gg.x_speed = (right_pressed - left_pressed) * speed
            gg.y_speed = (down_pressed - up_pressed) * speed
    if st_m == 4:
        if not finish:
            
            if lvl==1:
                window.blit(back, (0, 0))
                barriers.draw(window)
                bad.update()
                bad.draw(window)
                endup.reset()
                sprite.groupcollide(bullets, barriers, True, False)
                if sprite.spritecollide(gg, bad, True):
                    finish=True
                    img = image.load('go.png')
                    d = img.get_width() // img.get_height()
                    window.fill((255, 255, 255))
                    window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
                sprite.groupcollide(bad, bullets, True, True)
                if sprite.collide_rect(gg, endup):
                    lvl=2
            elif lvl==2:
                back=image.load('ground2.jpg')
                window.blit(back, (0, 0))
                barriers.empty()
                bad.empty()
                barriers2.add(wall1)
                barriers2.add(wall2)
                barriers2.add(wall3)
                barriers2.add(wall4)
                barriers2.draw(window)
                endup2.reset()
                bad2.update()
                bad2.draw(window)
                sprite.groupcollide(bullets, barriers2, True, False)
                if sprite.spritecollide(gg, bad2, True):
                    finish=True
                    img = image.load('go.png')
                    d = img.get_width() // img.get_height()
                    window.fill((255, 255, 255))
                    window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
                sprite.groupcollide(bad2, bullets, True, True)
                if sprite.collide_rect(gg, endup2):
                    lvl=3
            elif lvl==3:
                back=image.load('ground3.jpg')
                back=transform.scale(back,(win_width, win_height))
                window.blit(back, (0, 0))
                barriers.empty()
                bad.empty()
                barriers2.empty()
                bad2.empty()
                barriers3.add(wall5)
                barriers3.add(wall6)
                barriers3.add(wall7)
                barriers3.add(wall8)
                barriers3.draw(window)
                endup3.reset()
                bad3.update()
                bad3.draw(window)
                sprite.groupcollide(bullets, barriers3, True, False)
                if sprite.spritecollide(gg, bad3, True):
                    finish=True
                    img = image.load('go.png')
                    d = img.get_width() // img.get_height()
                    window.fill((255, 255, 255))
                    window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
                sprite.groupcollide(bad3, bullets, True, True)
                if sprite.collide_rect(gg, endup3):
                    finish = True
                    img = image.load('win.png')
                    window.fill((255, 255, 255))
                    window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            bullets.update()
            bullets.draw(window)
            gg.reset()
            gg.update()
            time.delay(24)
            display.update()