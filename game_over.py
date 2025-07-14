import pygame

def render_game_over(win, width, height, title_font, subtitle_font, frame_count):
    win.fill((0, 0, 0))
    sad_surface = title_font.render(":(", True, (255, 0, 0))
    over_surface = title_font.render("GAME OVER", True, (255, 255, 255))
    retry_surface = subtitle_font.render("You can always try again", True, (100, 255, 100))

    center_x = width // 2
    sad_x = center_x - sad_surface.get_width() // 2
    over_x = center_x - over_surface.get_width() // 2
    retry_x = center_x - retry_surface.get_width() // 2

    sad_y = height // 4
    over_y = height // 2 - 40
    retry_y = height // 2 + 40

    reveal_speed = 2

    sad_reveal = min(frame_count * reveal_speed, sad_surface.get_height())
    over_reveal = min((frame_count - 10) * reveal_speed, over_surface.get_height()) if frame_count > 10 else 0
    retry_reveal = min((frame_count - 20) * reveal_speed, retry_surface.get_height()) if frame_count > 20 else 0

    if sad_reveal > 0:
        sad_clip = sad_surface.subsurface((0, 0, sad_surface.get_width(), sad_reveal))
        win.blit(sad_clip, (sad_x, sad_y))

    if over_reveal > 0:
        over_clip = over_surface.subsurface((0, 0, over_surface.get_width(), over_reveal))
        win.blit(over_clip, (over_x, over_y))

    if retry_reveal > 0:
        retry_clip = retry_surface.subsurface((0, 0, retry_surface.get_width(), retry_reveal))
        win.blit(retry_clip, (retry_x, retry_y))

def render_victory_screen(win, width, height, title_font, subtitle_font, frame_count):
    win.fill((0, 0, 0))
    happy_surface = title_font.render(":D", True, (0, 255, 0))
    win_surface = title_font.render("YOU WIN!", True, (255, 255, 255))
    praise_surface = subtitle_font.render("You're a Pong Master!", True, (0, 255, 255))

    center_x = width // 2
    happy_x = center_x - happy_surface.get_width() // 2
    win_x = center_x - win_surface.get_width() // 2
    praise_x = center_x - praise_surface.get_width() // 2

    happy_y = height // 4
    win_y = height // 2 - 40
    praise_y = height // 2 + 40

    reveal_speed = 2

    happy_reveal = min(frame_count * reveal_speed, happy_surface.get_height())
    win_reveal = min((frame_count - 10) * reveal_speed, win_surface.get_height()) if frame_count > 10 else 0
    praise_reveal = min((frame_count - 20) * reveal_speed, praise_surface.get_height()) if frame_count > 20 else 0

    if happy_reveal > 0:
        happy_clip = happy_surface.subsurface((0, 0, happy_surface.get_width(), happy_reveal))
        win.blit(happy_clip, (happy_x, happy_y))

    if win_reveal > 0:
        win_clip = win_surface.subsurface((0, 0, win_surface.get_width(), win_reveal))
        win.blit(win_clip, (win_x, win_y))

    if praise_reveal > 0:
        praise_clip = praise_surface.subsurface((0, 0, praise_surface.get_width(), praise_reveal))
        win.blit(praise_clip, (praise_x, praise_y))

    pygame.display.flip()
