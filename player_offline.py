import pygame
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 1000,640
FPS = 60
Player_jump = 6
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join ("assets",dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0 ,width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites   
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheet("character","Blue", 48, 48, True)
    ANIMATION_DELAY = 6
    def __init__(self, x, y, width, height, lives):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.lives = lives
        self.isDead = False
        self.after_death = 0

    #nhay
    def jump(self):
        self.y_vel = -self.GRAVITY * 7
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    # Di chuyển
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    # di chuyển sang trái
    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    # di chuyển sang phải
    def move_right(self,vel):   
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    # lập lại theo khung hình
    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    # Đứng trên block
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    # đụng đầu
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    # Cập nhật Sprite
    def update_sprite(self):
        sprite_sheet = "idle"
        # Kiểm tra trạng thái của nhân vật để chọn sprite phù hợp
        if self.y_vel < 0:
            sprite_sheet = "jump"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        elif self.isDead == True:
            if self.after_death > 12:
                sprite_sheet = "after_death"
            else:
                sprite_sheet = "death"
                self.after_death = self.after_death + 1

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        # pygame.draw.rect(win, self.COLOR, self.rect)
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite,(self.rect.x, self.rect.y))
