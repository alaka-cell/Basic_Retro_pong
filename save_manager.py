import json
import os
import pygame

popup_active = False

def toggle_popup(player_score, opponent_score):
    global popup_active
    popup_active = not popup_active

def save_score(player_score, opponent_score):
    path = "scores.json"
    data = []

    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append({
        "player_score": player_score,
        "opponent_score": opponent_score
    })

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def show_score_popup(win, width, height, font):
    path = "scores.json"
    if not os.path.exists(path):
        return

    try:
        with open(path, "r") as f:
            scores = json.load(f)
    except json.JSONDecodeError:
        scores = []

    if not scores:
        return

    scores = sorted(scores, key=lambda x: x.get("player_score", 0), reverse=True)[:5]

    popup_width = 400
    popup_height = 300
    popup_rect = pygame.Rect((width - popup_width) // 2, (height - popup_height) // 2, popup_width, popup_height)

    pygame.draw.rect(win, (50, 50, 50), popup_rect)
    pygame.draw.rect(win, (255, 255, 255), popup_rect, 2)

    title_text = font.render("🏆 Highscores", True, (255, 255, 0))
    win.blit(title_text, (popup_rect.centerx - title_text.get_width() // 2, popup_rect.top + 20))

    y = popup_rect.top + 70
    for idx, score in enumerate(scores):
        line = f"{idx + 1}. You: {score['player_score']} | Opponent: {score['opponent_score']}"
        score_text = font.render(line, True, (255, 255, 255))
        win.blit(score_text, (popup_rect.left + 40, y))
        y += 40
