import pygame
import sys
import Soldier_Shooter
import subprocess
import os
import time
# Khởi tạo Pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# Cỡ chữ
FONT_SIZE = 40

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 600
WINDOW_SIZE = (WIDTH, HEIGHT)

theme_sound = pygame.mixer.Sound("assets/sound/result.mp3")

background_image = pygame.image.load("assets/Background/Loading_Screen.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# Tạo cửa sổ
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game Menu")

# Tạo font
title_font = pygame.font.Font("assets/font/anta.ttf", 90)
font = pygame.font.Font("assets/font/anta.ttf", FONT_SIZE)

# Hàm vẽ nút
def draw_button(text, color, rect):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_title(text):
    text_surface = title_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text_surface, text_rect)

# Hàm chính
def main(title):
    theme_sound.play()
    screen.blit(background_image, (0, 0))
    continue_rect = pygame.Rect(350, 400, 300, 50)

    while True:
        # screen.fill(DARK_BLUE)
        draw_title(title)
        # Lấy vị trí chuột
        mouse_pos = pygame.mouse.get_pos()

        # Kiểm tra nút online
        if continue_rect.collidepoint(mouse_pos):
            draw_button("Continue", GRAY, continue_rect)
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem nút chuột trái có được nhấn không
                theme_sound.stop()
                # Soldier_Shooter.main_menu()
                subprocess.Popen(["python", "Soldier_Shooter.py"])
                time.sleep(1)
                pygame.quit()
                sys.exit()
        else:
            draw_button("Continue", WHITE, continue_rect)


        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            break

        # Cập nhật màn hình
        pygame.display.flip()


# # # Chạy chương trình
# if __name__ == "__main__":
#     main("aaaa")
