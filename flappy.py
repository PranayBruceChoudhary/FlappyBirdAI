import pygame
import random
import sys
import torch

# --- GAME SETUP ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimal Flappy Bird for AI")
clock = pygame.time.Clock()

# --- COLORS ---
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)   # Bird
GREEN = (0, 200, 0)    # Pipes
RED = (255, 0, 0)      # Game Over flash

# --- BIRD SETTINGS ---
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 1.2
jump_strength = -12.0  # Negative because y=0 is the TOP of the screen
bird_size = 20

# --- PIPE SETTINGS ---
pipe_x = WIDTH
pipe_width = 60
pipe_gap = 150         # Vertical space the bird has to pass through
pipe_velocity = -5.0   # Moves left
pipe_gap_y = random.randint(150, HEIGHT - 150) # The exact center of the gap

# --- GAME LOOP ---
running = True
while running:
    jumped_this_frame = 0 # 0 = fell, 1 = jumped (For our AI later!)
    
    # 1. HANDLE USER INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
                jumped_this_frame = 1

    # 2. PHYSICS UPDATE
    # Apply gravity to bird
    bird_velocity += gravity
    bird_y += bird_velocity
    
    # Move pipe left
    pipe_x += pipe_velocity
    
    # If pipe goes off screen, spawn a new one!
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_gap_y = random.randint(150, HEIGHT - 150)

    # 3. CALCULATE AI VARIABLES (dx, dy)
    # dx = horizontal distance from bird to pipe
    dx = pipe_x - bird_x 
    # dy = vertical distance from bird to the center of the gap
    dy = bird_y - pipe_gap_y 
    
    # Print them so you can see the math happening live!
    print(f"dx: {dx:.1f} | dy: {dy:.1f} | Action: {jumped_this_frame}")

    # 4. COLLISION DETECTION (Game Over logic)
    hit_floor = bird_y > HEIGHT or bird_y < 0
    hit_pipe_x = bird_x + bird_size > pipe_x and bird_x < pipe_x + pipe_width
    hit_pipe_y = bird_y < pipe_gap_y - (pipe_gap // 2) or bird_y + bird_size > pipe_gap_y + (pipe_gap // 2)
    
    if hit_floor or (hit_pipe_x and hit_pipe_y):
        # Reset the game
        screen.fill(RED)
        pygame.display.flip()
        pygame.time.delay(300) # Pause for a moment
        bird_y = HEIGHT // 2
        bird_velocity = 0
        pipe_x = WIDTH
        pipe_gap_y = random.randint(150, HEIGHT - 150)
        continue

    # 5. DRAW EVERYTHING
    screen.fill(WHITE) # Background
    
    # Draw Bird
    pygame.draw.rect(screen, BLUE, (bird_x, bird_y, bird_size, bird_size))
    
    # Draw Pipes (Top pipe and Bottom pipe)
    top_pipe_height = pipe_gap_y - (pipe_gap // 2)
    bottom_pipe_y = pipe_gap_y + (pipe_gap // 2)
    bottom_pipe_height = HEIGHT - bottom_pipe_y
    
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, pipe_width, top_pipe_height)) # Top
    pygame.draw.rect(screen, GREEN, (pipe_x, bottom_pipe_y, pipe_width, bottom_pipe_height)) # Bottom

    # Update screen
    pygame.display.flip()
    
    # Run at 30 Frames Per Second
    clock.tick(30)