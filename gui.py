import sys
import pygame as pg
from pygame import time
from pygame.mixer import pause
from kenken import definition, formDomain, size_n, find_empty, domain, isValid, board, domainReduction
 
pg.init()

# SCREEN_SIZE = 700  # for 9x9
SCREEN_SIZE = 630 # for 4x4
BORDER_OFFSET = 15
squareSize = SCREEN_SIZE - 2*BORDER_OFFSET
cubeSize = (squareSize)/size_n
screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
# for 4x4
font = pg.font.SysFont(None, 80)
font1 = pg.font.SysFont(None, 50)
# for 9x9
# font = pg.font.SysFont(None, 50)
# font1 = pg.font.SysFont(None, 20)
 
def values():
    for coor in definition:
        for a in range(0, len(coor)-1):
            rowNo = coor[a][0]
            colNo = coor[a][1]
            if (rowNo+1, colNo) in coor:
                # draw black line down
                pg.draw.line(screen, pg.Color(194, 198, 204, 1), pg.Vector2(
                    (colNo*cubeSize + BORDER_OFFSET), (rowNo+1)*cubeSize + BORDER_OFFSET), pg.Vector2(((colNo+1)*cubeSize + BORDER_OFFSET), (rowNo+1)*cubeSize + BORDER_OFFSET), 5)
 
            if (rowNo-1, colNo) in coor:
                # draw line up
                pg.draw.line(screen, pg.Color(194, 198, 204, 1), pg.Vector2(
                    (colNo*cubeSize + BORDER_OFFSET), (rowNo)*cubeSize + BORDER_OFFSET), pg.Vector2(((colNo+1)*cubeSize + BORDER_OFFSET), (rowNo)*cubeSize + BORDER_OFFSET), 5)
                # y = y + cubeSize
 
            if (rowNo, colNo+1) in coor:
                # draw black line right
                pg.draw.line(screen, pg.Color(194, 198, 204, 1), pg.Vector2(
                    ((colNo+1)*cubeSize + BORDER_OFFSET), (rowNo*cubeSize + BORDER_OFFSET)), pg.Vector2(((colNo+1)*cubeSize + BORDER_OFFSET), (rowNo+1)*cubeSize + BORDER_OFFSET), 5)
 
            if (rowNo, colNo-1) in coor:
                # draw black line left
                pg.draw.line(screen, pg.Color(194, 198, 204, 1), pg.Vector2(
                    (colNo*cubeSize + BORDER_OFFSET), (rowNo*cubeSize + BORDER_OFFSET)), pg.Vector2((colNo * cubeSize + BORDER_OFFSET), (rowNo+1)*cubeSize + BORDER_OFFSET), 5)
 

def draw_background():
    screen.fill(pg.Color("white"))
   
    i = 1
    while (i * cubeSize) < squareSize:  # lines horizontally and vertically of width cubeSize
        j = 0
        count = 0
        while count < size_n:
            # Vertical
            pg.draw.line(screen, pg.Color("black"), pg.Vector2(
                (i * cubeSize) + BORDER_OFFSET, BORDER_OFFSET), pg.Vector2((i * cubeSize) + BORDER_OFFSET, (j + cubeSize) + BORDER_OFFSET), 5)
            j = j + cubeSize
            count += 1  # (x,y) coordonates for column
        count = 0
        j = 0
        while count < size_n:
            # Horizontal
            pg.draw.line(screen, pg.Color("black"), pg.Vector2(
                BORDER_OFFSET, (i * cubeSize) + BORDER_OFFSET), pg.Vector2((j + cubeSize) + BORDER_OFFSET, (i * cubeSize) + BORDER_OFFSET), 5)
            j = j + cubeSize
            count = count + 1
        i += 1
    values()
    # offset both x and y, screen size 
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(BORDER_OFFSET, BORDER_OFFSET, squareSize, squareSize), 10)
 
 
 
def draw_numbers():
    row = 0
    # off = 25 # for 9x9
    off = 60 # for 4x4
 
    while row < size_n:
        col = 0
        while col < size_n:
            output = board[row][col]
            n_text = font.render(str(output), True, pg.Color('black'), "white")
            screen.blit(n_text, pg.Vector2(
                (col * cubeSize) + (off + 15), (row * cubeSize) + (off + 15)))
            col += 1
        row += 1
 
    a = 0
    b = 0
    offs = 10
 
    for line in definition:
        # want only the first coordinate
        a = line[0][0]
        b = line[0][1]
        outputText = str(line[len(line)-1][0]) + str(line[len(line)-1][1])
        n_text = font1.render(outputText, True, pg.Color('black'))
        screen.blit(n_text, pg.Vector2(
            (b * cubeSize) + (25), (a * cubeSize) + (offs + 20)))
 
 

def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
 
    draw_background()
    draw_numbers()
    pg.display.flip()    
 
 
 
 
def changeText(textBox, colour, row, col):
    # offs = 25 # for 9x9
    offs = 60 # for 4x4
    c_text = font.render(textBox, True, pg.Color(colour), "white")
    screen.blit(c_text, pg.Vector2((col * cubeSize) + (offs + 15), (row * cubeSize) + (offs + 15)))
    pg.display.flip()
 

 
def solve(puzzle):
    find = find_empty(puzzle)
    if not find:
        return True
    else:
        row, col = find
    i = row*size_n + col
    for val in domain[i]:
        if isValid(puzzle, val, (row, col)):
            changeText(str(puzzle[row][col]), "white", row, col)
            pg.time.wait(100)
            puzzle[row][col] = val
            changeText(str(val), "black" , row, col)
            pg.time.wait(100)
            if solve(puzzle):
                return True
            changeText(str(puzzle[row][col]), "white", row, col)
            pg.time.wait(100)
            puzzle[row][col] = 0
            changeText(str(puzzle[row][col]), "black", row, col)
            pg.time.wait(100)
    return False



if __name__ == "__main__":
    formDomain()
    domainReduction()
    game_loop()
    solve(board)
    pg.time.wait(1000)
    while 1:
        game_loop()
