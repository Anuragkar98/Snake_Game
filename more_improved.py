import pygame
import time
import random

pygame.init()

width = 800
height = 600
scoreboard_height = 100
lower_section_height = 50
game_area_height = height - (scoreboard_height + lower_section_height)

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Snake Game")

bg_image = pygame.image.load("background.jpg")
bg_image = pygame.transform.scale(bg_image, (width, height))

snakegame_image = pygame.image.load("snakegame_image.webp")
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (30, 30))


dark_green = (0, 100, 0)
white = (255, 255, 255)
light_yellow = (255, 255, 153)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
light_green = (144, 238, 144)

title_font = pygame.font.SysFont("arialblack", 35)
font = pygame.font.SysFont("arialblack", 30)
button_font = pygame.font.SysFont("arialblack", 20)

fullscreen = False
snake_size = 20
snake_speed = 10
clock = pygame.time.Clock()

high_score = 0

def opening_screen():
    screen.fill(light_green)
    scaled_image = pygame.transform.scale(snakegame_image, (300, 200))
    screen.blit(scaled_image, (width // 2 - 150, height // 4 - 50))
    
    pygame.draw.rect(screen, dark_green, (width // 2 - 100, height // 2 + 50, 200, 60), border_radius=20)
    text = button_font.render("Start Game", True, light_green)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 + 70))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width // 2 - 100 <= mouse_x <= width // 2 + 100 and height // 2 + 50 <= mouse_y <= height // 2 + 110:
                    waiting = False

def show_score(score):
    global high_score
    if score > high_score:
        high_score = score
    pygame.draw.rect(screen, dark_green, (0, 0, width, scoreboard_height))
    pygame.draw.rect(screen, dark_green, (0, height - lower_section_height, width, lower_section_height))
    
    game_title = title_font.render("SNAKE GAME", True, light_yellow)
    score_text = font.render(f"Score: {score}", True, light_yellow)
    high_score_text = font.render(f"High Score: {high_score}", True, light_yellow)
    
    screen.blit(game_title, (width // 2 - game_title.get_width() // 2, 10))
    screen.blit(score_text, (width - score_text.get_width() - 20, 10))
    screen.blit(high_score_text, (20, 10))

def game_loop():
    global fullscreen, screen, width, height, high_score
    game_over = False
    game_close = False
    
    x, y = width // 2, game_area_height // 2 + scoreboard_height
    x_change, y_change = 0, 0
    snake_body = [[x, y]]
    snake_length = 1
    
    def generate_food():
        while True:
            food_x = random.randint(0, (width - snake_size) // 20) * 20
            food_y = random.randint(scoreboard_height // 20, (game_area_height - snake_size) // 20) * 20 + scoreboard_height
            if [food_x, food_y] not in snake_body:
                return food_x, food_y
    
    food_x, food_y = generate_food()
    
    while not game_over:
        while game_close:
            screen.fill(black)
            message1 = font.render("Game Over!", True, red)
            message2 = font.render("Press Q to Quit", True, red)
            message3 = font.render("Press C to Continue", True, red)
            
            screen.blit(message1, (width / 3, height / 4))
            screen.blit(message2, (width / 3, height / 3))
            screen.blit(message3, (width / 3, height / 2 + 30))
            
            show_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                elif event.type == pygame.QUIT:
                    game_over = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_size
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_size
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_size
                    x_change = 0
        
        if x >= width or x < 0 or y >= height - lower_section_height or y < scoreboard_height:
            game_close = True
        
        x += x_change
        y += y_change
        
        screen.blit(bg_image, (0, 0))
        screen.blit(apple_image, (food_x, food_y))
        
        if abs(x - food_x) < snake_size and abs(y - food_y) < snake_size:
            snake_length += 1
            food_x, food_y = generate_food()
        
        snake_head = [x, y]
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]
        
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True
        
        for segment in snake_body:
            pygame.draw.rect(screen, blue, [segment[0], segment[1], snake_size, snake_size])
        
        show_score(snake_length - 1)
        pygame.display.update()
        
        clock.tick(snake_speed)
    
    pygame.quit()
    quit()

opening_screen()
game_loop()
