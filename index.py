import pygame
import random

# Initialize pygame
pygame.init()


# Game Constants
WIDTH, HEIGHT = 800, 500
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PLAYER_SIZE = 25
OBSTACLE_SIZE = 25
BULLET_SIZE = 5
SPEED = 2
BULLET_SPEED = 2
ENEMY_BULLET_SPEED = 10


# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create window
pygame.display.set_caption("Avoid!")  # Window title
background_img = pygame.image.load("bck.jpg")  # Load background image
background_img = pygame.transform.scale(
    background_img, (WIDTH, HEIGHT))  # Scale image

obstacle_img = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
obstacle_img.fill(RED)

# Player setup
player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_SIZE -
                     10, PLAYER_SIZE, PLAYER_SIZE)

# Obstacles and bullets lists
obstacles = []
bullets = []
enemy_bullets = []

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.blit(background_img, (0, 0))

    pygame.time.delay(20)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player.x + PLAYER_SIZE // 2 -
                               BULLET_SIZE // 2, player.y, BULLET_SIZE, BULLET_SIZE))

    # **Define keys before using them**
    keys = pygame.key.get_pressed()
    # Player movement
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= SPEED
    if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
        player.x += SPEED

    # Spawn obstacles
    if random.randint(1, 20) == 1:  # Random chance to spawn an obstacle
        obstacles.append(pygame.Rect(random.randint(
            0, WIDTH - OBSTACLE_SIZE), 0, OBSTACLE_SIZE, OBSTACLE_SIZE))

    # Enemy shooting
    for obstacle in obstacles:
        if random.randint(1, 100) == 1:  # Random chance for obstacle to shoot
            enemy_bullets.append(pygame.Rect(obstacle.x + OBSTACLE_SIZE // 2 -
                                 BULLET_SIZE // 2, obstacle.y + OBSTACLE_SIZE, BULLET_SIZE, BULLET_SIZE))

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.y += SPEED
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)
            score += 1  # Increase score when an obstacle is dodged
        if obstacle.colliderect(player):
            print(f"Game Over! Final Score: {score}")
            running = False

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move enemy bullets
    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet.y += ENEMY_BULLET_SPEED
        if enemy_bullet.y > HEIGHT:
            enemy_bullets.remove(enemy_bullet)
        if enemy_bullet.colliderect(player):
            print(f"Game Over! Final Score: {score}")
            running = False

    # Check for bullet collision with obstacles
    for bullet in bullets[:]:
        for obstacle in obstacles[:]:
            if bullet.colliderect(obstacle):
                bullets.remove(bullet)
                obstacles.remove(obstacle)
                score += 5
                break

    # Draw player, obstacles, and bullets
    pygame.draw.rect(screen, BLUE, player)
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle.x, obstacle.y))

    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, enemy_bullet)

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
