#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import random
import time

# Input game dimension
rows = int(input("Define game rows dimension (integer number): "))
cols = int(input("Define game columns dimension (integer number): "))

# blocks dimension and screen dimension
if rows + cols < 10:
    n = 160  # Dimensione dei blocchi
    screen_width, screen_height = cols * n, rows * n
else:  # Schermo troppo grande
    n = 800 // max(rows, cols)
    screen_width, screen_height = cols * n, rows * n

# Pygame configuration
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gioco del 15")
font = pygame.font.Font(None, 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# counting permutations
def count_inversions(blocks):
    flat_list = [block for block in blocks if block != 0]  # Escludiamo il blocco vuoto (0)
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions

# solvibility check
def is_solvable(blocks, rows, cols):
    inversions = count_inversions(blocks)
    blank_row = blocks.index(0) // cols  
    
    if cols % 2 == 1:  
        return inversions % 2 == 0
    else:  # Se il numero di colonne è pari
        return (inversions + blank_row) % 2 == 0


def generate_solvable_puzzle(rows, cols):
    blocks = list(range(1, rows * cols)) + [0]  
    while True:
        random.shuffle(blocks)
        if is_solvable(blocks, rows, cols):
            return blocks

# block drawing
def draw_blocks(screen, blocks, rows, cols, n):
    screen.fill(GRAY)
    for i, value in enumerate(blocks):
        x = (i % cols) * n
        y = (i // cols) * n
        rect = pygame.Rect(x, y, n, n)
        if value != 0:  
            pygame.draw.rect(screen, WHITE, rect)
            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  

# win check
def check_win(blocks):
    return blocks == list(range(1, rows * cols)) + [0]

# moving blocks
def move_block(blocks, direction, rows, cols):
    blank_index = blocks.index(0)
    if direction == "up" and blank_index // cols > 0: 
        target_index = blank_index - cols
    elif direction == "down" and blank_index // cols < rows - 1:  
        target_index = blank_index + cols
    elif direction == "left" and blank_index % cols > 0:  
        target_index = blank_index - 1
    elif direction == "right" and blank_index % cols < cols - 1:  
        target_index = blank_index + 1
    else:
        return blocks  

    #blocks exchange
    blocks[blank_index], blocks[target_index] = blocks[target_index], blocks[blank_index]
    return blocks

# puzzle generating
blocks = generate_solvable_puzzle(rows, cols)

# start time
start_time = time.time()

# game cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                blocks = move_block(blocks, "up", rows, cols)
            elif event.key == pygame.K_UP:
                blocks = move_block(blocks, "down", rows, cols)
            elif event.key == pygame.K_RIGHT:
                blocks = move_block(blocks, "left", rows, cols)
            elif event.key == pygame.K_LEFT:
                blocks = move_block(blocks, "right", rows, cols)

    # draws blocks
    draw_blocks(screen, blocks, rows, cols, n)
    pygame.display.flip()

    # check puzzle and restart it
    if check_win(blocks):
        elapsed_time = time.time() - start_time
        screen.fill(BLACK)
        victory_text = font.render("You Win!", True, WHITE)
        time_text_1 = font.render(f"Block complexity: {rows}X{cols}", True, WHITE)
        time_text_2 = font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
        time_text_3 = font.render('Play again? Y/N', True, WHITE)
        line_spacing = 50
        screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 5))
        screen.blit(time_text_1, (screen_width // 2 - time_text_1.get_width() // 2, screen_height // 5 + line_spacing))
        screen.blit(time_text_2, (screen_width // 2 - time_text_2.get_width() // 2, screen_height // 5 + line_spacing * 2))
        screen.blit(time_text_3, (screen_width // 2 - time_text_3.get_width() // 2, screen_height // 5 + line_spacing * 3))
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
                        blocks = generate_solvable_puzzle(rows, cols)
                        pygame.display.flip()
                        start_time = time.time()  # time reset
                        waiting_for_input = False 
                    elif event.key == pygame.K_n:
                        running = False 
                        waiting_for_input = False


pygame.quit()


# In[15]:


import pygame
import random
import time

# Input game dimension
rows = int(input("Define game rows dimension (integer number): "))
cols = int(input("Define game columns dimension (integer number): "))

# blocks dimension and screen dimension
if rows + cols < 10:
    n = 160  # Dimensione dei blocchi
    screen_width, screen_height = cols * n, rows * n
else:  # Schermo troppo grande
    n = 800 // max(rows, cols)
    screen_width, screen_height = cols * n, rows * n

# Pygame configuration
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gioco del 15")
font = pygame.font.Font(None, 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Count inversions in the puzzle
def count_inversions(blocks):
    flat_list = [block for block in blocks if block != 0]  # Exclude the empty block (0)
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions

# Solvability check considering all possible cases
def is_solvable(blocks, rows, cols):
    inversions = count_inversions(blocks)
    blank_row = blocks.index(0) // cols  # Row of the empty block
    
    if rows % 2 == 1 and cols % 2 == 1:
        # Both rows and columns are odd, solvability depends on inversions
        return inversions % 2 == 0
    elif rows % 2 == 0 and cols % 2 == 0:
        # Both rows and columns are even, solvability depends on inversions + row of the empty block
        return (inversions + blank_row+1) % 2 == 0
    else:
        # One dimension is odd, the other is even (either rows even, cols odd or rows odd, cols even)
        # Solvability depends on inversions only
        return inversions % 2 == 0


# Puzzle generator
def generate_solvable_puzzle(rows, cols):
    blocks = list(range(1, rows * cols)) + [0]
    while True:
        random.shuffle(blocks)
        if is_solvable(blocks, rows, cols):
            return blocks

# Block drawing
def draw_blocks(screen, blocks, rows, cols, n):
    screen.fill(GRAY)
    for i, value in enumerate(blocks):
        x = (i % cols) * n
        y = (i // cols) * n
        rect = pygame.Rect(x, y, n, n)
        if value != 0:
            pygame.draw.rect(screen, WHITE, rect)
            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

# Win check
def check_win(blocks):
    return blocks == list(range(1, rows * cols)) + [0]

# Moving blocks
def move_block(blocks, direction, rows, cols):
    blank_index = blocks.index(0)
    if direction == "up" and blank_index // cols > 0:
        target_index = blank_index - cols
    elif direction == "down" and blank_index // cols < rows - 1:
        target_index = blank_index + cols
    elif direction == "left" and blank_index % cols > 0:
        target_index = blank_index - 1
    elif direction == "right" and blank_index % cols < cols - 1:
        target_index = blank_index + 1
    else:
        return blocks  # Nessun movimento se non possibile

    blocks[blank_index], blocks[target_index] = blocks[target_index], blocks[blank_index]
    return blocks

# Puzzle generating
blocks = generate_solvable_puzzle(rows, cols)

# Start time
start_time = time.time()

# game cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                blocks = move_block(blocks, "up", rows, cols)
            elif event.key == pygame.K_UP:
                blocks = move_block(blocks, "down", rows, cols)
            elif event.key == pygame.K_RIGHT:
                blocks = move_block(blocks, "left", rows, cols)
            elif event.key == pygame.K_LEFT:
                blocks = move_block(blocks, "right", rows, cols)
    # Draw blocks
    draw_blocks(screen, blocks, rows, cols, n)
    pygame.display.flip()

    # Check win condition
    if check_win(blocks):
        elapsed_time = time.time() - start_time
        screen.fill(BLACK)
        victory_text = font.render("You Win!", True, WHITE)
        time_text_1 = font.render(f"Block complexity: {rows}X{cols}", True, WHITE)
        time_text_2 = font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
        time_text_3 = font.render('Play again? Y/N', True, WHITE)
        line_spacing = 50
        screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 5))
        screen.blit(time_text_1, (screen_width // 2 - time_text_1.get_width() // 2, screen_height // 5 + line_spacing))
        screen.blit(time_text_2, (screen_width // 2 - time_text_2.get_width() // 2, screen_height // 5 + line_spacing * 2))
        screen.blit(time_text_3, (screen_width // 2 - time_text_3.get_width() // 2, screen_height // 5 + line_spacing * 3))
        pygame.display.flip()
        # Input Y or N
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        blocks = generate_solvable_puzzle(rows, cols)
                        pygame.display.flip()
                        start_time = time.time()  # reset time
                        waiting_for_input = False
                    elif event.key == pygame.K_n:
                        running = False
                        waiting_for_input = False

pygame.quit()

