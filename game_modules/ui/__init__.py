import pygame

from pygame_core import get_game
game = get_game()
eh, am, sm = game.handles

sm.register_state('debug', False)


def update():
    pass


def render_debug_info(screen):
    # Draw debug info
    font = pygame.font.SysFont('monospace', 12)

    fps = int(game.clock.get_fps())
    fps_text = font.render(f'FPS: {fps}', True, (255, 255, 255))
    screen.blit(fps_text, (5, 5))

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_text = font.render(f'Mouse: {mouse_pos}', True, (255, 255, 255))
    screen.blit(mouse_pos_text, (5, 25))

    # print all game states
    states = sm.get_states()
    for index, (key, value) in enumerate(states.items()):
        state_text = font.render(f'{key}: {value}', True, (255, 255, 255))
        screen.blit(state_text, (5, 45 + index * 15))

def render(screen):
    if sm.get_state('debug'):
        render_debug_info(screen)


@eh(pygame.KEYDOWN)
def toggle_debug(event):
    if event.key == pygame.K_F1:
        sm.set_state('debug', not sm.get_state('debug'))

