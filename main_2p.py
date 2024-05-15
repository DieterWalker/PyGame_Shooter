import os
import random
import math
import pygame
import player_offline
import player_offline_2
import map
import item
import datetime
import offline_result
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 600
PLAYER_VEL = 5
FPS = 60

speed_shoot_1 = 500
speed_shoot_2 = 500
# Máu người chơi
player1_lives = 1
player2_lives = 1

# Thiết lập cấu hình âm thanh
theme_sound = pygame.mixer.Sound("assets/sound/theme_1.mp3")
jump_sound = pygame.mixer.Sound("assets/sound/jump.mp3")
shot_sound = pygame.mixer.Sound("assets/sound/shot.mp3")

font_path = "assets/font/anta.ttf"
font_info = pygame.font.Font(font_path, 30)
window = pygame.display.set_mode((WIDTH, HEIGHT))
# =========================== load_map==========================
# Mãng mapdư
maps_array = [
    {"bg_image": "Blue.png", 
     "floor": [
            (48*0, 244), (48*1, 244), (48*2, 244), (48*18, 244), (48*19, 244),(48*20, 244),
            # (48*3, 340), (48*4, 340), (48*16, 340),(48*17, 340),
            (48*7, 436), (48*8, 436), (48*9, 436),(48*10, 436),  (48*11, 436),(48*12, 436), (48*13, 436),
            (48*0, 532), (48*1, 532), (48*19, 532),(48*20, 532),
            (48*0, 580), (48*1, 580), (48*2, 580),(48*3, 580), (48*4, 580), (48*5, 580),
            (48*6, 580), (48*7, 580), (48*8, 580),(48*9, 580), (48*10, 580), (48*11, 580),
            (48*12, 580), (48*13, 580), (48*14, 580),(48*15, 580), (48*16, 580), (48*17, 580),
            (48*18, 580), (48*19, 580), (48*20, 580)],
        "block_y": 0},
]

# Tải dữ liệu map
def load_map(block_size, map_info):
    background_image_path = map_info["bg_image"]
    custom_coordinates = map_info["floor"]
    block_y = map_info.get("block_y", 0)
    background, bg_image = map.get_background(background_image_path)
    floor = [map.Block(x, y, block_size,block_y) for x, y in custom_coordinates]
    return background, bg_image, floor
# ===========================Background=========================
def get_background(name):
    image =  pygame.image.load(join("assets","Background",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image
#=========================Window Panel=========================#
# player 1
def draw_info_panel(window, player):
    # Thiết lập kích thước và màu sắc cho panel
    panel_height = 70
    panel_width = 180
    panel_color = (135, 206, 235, 150)  # Màu xanh da trời với độ trong suốt
    
    # Tạo một surface mới cho panel thông tin
    info_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    info_panel.fill(panel_color)
    
    # Thiết lập font và màu sắc cho text
    font_color = (50, 50, 50)  # Màu trắng

    image_heart = pygame.image.load("assets/Hearth_Simple.png")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image_heart = pygame.transform.scale(image_heart, (48, 48))
    # Vẽ thông tin lên panel
    lives_text = font_info.render(" x " + str(player.lives), True, font_color)

    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (60, 20))
    info_panel.blit(image_heart, (10, 10))
    
    # Vẽ panel lên window
    window.blit(info_panel, (5, 0))  # Bạn có thể thay đổi vị trí này tùy ý
# player2
def draw_info_panel2(window, player):
    # Thiết lập kích thước và màu sắc cho panel
    panel_height = 70
    panel_width = 180
    panel_color = (255, 155, 155, 150)  
    
    # Tạo một surface mới cho panel thông tin
    info_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    info_panel.fill(panel_color)
    
    # Thiết lập font và màu sắc cho text
    font_color = (50, 50, 50)  # Màu trắng

    image_heart = pygame.image.load("assets/Hearth_Simple_2.png")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image_heart = pygame.transform.scale(image_heart, (48, 48))
    # Vẽ thông tin lên panel
    lives_text = font_info.render(str(player.lives) + " x ", True, font_color)

    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (50, 20))
    info_panel.blit(image_heart, (130, 10))
    
    # Vẽ panel lên window
    window.blit(info_panel, (820, 0))  # Bạn có thể thay đổi vị trí này tùy ý
#==========================Draw================================#
def draw(window, background, bg_image, player, objects, player2, player_bullet1, player_bullet2):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    for bullet1 in player_bullet1:
        bullet1.draw(window)

    for bullet2 in player_bullet2:
        bullet2.draw(window)

    player.draw(window)
    player2.draw(window)
    draw_info_panel(window,player)
    draw_info_panel2(window,player2)
    pygame.display.update()
# =========================Handle_move==========================/
# Điều khiển người chơi 1
def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
   
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)
    player.rect.clamp_ip(window.get_rect())

# Điều khiển người chơi 2
def handle_move_2(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
   
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)
    player.rect.clamp_ip(window.get_rect())

# Check Collision
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            # elif dy < 0:
            #     player.rect.top = obj.rect.bottom
            #     player.hit_head()
        
        collided_objects.append(obj)
    return collided_objects
#===========================Player Shoot========================
# player 1
def playerShoot(player, bullets):
    initial_speed = 15
    speed_increment = 1
    if player.direction == "left":
        bullet = item.Bullet(player.rect.left, player.rect.top + 40, 32, 32,"bullet")
        bullet.x_vel = -initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang trái
    elif player.direction == "right":
        bullet = item.Bullet(player.rect.right, player.rect.top + 40, 32, 32,"bullet")
        bullet.x_vel = initial_speed   # Thiết lập vận tốc ban đầu của quả táo khi ném sang phải

    initial_speed += speed_increment
    bullets.append(bullet)
#===========================Main==== ===========================#
def main(window):
    theme_sound.play(-1)
    global player1_lives, player2_lives
    clock = pygame.time.Clock()

    block_size = 48
    random_map_info = random.choice(maps_array)
    background, bg_image, floor = load_map(block_size, random_map_info)
    player = player_offline.Player(100, 100, 48, 48, player1_lives)
    player2 = player_offline_2.Player(600, 100, 48, 48, player2_lives)
    input_visible = False

    # xét các nhân vật đang bắn
    is_shoot = False
    is_jumping = False
    can_shoot1 = True
    can_shoot2 = True
    # thời gian bắn
    # current_time = datetime.datetime.now()
    shot_time1 = datetime.datetime.now()
    shot_time2 = datetime.datetime.now()
    last_shoot_time = pygame.time.get_ticks()

    # Đạn của người chơi
    bullet1 = []
    bullet2 = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and player.jump_count < 1:
                    player.jump() 
                    is_jumping = True
                elif event.key == pygame.K_UP and player2.jump_count < 1:
                    is_jumping = True
                    player2.jump() 
                elif event.key == pygame.K_SPACE:
                    shot_time1 = pygame.time.get_ticks()
                    if can_shoot1 and not input_visible:
                        playerShoot(player,bullet1)
                        last_shoot_time = shot_time1
                        is_shoot = True
                        can_shoot1 = False
                elif event.key == pygame.K_RETURN:
                    shot_time2 = pygame.time.get_ticks()
                    if can_shoot2 and not input_visible:
                        playerShoot(player2,bullet2)
                        last_shoot_time = shot_time2
                        is_shoot = True
                        can_shoot2 = False
        
        if is_jumping:
            jump_sound.play()
            is_jumping = False
        
        if is_shoot:
            shot_sound.play()
            is_shoot = False

        # Kiểm tra nạp đạn
        if not can_shoot2:
            shot_time2 = pygame.time.get_ticks()
            if shot_time2 - last_shoot_time >= speed_shoot_2:
                can_shoot2 = True

        if not can_shoot1:
            shot_time1 = pygame.time.get_ticks()
            if shot_time1 - last_shoot_time >= speed_shoot_1:
                can_shoot1 = True
            
        # Cập nhật vị trí    
        player.loop(FPS)
        player2.loop(FPS)
        handle_move(player, floor)
        handle_move_2(player2, floor)
        # vẽ
        draw(window, background, bg_image, player, floor, player2, bullet1, bullet2)
        # kiểm tra đạn có tồn tại không
        for bullet in bullet1:
            bullet.rect.x += bullet.x_vel
            bullet.rect.y += bullet.y_vel
            if bullet.rect.right < 0 or bullet.rect.left > WIDTH:
                bullet1.remove(bullet)
            if bullet.rect.colliderect(player2.rect):
                if player2_lives > 1:
                    player2_lives -= 1
                else:
                    player2_lives = 0
                    player2.isDead = True
                    theme_sound.stop()
                    offline_result.main("Blue Player Win")
                bullet1.remove(bullet)
                pygame.display.update()
        player2.lives = player2_lives

        for bullet in bullet2:
            bullet.rect.x += bullet.x_vel
            bullet.rect.y += bullet.y_vel
            if bullet.rect.right < 0 or bullet.rect.left > WIDTH:
                bullet2.remove(bullet)
            if bullet.rect.colliderect(player.rect):
                if player1_lives > 1:
                    player1_lives -= 1
                else:
                    player1_lives = 0
                    player.isDead = True
                    theme_sound.stop()
                    offline_result.main("Red Player Win")
                bullet2.remove(bullet)
                pygame.display.update()
        player.lives = player1_lives

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)