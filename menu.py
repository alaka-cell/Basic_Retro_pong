import pygame

selected_difficulty = None

def update_selected_difficulty(level):
    global selected_difficulty
    selected_difficulty = level

def get_selected_difficulty():
    return selected_difficulty

def render_menu(win, width, height, title_font, subtitle_font, score_font):
    win.fill((0, 0, 0))

    brain_icon = pygame.image.load(
        r"C:\\path\\to\\the\image\"
    ).convert_alpha()
    brain_icon = pygame.transform.scale(brain_icon, (120, 120))

    spacing = 30
    brain_h = brain_icon.get_height()
    title_h = title_font.size("Retro Pong")[1]
    button_h = subtitle_font.size("START")[1] + 10
    difficulty_h = subtitle_font.size("Easy")[1] + 20

    total_height = brain_h + spacing + title_h + spacing + button_h + spacing + button_h + spacing + difficulty_h
    start_y = (height - total_height) // 2

    brain_rect = brain_icon.get_rect(center=(width // 2, start_y + brain_h // 2))
    win.blit(brain_icon, brain_rect)

    title_text = title_font.render("Retro Pong", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(width // 2, brain_rect.bottom + spacing + title_h // 2))
    win.blit(title_text, title_rect)

    start_text = subtitle_font.render("START", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(width // 2, title_rect.bottom + spacing + button_h // 2))
    pygame.draw.rect(win, (255, 255, 255), start_rect.inflate(20, 10), 2)
    win.blit(start_text, start_rect)

    hs_text = subtitle_font.render("HIGHSCORE", True, (255, 255, 255))
    hs_rect = hs_text.get_rect(center=(width // 2, start_rect.bottom + spacing + button_h // 2))
    pygame.draw.rect(win, (255, 255, 255), hs_rect.inflate(30, 10), 2)
    win.blit(hs_text, hs_rect)

    difficulties = ["Easy", "Medium", "Hard"]
    selected = get_selected_difficulty()
    difficulty_rects = {}

    button_padding = 20
    button_spacing = 20
    button_boxes = []

    for diff in difficulties:
        text_surface = subtitle_font.render(diff, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        box = pygame.Rect(0, 0, text_rect.width + button_padding * 2, text_rect.height + 10)
        button_boxes.append((diff, text_surface, text_rect, box))

    total_width = sum(box[3].width for box in button_boxes) + button_spacing * (len(button_boxes) - 1)
    start_x = (width - total_width) // 2
    y = hs_rect.bottom + spacing

    for diff, text_surface, text_rect, box in button_boxes:
        box.topleft = (start_x, y)
        text_rect.center = box.center

        if selected == diff:
            pygame.draw.rect(win, (255, 255, 255), box)  
            text_surface = subtitle_font.render(diff, True, (0, 0, 0)) 
        else:
            pygame.draw.rect(win, (255, 255, 255), box, 2)

        win.blit(text_surface, text_rect)
        difficulty_rects[diff] = box
        start_x += box.width + button_spacing

    pygame.display.update()

    return {
        "start": start_rect.inflate(20, 10),
        "highscore": hs_rect.inflate(30, 10),
        "difficulties": difficulty_rects
    }
