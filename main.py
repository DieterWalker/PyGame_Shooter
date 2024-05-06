import pygame
import sys
from pygame.math import Vector2
# Hàm main chính
def main():
    # Khởi tạo pygame
    pygame.init()

    # Cấu hình cửa sổ game
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tank Attack")

    x = 32
    y = 32
    vel = 0.25

    tank_angle = 0
    turret_angle = 0
    tank_direction = Vector2(0, 1)
    
# Đọc hình ảnh cho biểu tượng
    icon_image = pygame.image.load("assets/images/TankRed_FullCase.png")  # Đường dẫn tới hình ảnh biểu tượng
    pygame.display.set_icon(icon_image)

    # Khởi tạo đối tượng Game

    tank_image = pygame.image.load("assets/images/TankBase_Red.png")
    turret_image = pygame.image.load("assets/images/TankTurret_Red.png")
    bullet_image = pygame.image.load("assets/images/TankBullet_Red.png")

    bullets = []
    bullet_speed = 1.0

    font = pygame.font.SysFont(None, 24)
    # Vòng lặp chính của trò chơi
    while True:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Tạo đạn mới
                    bullet = {
                        'pos': Vector2(x, y),  # Vị trí xuất phát của đạn là vị trí hiện tại của tháp tank
                        'dir': tank_direction,  # Hướssssng của đạn là hướng của tháp tank
                    }
                    bullets.append(bullet)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # x -= vel
            tank_angle += 0.25
            turret_angle += 0.25
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # x += vel
            turret_angle -= 0.25
            tank_angle -= 0.25
        if keys[pygame.K_q]:
            turret_angle -= 0.25
        if keys[pygame.K_e]:
            turret_angle += 0.25

        tank_direction = Vector2(0, -1).rotate(tank_angle)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            x -= vel * tank_direction.x
            y += vel * tank_direction.y
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            x += vel * tank_direction.x
            y -= vel * tank_direction.y
        
        for bullet in bullets:
            bullet['pos'] += bullet['dir'] * bullet_speed
            # Kiểm tra nếu viên đạn ra khỏi màn hình thì loại bỏ nó khỏi danh sách
            if bullet['pos'].x < 0 or bullet['pos'].x > screen_width or bullet['pos'].y < 0 or bullet['pos'].y > screen_height:
                bullets.remove(bullet)
        

        screen.fill((0, 0, 0))
        rotated_tank = pygame.transform.rotate(tank_image, tank_angle)
        screen.blit(rotated_tank, (x, y))
        
        rotated_turret = pygame.transform.rotate(turret_image, turret_angle)
        turret_pos = Vector2(x, y) + Vector2(rotated_tank.get_rect().center)
        screen.blit(rotated_turret, rotated_turret.get_rect(center=turret_pos))        
                    
        # text_surface = font.render(f'X: {x}, Y: {y}', True, (255, 255, 255))
        # # Vẽ văn bản lên màn hình
        # screen.blit(text_surface, (10, 10))
        for bullet in bullets:
            screen.blit(bullet_image, bullet['pos'])
        # pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        pygame.display.update()


# Kiểm tra xem script được chạy trực tiếp hay được import từ một module khác
if __name__ == "__main__":
    main() 