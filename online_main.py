import pygame
import sys
from network import Network

screen = pygame.display.set_mode((550, 550))
pygame.display.set_caption("caro")
board_size = 11

client_number = 0

isClicking = False
game_over = False

img_empty = pygame.image.load('Assets/caro_asset-01.png')
img_empty = pygame.transform.scale(img_empty,(50,50))
img_x = pygame.image.load('Assets/caro_asset-02.png')
img_x = pygame.transform.scale(img_x,(50,50))
img_o = pygame.image.load('Assets/caro_asset-03.png')
img_o = pygame.transform.scale(img_o,(50,50))
rect = img_empty.get_rect()

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([0]*sz)
    return board

def draw_screen(img_empty, img_x, img_o, rect, board):
    for x in range(11):
        rect.center = (50*x+25, -25)
        for y in range(11):
            rect.centery += 50
            if board[x][y] == 0:
                screen.blit(img_empty, rect)
            elif board[x][y] == 1:
                screen.blit(img_x, rect)
            else:
                screen.blit(img_o, rect)
                
def is_win(board):
    for x in range(board_size):
        for y in range (board_size):
            if board[x][y] != 0:
                score = 0
                if x<=6:
                    for t in range(4):
                        if board[x+t+1][y] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if x<=6 and y<=6:
                    for t in range(4):
                        if board[x+t+1][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if y<=6:
                    for t in range(4):
                        if board[x][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if x >=4 and y<=6:
                    for t in range(4):
                        if board[x-(t+1)][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
    return -1

def main():
    global isClicking
    global game_over
    your_turn = True
    you_x = True
    board = make_empty_board(board_size)
    n = Network()
    start = n.getTurn()
    n.send([-1,-1,-1])
    if start == 2:
        your_turn = False
        you_x = False


    while True:
        p2 = n.recieve()
        print(p2)
        if p2 != board:
            board = p2
            your_turn = True

        play_pos = [-1,-1,-1] # chơi ở vị trí nào

        if game_over == False:
            if is_win(board) == 1:
                game_over = True
                print("player 1 win")
            elif is_win(board) == 2:
                game_over = True
                print("player 2 win")

        for event in pygame.event.get():
            if game_over == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isClicking = True
                    mouse_pos = pygame.mouse.get_pos()
                    tile_click_x = int(mouse_pos[0]/50)
                    print(tile_click_x)
                    tile_click_y = int(mouse_pos[1]/50)
                    print(tile_click_y)
                    if board[tile_click_x][tile_click_y] == 0 and your_turn:
                        if you_x:
                            board[tile_click_x][tile_click_y] = 1
                            play_pos = [tile_click_x, tile_click_y,1]
                            your_turn = False
                        else:
                            board[tile_click_x][tile_click_y] = 2
                            play_pos = [tile_click_x, tile_click_y,2]
                            your_turn = False
                if event.type == pygame.MOUSEBUTTONUP:
                    isClicking = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_screen(img_empty, img_x, img_o, rect, board)
        n.send(play_pos)
        pygame.display.update()

main() 