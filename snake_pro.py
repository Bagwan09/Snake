import pygame
import random
import os

# Initialize Pygame
pygame.init()

# --- COLORS ---
BG_COLOR = (15, 15, 25)
SNAKE_HEAD_COLOR = (0, 255, 180)
SNAKE_BODY_COLOR = (0, 180, 120)
FOOD_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)
BAR_EMPTY = (40, 40, 60)
GOLD = (255, 215, 0)

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Pro: High Score Edition')

clock = pygame.time.Clock()
BLOCK_SIZE = 20
last_score = 0
chosen_speed = 10

# --- HIGH SCORE LOGIC ---
def get_high_score():
    if not os.path.exists("highscore.txt"):
        return 0
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    current_high = get_high_score()
    if score > current_high:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

# --- FONTS ---
font_main = pygame.font.SysFont("arial", 35, bold=True)
font_sub = pygame.font.SysFont("arial", 20, bold=True)

def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        if i == len(snake_body) - 1: # Head
            pygame.draw.rect(screen, SNAKE_HEAD_COLOR, [segment[0], segment[1], BLOCK_SIZE-1, BLOCK_SIZE-1], border_radius=8)
            # Eyes
            pygame.draw.circle(screen, (255, 255, 255), (segment[0] + 6, segment[1] + 6), 3)
            pygame.draw.circle(screen, (255, 255, 255), (segment[0] + 14, segment[1] + 6), 3)
        else: # Body
            pygame.draw.rect(screen, SNAKE_BODY_COLOR, [segment[0] + 2, segment[1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4], border_radius=10)

def show_menu():
    global chosen_speed
    high_score = get_high_score()
    in_menu = True
    while in_menu:
        screen.fill(BG_COLOR)
        
        score_txt = font_sub.render(f"LAST: {last_score}   |   BEST: {high_score}", True, GOLD)
        screen.blit(score_txt, [WIDTH/2 - 110, 30])

        title = font_main.render("SNAKE HIGH SCORE", True, TEXT_COLOR)
        screen.blit(title, [WIDTH/2 - 150, 80])

        # Speed Loading Bar
        bar_x, bar_y, bar_w, bar_h = WIDTH/2 - 100, 150, 200, 30
        fill_pct = 0.33 if chosen_speed == 10 else 0.66 if chosen_speed == 20 else 1.0
        pygame.draw.rect(screen, BAR_EMPTY, [bar_x, bar_y, bar_w, bar_h], border_radius=5)
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, [bar_x, bar_y, bar_w * fill_pct, bar_h], border_radius=5)

        # Speed Labels
        screen.blit(font_sub.render("[1] SLOW", True, TEXT_COLOR), [WIDTH/2 - 150, 200])
        screen.blit(font_sub.render("[2] MED", True, TEXT_COLOR), [WIDTH/2 - 40, 200])
        screen.blit(font_sub.render("[3] FAST", True, TEXT_COLOR), [WIDTH/2 + 70, 200])
        screen.blit(font_sub.render("PRESS SPACE TO START", True, SNAKE_HEAD_COLOR), [WIDTH/2 - 110, 300])

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: chosen_speed = 10
                if event.key == pygame.K_2: chosen_speed = 20
                if event.key == pygame.K_3: chosen_speed = 35
                if event.key == pygame.K_SPACE: in_menu = False

def run_game():
    global last_score
    x, y = WIDTH/2, HEIGHT/2
    dx, dy = 0, 0
    snake_body = []
    snake_len = 1
    
    fx = round(random.randrange(0, WIDTH - BLOCK_SIZE)/20.0)*20.0
    fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE)/20.0)*20.0

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0: dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0: dy, dx = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and dy == 0: dy, dx = BLOCK_SIZE, 0

        x += dx
        y += dy
        
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0: playing = False

        screen.fill(BG_COLOR)
        pygame.draw.circle(screen, FOOD_COLOR, (int(fx + 10), int(fy + 10)), 8)

        head = [x, y]
        snake_body.append(head)
        if len(snake_body) > snake_len: del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == head and (dx != 0 or dy != 0): playing = False

        draw_snake(snake_body)
        pygame.display.update()

        # Fixed the line that caused the SyntaxError
        if x == fx and y == fy:
            fx = round(random.randrange(0, WIDTH - BLOCK_SIZE)/20.0)*20.0
            fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE)/20.0)*20.0
            snake_len += 1
        
        clock.tick(chosen_speed)
    
    last_score = snake_len - 1
    save_high_score(last_score)

# --- START ---
while True:
    show_menu()
    run_game()