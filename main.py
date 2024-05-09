import pygame
import sys
import os

from pygame.math import Vector2
# Class nhân vật
class Soldier(pygame.sprite.Sprite):
    # Khởi tạo
    def __init__(self,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.isAlive = True
        self.speed = speed
        self.velocity_y = 0

        self.isJump = False
        self.isIn_air = False
        self.isMove_left = False
        self.isMove_right = False
        self.isFlip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0

        self.update_time = pygame.time.get_ticks()
        # Animation
        animation_type = ['Idle','Run','Jump']
        for animation in animation_type:
            num_of_animations = os.listdir(f'assets/images/player/{animation}')
            temp_list = []
            for i in range(len(num_of_animations)):
                characterImage = pygame.image.load(f'assets/images/player/{animation}/{i}.png')
                characterImage = pygame.transform.scale(characterImage,(characterImage.get_width()*scale, characterImage.get_height()*scale))
                temp_list.append(characterImage)
            self.animation_list.append(temp_list)

        self.characterImage = self.animation_list[self.action][self.frame_index]
        self.rect = self.characterImage.get_rect()
        self.rect.center = (x,y)
    # Di chuyển
    def move (self):
        # Độ thay đổi
        dx = 0
        dy = 0
        # Sang trái hay phải
        if self.isMove_left:
            dx = -self.speed
            self.isFlip = True
        if self.isMove_right:
            dx = self.speed
            self.isFlip = False
        # Nhảy
        if self.isJump and self.isIn_air == False:
            self.velocity_y = -11
            self.isJump = False
            self.isIn_air = True
        # Trọng lực
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y = 10
        dy += self.velocity_y
        # Collision
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.isIn_air = False
        # Update vị trí
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.characterImage = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index =0
            self.update_time = pygame.time.get_ticks()
    # Vẽ UI
    def draw(self):
        screen.blit(pygame.transform.flip(self.characterImage, self.isFlip, False), self.rect)
# Tạo ng chơi     
player = Soldier(200,200,3,5)
# Trọng lực
GRAVITY = 0.75
# Cấu hình cửa sổ game
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ConTra")
# FPS
clock = pygame.time.Clock()
FPS = 60
# Đọc hình ảnh cho biểu tượng
#icon_image = pygame.image.load("assets/images/TankRed_FullCase.png")  # Đường dẫn tới hình ảnh biểu tượng
#pygame.display.set_icon(icon_image)
#Màu
BACKGROUND = (144, 201, 120)
RED = (255, 0, 0)
def draw_bg(BG):
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0,300), (screen_width, 300))
# Hàm main chính
def main():
    # Khởi tạo pygame
    pygame.init()
    # Vòng lặp chính của trò chơi
    run = True;
    while run:
        clock.tick(FPS)

        draw_bg(BACKGROUND)
        player.update_animation()
        player.draw()
        if player.isAlive:
            if player.isIn_air:
                player.update_action(2)
            elif player.isMove_left or player.isMove_right:
                player.update_action(1)
            else:
                player.update_action(0)
            player.move()
        # Xử lý sự kiện
        for event in pygame.event.get():
            # Thoát game
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.isMove_left = True
                if event.key == pygame.K_d:
                    player.isMove_right = True
                if event.key == pygame.K_w:
                    player.isJump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.isMove_left = False
                if event.key == pygame.K_d:
                    player.isMove_right = False

        pygame.display.update()


# Kiểm tra xem script được chạy trực tiếp hay được import từ một module khác
if __name__ == "__main__":
    main() 