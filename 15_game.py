#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import random
import time

a= int(input('define game rows dimension, integer number='))
b= int(input('define game columns dimension, integer number='))
rows, cols = a, b  # Dimensioni della griglia
if a+b<10:
    n = 160  # blocks dimension
    screen_width, screen_height = cols * n, rows * n
else: #screen to big
    screen_width, screen_height = 800*(a//b), 800*(b//a)
    n=800//max(a,b)

# initial configuration
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gioco del 15")
font = pygame.font.Font(None, 72)

# Colors
WHITE = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
BLACK = (255-WHITE[0],255-WHITE[1],255-WHITE[2])
BACK= (50,50,50)

# Blocks creation
original_blocks = [(x, y) for x in range(0, rows * n, n) for y in range(0, cols * n, n)]

# add white block
white_block = (rows * n - n, cols * n - n)  # Posizione del blocco vuoto
original_blocks.remove(white_block)
original_blocks.append(white_block)

# bloks shuffle
shuffled_blocks = original_blocks[:-1]
random.shuffle(shuffled_blocks)
shuffled_blocks.append(white_block)

def draw_blocks(screen, blocks, n):
    screen.fill(BACK)  # gray background
    for index, (x, y) in enumerate(blocks):
        # draw numbered blocks
        if (x, y) != white_block:
            number = index + 1
            rect = pygame.Rect(y, x, n, n)
            pygame.draw.rect(screen, WHITE, rect) 
            text = font.render(str(number), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            
           #borders
            pygame.draw.rect(screen, BLACK, rect, 2) 
        
        # white block borders
        if (x, y) == white_block:
            rect = pygame.Rect(y, x, n, n)
            pygame.draw.rect(screen, (220,220,220), rect) 
            pygame.draw.rect(screen, BLACK, rect, 2)  
    
    pygame.draw.rect(screen, BLACK, (0, 0, screen_width, screen_height), 5)  # screen borders


# win check
def check_win(shuffled_blocks, original_blocks):
    return shuffled_blocks == original_blocks


def are_adjacent(block1, block2):
    x1, y1 = block1
    x2, y2 = block2
    return (abs(x1 - x2) == n and y1 == y2) or (abs(y1 - y2) == n and x1 == x2)

# time counting
start_time = time.time()

# running conditions
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # arrows movements
            white_index = shuffled_blocks.index(white_block)
            x, y = white_block

            if event.key == pygame.K_DOWN and x - n >= 0:  
                neighbor = (x - n, y)
            elif event.key == pygame.K_UP and x + n < rows * n:  
                neighbor = (x + n, y)
            elif event.key == pygame.K_RIGHT and y - n >= 0: 
                neighbor = (x, y - n)
            elif event.key == pygame.K_LEFT and y + n < cols * n: 
                neighbor = (x, y + n)
            else:
                neighbor = None

            if neighbor and neighbor in shuffled_blocks:
                # blocks exchanging
                neighbor_index = shuffled_blocks.index(neighbor)
                shuffled_blocks[white_index], shuffled_blocks[neighbor_index] = (
                    shuffled_blocks[neighbor_index],
                    shuffled_blocks[white_index],
                )
                white_block = neighbor  # update white block position

    # update screen window
    draw_blocks(screen, shuffled_blocks, n)
    pygame.display.flip()

  # Controlla se il puzzle è completo
    if check_win(shuffled_blocks, original_blocks):
        elapsed_time = time.time() - start_time  # compute time
        screen.fill(BLACK)
        
        victory_text = font.render("Hai vinto! Giocare ancora?", True, WHITE)
        time_text = font.render(f"Tempo: {elapsed_time:.2f} sec", True, WHITE)
        
        # draw victory message and time
        screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 3))
        screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, screen_height // 2))
        
        pygame.display.flip()

        # input Y o N
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # play again blocks shuffle
                        shuffled_blocks = original_blocks[:-1]
                        random.shuffle(shuffled_blocks)
                        shuffled_blocks.append(white_block)
                        start_time = time.time()  # time reset
                        waiting_for_input = False 
                    elif event.key == pygame.K_n:
                        running = False 
                        waiting_for_input = False

    pygame.display.flip()

pygame.quit()

