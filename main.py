import pygame
import sys
from network import Network
from player import Player


from pygame.math import Vector2

# Tạo ng chơi     
player = Player(200,200,3,5)
# Trọng lực

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
    run = True
    # n = Network() 
    
    while run:
        clock.tick(FPS)

        draw_bg(BACKGROUND)
        player.update_animation()
        player.draw(screen)
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