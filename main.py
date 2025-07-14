import pygame
import sys
import random
from gamestate import GameStateManager
from menu import render_menu, update_selected_difficulty, get_selected_difficulty
from game_over import render_game_over, render_victory_screen
from particle import Particle
from save_manager import show_score_popup, toggle_popup, popup_active, save_score

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_path = r"C:\\Users\\user\\filename\\arcade_classic\\Arcade Classic.ttf"
title_font = pygame.font.Font(font_path, 60)
subtitle_font = pygame.font.Font(font_path, 28)
score_font = pygame.font.Font(font_path, 30)

brain_icon = pygame.image.load(
   r"C:\\path\\to\\the\image\"
).convert_alpha()
brain_icon = pygame.transform.scale(brain_icon, (40, 40))
brain_rect = brain_icon.get_rect(topright=(WIDTH - 20, 20))

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 8
PADDLE_SPEED = 6
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

player = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

player_score = 0
opponent_score = 0
ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y

game_state = GameStateManager()
clock = pygame.time.Clock()
game_over_frame = 0

ao_difficulty = None
ai_speed_multiplier = 0.8

explode_timer = 0
fade_alpha = 0
particles = []
score_saved = False
winner = None

def reset_game():
    global player_score, opponent_score, ball_dx, ball_dy, player, opponent, score_saved, winner, game_over_frame
    player_score = 0
    opponent_score = 0
    score_saved = False
    winner = None
    game_over_frame = 0
    player = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    opponent = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED_X
    ball_dy = BALL_SPEED_Y

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if brain_rect.collidepoint(event.pos):
                toggle_popup(player_score, opponent_score)

        if game_state.is_menu():
            button_data = render_menu(WIN, WIDTH, HEIGHT, title_font, subtitle_font, score_font)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level, rect in button_data["difficulties"].items():
                    if rect.collidepoint(event.pos):
                        update_selected_difficulty(level)
                        ai_difficulty = level
                        ai_speed_multiplier = {"Easy": 0.5, "Medium": 0.8, "Hard": 1.1}[level]

                if button_data["start"].collidepoint(event.pos) and get_selected_difficulty():
                    game_state.start_game()
                elif button_data["highscore"].collidepoint(event.pos):
                    toggle_popup(player_score, opponent_score)

        elif game_state.is_playing() and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state.go_to_menu()
                reset_game()
            elif event.key == pygame.K_r:
                reset_game()

        elif game_state.is_game_over() and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()
                game_state.go_to_menu()

    if game_state.is_menu():
        render_menu(WIN, WIDTH, HEIGHT, title_font, subtitle_font, score_font)

    elif game_state.is_playing():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.top > 0:
            player.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += PADDLE_SPEED

        if opponent.centery < ball.centery and opponent.bottom < HEIGHT:
            opponent.y += PADDLE_SPEED * ai_speed_multiplier
        if opponent.centery > ball.centery and opponent.top > 0:
            opponent.y -= PADDLE_SPEED * ai_speed_multiplier

        ball.x += ball_dx
        ball.y += ball_dy

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_dx *= -1

        if ball.left <= 0:
            opponent_score += 1
            if opponent_score >= 2:
                winner = "opponent"
                game_state.explode()
                particles = [Particle(ball.centerx, ball.centery) for _ in range(100)]
                fade_alpha = 0
                explode_timer = 0
            else:
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_dx = BALL_SPEED_X
                ball_dy = BALL_SPEED_Y

        if ball.right >= WIDTH:
            player_score += 1
            if player_score >= 2:
                winner = "player"
                game_state.explode()
                particles = [Particle(ball.centerx, ball.centery) for _ in range(100)]
                fade_alpha = 0
                explode_timer = 0
            else:
                ball.center = (WIDTH // 2, HEIGHT // 2)
                ball_dx = -BALL_SPEED_X
                ball_dy = BALL_SPEED_Y

        WIN.fill(BLACK)
        pygame.draw.rect(WIN, WHITE, player)
        pygame.draw.rect(WIN, WHITE, opponent)
        pygame.draw.ellipse(WIN, WHITE, ball)
        pygame.draw.aaline(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = score_font.render(f"{player_score} : {opponent_score}", True, WHITE)
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        #WIN.blit(brain_icon, brain_rect)
        #if popup_active:
            #show_score_popup(WIN, WIDTH, HEIGHT, subtitle_font)

        pygame.display.flip()

    elif game_state.is_exploding():
        WIN.fill(BLACK)
        for p in particles[:]:
            p.update()
            p.draw(WIN)
            if p.life <= 0:
                particles.remove(p)

        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill(BLACK)
        WIN.blit(fade_surface, (0, 0))
        if fade_alpha < 255:
            fade_alpha += 8

        #WIN.blit(brain_icon, brain_rect)
        #if popup_active:
            #show_score_popup(WIN, WIDTH, HEIGHT, subtitle_font)

        pygame.display.flip()
        explode_timer += 1
        if explode_timer > 60 and len(particles) == 0:
            game_state.finish_explode()
            game_state.go_to_game_over()

    elif game_state.is_game_over():
        WIN.fill(BLACK)
        if winner == "player":
            render_victory_screen(WIN, WIDTH, HEIGHT, title_font, subtitle_font, game_over_frame)
        else:
            render_game_over(WIN, WIDTH, HEIGHT, title_font, subtitle_font, game_over_frame)

        if not score_saved:
            save_score(player_score, opponent_score)
            score_saved = True

        #WIN.blit(brain_icon, brain_rect)
        #if popup_active:
            #show_score_popup(WIN, WIDTH, HEIGHT, subtitle_font)

        pygame.display.flip()
        if game_over_frame < 100:
            game_over_frame += 1

    clock.tick(60)
