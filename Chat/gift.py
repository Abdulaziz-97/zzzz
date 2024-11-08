import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1920
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Virtual Pet")

# Load and scale background image
try:
    background = pygame.image.load('9205427.png')
    background = pygame.transform.scale(background, (screen_width, screen_height))
except pygame.error as e:
    print(f"Unable to load background image: {e}")
    sys.exit()

# Load sprite sheets
try:
    idle_sprite_sheet = pygame.image.load('Idle (40x48).png')
    sitting_sprite_sheet = pygame.image.load('Ground (40x48).png')
    falling_sprite_sheet = pygame.image.load('Fall (40x48).png')
except pygame.error as e:
    print(f"Unable to load sprite sheet image: {e}")
    sys.exit()

# Define sprite dimensions (assuming each frame is 32x32 pixels)
SPRITE_WIDTH = 40
SPRITE_HEIGHT = 48
SPRITE_COLUMNS = 4  # Number of columns in each sprite sheet
SPRITE_ROWS = 1     # Number of rows in each sprite sheet

# Scale factor
SCALE_FACTOR = 5

# Extract frames from sprite sheets and scale them
def load_frames(sprite_sheet):
    frames = []
    for col in range(SPRITE_COLUMNS):
        frame = sprite_sheet.subsurface(pygame.Rect(
            col * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
        scaled_frame = pygame.transform.scale(frame, (SPRITE_WIDTH * SCALE_FACTOR, SPRITE_HEIGHT * SCALE_FACTOR))
        frames.append(scaled_frame)
    return frames

idle_frames = load_frames(idle_sprite_sheet)
sitting_frames = load_frames(sitting_sprite_sheet)
falling_frames = load_frames(falling_sprite_sheet)

# Animation variables
current_frame = 0
frame_delay = 1000  # Milliseconds between frames (slower animation)
last_update = pygame.time.get_ticks()

# Define pet states
IDLE = 'idle'
SITTING = 'sitting'
FALLING = 'falling'
current_state = IDLE

# Define pet attributes
hunger = 100

def feed_pet():
    global hunger
    hunger = min(hunger + 10, 100)

# Add a button to feed the pet
feed_button = pygame.Rect(50, 1100, 100, 50)

# Pet position variables (bottom of the screen)
pet_x = screen_width // 2 - (SPRITE_WIDTH * SCALE_FACTOR) // 2
pet_y = screen_height - (SPRITE_HEIGHT * SCALE_FACTOR) - 100

# Hunger decrease variables
hunger_decrease_delay = 5000  # Milliseconds between hunger decreases
last_hunger_update = pygame.time.get_ticks()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if feed_button.collidepoint(event.pos):
                feed_pet()

    # Update animation frame
    now = pygame.time.get_ticks()
    if now - last_update > frame_delay:
        current_frame = (current_frame + 1) % SPRITE_COLUMNS
        last_update = now

    # Decrease hunger over time
    if now - last_hunger_update > hunger_decrease_delay:
        hunger = max(hunger - 5, 0)
        last_hunger_update = now

    # Perform random actions
    if current_state != FALLING:
        action_delay = 3000  # Milliseconds between actions
        last_action = pygame.time.get_ticks()
        if now - last_action > action_delay:
            action = random.choice(['sit', 'fall', 'none'])
            if action == 'sit':
                current_state = SITTING
            elif action == 'fall':
                current_state = FALLING

    # Apply gravity if falling
    if current_state == FALLING:
        pet_y += pet_speed_y
        pet_speed_y += 1  # Fall down faster over time

        if pet_y >= screen_height - (SPRITE_HEIGHT * SCALE_FACTOR) - 100:
            pet_y = screen_height - (SPRITE_HEIGHT * SCALE_FACTOR) - 100
            pet_speed_y = 0
            current_state = IDLE

    # Clear the screen and draw the background
    screen.blit(background, (0, 0))

    # Draw the current frame of the pet based on its state
    if current_state == IDLE:
        screen.blit(idle_frames[current_frame], (pet_x, pet_y))
    elif current_state == SITTING:
        screen.blit(sitting_frames[current_frame], (pet_x, pet_y))
    elif current_state == FALLING:
        screen.blit(falling_frames[current_frame], (pet_x, pet_y))

    # Draw the feed button and hunger bar background
    pygame.draw.rect(screen, (0, 255, 0), feed_button)
    font = pygame.font.Font(None, 36)
    text = font.render('Feed', True, (0, 0, 0))
    screen.blit(text, (60, 1110))

    # Draw the hunger bar background and fill based on hunger level
    hunger_bar_background = pygame.Rect(200, 1100, 300, 50)
    hunger_bar_fill = pygame.Rect(200, 1100, hunger * 3, 50) # Scale hunger to fit within the bar width

    pygame.draw.rect(screen, (255, 0, 0), hunger_bar_background) # Red background for empty bar
    pygame.draw.rect(screen, (0, 255, 0), hunger_bar_fill)       # Green fill for current hunger level

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
