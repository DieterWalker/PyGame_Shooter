import os
import random
import math
import sys
import socket
import pygame
import player_online
import player_online_2
import map
import item
import time
import datetime
import threading
import builtins
import map
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
max_life = 10
player1_lives = max_life
player2_lives = max_life

theme_sound = pygame.mixer.Sound("assets/sound/theme_1.mp3")
jump_sound = pygame.mixer.Sound("assets/sound/jump.mp3")
shot_sound = pygame.mixer.Sound("assets/sound/shot.mp3")

font_path = "assets/font/anta.ttf"
font_info = pygame.font.Font(font_path, 30)

#màn hình chờ
wait_image = pygame.image.load("assets/Background/Loading_Screen.jpg")  # Thay đổi đường dẫn tới ảnh của bạn
wait_image = pygame.transform.scale(wait_image, (WIDTH, HEIGHT))

window = pygame.display.set_mode((WIDTH, HEIGHT))
client_count = 0
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        send_thread_a = threading.Thread(target=send_coordinate, args=(player.rect.x,player.rect.y))
        send_thread_a.start()
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)
        send_thread_d = threading.Thread(target=send_coordinate, args=(player.rect.x,player.rect.y))
        send_thread_d.start()

    handle_vertical_collision(player, objects, player.y_vel)
    player.rect.clamp_ip(window.get_rect())

# Điều khiển người chơi 2
def handle_move_2(player, objects):
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
#==============================socket============================
# Kết nối đến server
def connect_to_server(server_ip, server_port):
    try:
        client_socket.connect((server_ip, server_port))
        print("Kết nối thành công!")
    except Exception as e:
        print("Không thể kết nối đến server:", e)
        sys.exit(1) 

# Đóng kết nối
def close_connection():
    client_socket.close()

# Gửi dữ liệu vị trí player
def send_coordinate(player_x,player_y):
    data = f"COORD:{player_x} {player_y}|"
    client_socket.send(data.encode())

# Gửi dữ liệu vị trí viên đạn 
def send_coordinate_bullet(bullet_x,bullet_y):
    data = f"SHOOT:{bullet_x} {bullet_y}|"
    client_socket.send(data.encode())

# Gửi dữ liệu sprite
def send_sprite_info(sprite_name):
    sprite_info = f"SPRITE:{sprite_name}|"
    client_socket.send(sprite_info.encode())

def send_player_direction(direction):
    direction_data = f"CDR:{direction}|"
    client_socket.send(direction_data.encode())

# def send_player_number(player_number):
#     number = f"SERVER:{player_number}|"
#     client_socket.send(number.encode())

def send_player_hp(hp1):
    direction_data = f"CLIVE:{hp1}|"
    client_socket.send(direction_data.encode())
# Nhận dữ liệu
def receive_thread(player2, bullet2):
    data = client_socket.recv(2048).decode().split('\n')
    result = []
    global player1_lives
    global client_count 
    for line in data:
        parts = []
        current_part = ''
        for char in line:
            if char == 'C' or char == 'S'or char == 'A': 
                if current_part:
                    parts.append(current_part)
                current_part = char
            else:
                current_part += char
        if current_part:
            parts.append(current_part)
        result.append(parts)
    for group in result:
        for item in group:
            if item.startswith("SERVER:"):
                data = item[7:] 
                x = data.rstrip('|').split()
                if x and x[0].isdigit():
                    client_count = int(x[0])
            elif item.startswith("COORD:"):
                data = item[6:] 
                print(data)
                x, y = builtins.map(int, data.rstrip('|').split())
                player2.rect.x, player2.rect.y = x, y
            elif item.startswith("CLIVE:"):
                data = item[6:] 
                x = data.rstrip('|').split()
                if x and x[0].isdigit():
                    player1_lives = int(x[0])
            elif item.startswith("CDR:"):
                direction = item[4:].rstrip('|')
                player2.direction = direction 
            elif item.startswith("SPRITE:"):
                sprite = item[7:].rstrip('|')
                player2.sprite_name = sprite
            elif item.startswith("SHOOT:"):
                coord_data = item[6:]
                x, y = builtins.map(int, coord_data.rstrip('|').split())
                if coord_data is not None:
                    playerShoot(player2, bullet2)

def receive_client_count_from_server():
    global client_count  # Đảm bảo rằng biến count được gọi từ phạm vi toàn cục
    result = []
    while True:
        try:
            client_count_data = client_socket.recv(2048).decode()
            # print(client_count_data)

            if not client_count_data:
                break
            for line in client_count_data:
                parts = []
                current_part = ''
                for char in line:
                    if char == 'C' or char == 'S'or char == 'A': 
                        if current_part:
                            parts.append(current_part)
                        current_part = char
                    else:
                        current_part += char
                if current_part:
                    parts.append(current_part)
                result.append(parts)
            for group in result:
                for item in group:
                    if item.startswith("SERVER:"):
                        data = item[7:] 
                        x = data.rstrip('|').split()
                        if x and x[0].isdigit():
                            client_count = int(x[0])
            if client_count  == 1:
                print("Not_Null")
                window.blit(wait_image, (0, 0))
                pygame.display.flip()  
            elif client_count  == 2:
                print("Full")
                result_variable = calculate_seconds()
                time.sleep(result_variable)
                # break
        except Exception as e:
            print(f"Error receiving client count from server: {e}")
            break

def calculate_seconds():
    current_seconds = int(time.time() % 60)

    if current_seconds >= 1 and current_seconds <= 10:
        result = current_seconds / 10 * 0.5 + 0.5  # Chuyển từ khoảng từ 0 đến 1 thành khoảng từ 0.5 đến 1
    elif current_seconds >= 11 and current_seconds <= 60:
        result = current_seconds / 100 * 0.5 + 0.5  # Chuyển từ khoảng từ 0 đến 1 thành khoảng từ 0.5 đến 1

    return result


def draw_waiting(window):
    window.blit(wait_image, (0, 0))
    pygame.display.flip()  

#===========================Main==== ===========================#
def main_online(window):
    theme_sound.play(-1)
    global player1_lives, player2_lives
    global client_count
    clock = pygame.time.Clock()
    draw_waiting(window)
    connect_to_server("192.168.48.205", 8080)
    try:
        player = player_online.Player(300, 100, 48, 48, player1_lives)
        player2 = player_online_2.Player(600, 100, 48, 48, player2_lives)
        block_size = 48
        random_map_info = random.choice(maps_array)
        background, bg_image, floor = load_map(block_size, random_map_info)

        
        input_visible = False
        
        
        can_shoot1 = True
        can_shoot2 = True
        shot_time1 = datetime.datetime.now()
        shot_time2 = datetime.datetime.now()
        last_shoot_time = pygame.time.get_ticks()

        is_shoot = False
        is_jumping = False

        # Đạn của người chơi
        bullet1 = []
        bullet2 = []
        
        #count client
        receive_thread2l= threading.Thread(target=receive_client_count_from_server,args=())
        receive_thread2l.start()

        
        # receive_thread_x = threading.Thread(target=receive_thread_player, args=())
        # receive_thread_x.start()
        # if client_count == 0:
        #     client_count = 1
        # elif client_count == 1:
        #     client_count = 2
        # send_thread_number_player = threading.Thread(target=send_player_number, args=(client_count,))
        # send_thread_number_player.start()

        run = True
        while run:
            clock.tick(FPS)
            print ("server has: ", client_count)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.USEREVENT:
                    if 'x' in event.dict and 'y' in event.dict and 'sprite' in event.dict :
                        x = event.dict['x']
                        y = event.dict['y']

                        sprite_info = event.dict['sprite']
                        send_thread1 = threading.Thread(target=send_coordinate, args=(x,y))
                        send_thread1.start()

                        send_thread1b = threading.Thread(target=send_sprite_info, args=(sprite_info,))
                        send_thread1b.start() 

                        send_thread1c = threading.Thread(target=send_player_direction, args=(player.direction,))
                        send_thread1c.start() 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and player.jump_count < 1:
                        is_jumping = True
                        player.jump() 
                    elif event.key == pygame.K_SPACE:
                        shot_time1 = pygame.time.get_ticks()
                        if can_shoot1 and not input_visible:
                            is_shoot = True
                            playerShoot(player,bullet1)
                            last_shoot_time = shot_time1
                            can_shoot1 = False
                            for bullet in bullet1:
                                send_thread_bullet = threading.Thread(target=send_coordinate_bullet, args=(bullet.rect.x,bullet.rect.y))
                                send_thread_bullet.start()

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

            receive_thread_x = threading.Thread(target=receive_thread, args=(player2, bullet2))
            receive_thread_x.start()

            # vẽ
            if client_count == 2:
                draw(window, background, bg_image, player, floor, player2, bullet1, bullet2)
            # kiểm tra đạn có tồn tại không
            for bullet in bullet1:
                bullet.rect.x += bullet.x_vel
                bullet.rect.y += bullet.y_vel
                if bullet.rect.right < 0 or bullet.rect.left > WIDTH:
                    bullet1.remove(bullet)
                if bullet.rect.colliderect(player2.rect):
                    if player2_lives > 0:
                        player2_lives -= 1
                        send_thread_hp = threading.Thread(target=send_player_hp, args=(player2_lives,))
                        send_thread_hp.start() 
                        
                    # else:
                    #     player2_lives = 0
                    #     player2.isDead = True
                    #     theme_sound.stop()
                    #     close_connection()
                    #     offline_result.main("You Win")
                    bullet1.remove(bullet)
                    pygame.display.update()
            player2.lives = player2_lives

            for bullet in bullet2:
                bullet.rect.x += bullet.x_vel
                bullet.rect.y += bullet.y_vel
                if bullet.rect.right < 0 or bullet.rect.left > WIDTH:
                    bullet2.remove(bullet)
                if bullet.rect.colliderect(player.rect):
                    bullet2.remove(bullet)
                    pygame.display.update()
            player.lives = player1_lives

            if player.lives == 0:
                player.isDead = True
                theme_sound.stop()
                offline_result.main("You Lose")
                close_connection()
            elif player2.lives == 0:
                player2.isDead = True
                theme_sound.stop()
                offline_result.main("You Win")
                close_connection()
        pygame.quit()
        quit()
    finally:
        close_connection()

if __name__ == "__main__":
    main_online(window)