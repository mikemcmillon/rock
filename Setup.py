import os
import pygame
import time

# Set my basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Initialize pygame
HEIGHT = 600
WIDTH = 660
FPS = 10  # Frames per second
pygame.init()  # Turns on pygame
pygame.font.init() # Allows us to set a font type for words on the screen
pygame.mixer.init()  # Turns on sound in pygame
font_name = pygame.font.match_font('Times New Roman')
font = pygame.font.Font(font_name, 50)
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'   # Sets where your game window appears on the screen
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Setup images
pygame.display.set_caption('Rock - Paper - Scissors')
icon = pygame.image.load(os.path.join('images', 'letter-m.png'))
pygame.display.set_icon(icon)
rock = pygame.image.load(os.path.join('images', 'rock.png')).convert_alpha()
paper = pygame.image.load(os.path.join('images', 'paper.png')).convert_alpha()
scissors = pygame.image.load(os.path.join('images', 'scissors.png')).convert_alpha()
rectangles = [pygame.rect.Rect(30, 90, 138, 138), pygame.rect.Rect(30, 250, 128, 138),
              pygame.rect.Rect(30, 420, 128, 138), pygame.rect.Rect(490, 90, 138, 138),
              pygame.rect.Rect(490, 250, 138, 138), pygame.rect.Rect(490, 420, 138, 138)]
