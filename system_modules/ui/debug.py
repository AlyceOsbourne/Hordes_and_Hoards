import pygame

from pygame_core import get_game

game = get_game()
event_handler, asset_handler, state_handler = game.handles

# monospace font
font = pygame.font.SysFont("monospace", 12)


def init():
    state_handler.add_states(debug_view=False)


def render_debug_info(screen):
    if state_handler.get_state('debug_view'):
        outputs = []
        font_surface = font.render(
            f'FPS: {int(game.get_fps())} |'
            f' RAM: {game.get_ram_usage() / 1024 / 1024:.2f}MB |'
            f' CPU: {game.get_cpu_usage():.2f}% |'
            f' CPU CORES: {game.get_num_cores()} |'
            f" DISK: {game.get_disk_usage() / 1024 / 1024:.2f}mb",
            True, (255, 255, 255))
        outputs.append(font_surface)

        num_assets_text = font.render(
            f'Loaded Assets -> '
            f'Images: {asset_handler.number_of_images()} '
            f'Fonts: {asset_handler.number_of_fonts()} '
            f'Sounds: {asset_handler.number_of_sounds()}',
            True,
            (255, 255, 255)
        )
        outputs.append(num_assets_text)

        # get name of all currently pressed keys
        pressed_keys = pygame.key.get_pressed()
        # get name for every key that is pressed
        # a-z
        pressed_keys_names = [pygame.key.name(key) for key in range(pygame.K_a, pygame.K_z + 1) if pressed_keys[key]]
        # 0-9
        pressed_keys_names += [pygame.key.name(key) for key in range(pygame.K_0, pygame.K_9 + 1) if pressed_keys[key]]
        # numpad 0-9
        pressed_keys_names += [pygame.key.name(key) for key in range(pygame.K_KP0, pygame.K_KP9 + 1) if pressed_keys[key]]
        # insert, delete, home, end, page up, page down,
        pressed_keys_names += [pygame.key.name(key) for key in [pygame.K_INSERT, pygame.K_DELETE, pygame.K_HOME, pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN] if pressed_keys[key]]
        # F1-F12
        pressed_keys_names += [pygame.key.name(key) for key in range(pygame.K_F1, pygame.K_F12 + 1) if pressed_keys[key]]
        # arrow keys
        pressed_keys_names += [pygame.key.name(key) for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] if pressed_keys[key]]
        # spacebar, return, tab, escape, backspace,
        pressed_keys_names += [pygame.key.name(key) for key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE, pygame.K_BACKSPACE] if pressed_keys[key]]
        # shift, ctrl, alt, capslock, numlock, scrolllock
        pressed_keys_names += [pygame.key.name(key) for key in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_CAPSLOCK, pygame.K_NUMLOCK, pygame.K_SCROLLOCK] if pressed_keys[key]]
        # punctuation keys
        pressed_keys_names += [pygame.key.name(key) for key in [pygame.K_MINUS, pygame.K_EQUALS, pygame.K_BACKQUOTE, pygame.K_QUOTE, pygame.K_SEMICOLON, pygame.K_SLASH, pygame.K_BACKSLASH, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET] if pressed_keys[key]]

        keys_text = font.render(
            f'Pressed Keys -> [{", ".join(pressed_keys_names)}]',
            True,
            (255, 255, 255)
        )

        outputs.append(keys_text)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_text = font.render(
            f'Mouse Pos -> '
            f'{mouse_pos[0]}, {mouse_pos[1]}',
            True,
            (255, 255, 255)
        )
        outputs.append(mouse_pos_text)
        loaded_modules = [module.__name__ for module in game.get_game_modules()]
        for module in loaded_modules:
            module_text = font.render(
                f'Loaded Module -> {module}',
                True,
                (255, 255, 255)
            )
            outputs.append(module_text)
        states = state_handler.get_all_states()
        states_text = font.render(
            f'States -> ',
            True,
            (255, 255, 255)
        )
        outputs.append(states_text)
        for index, (key, value) in enumerate(states.items()):
            state_text = font.render(f'  {key}: {value}', True, (255, 255, 255))
            outputs.append(state_text)

        for index, output in enumerate(outputs):
            screen.blit(output, (5, 5 + (index * 15)))


@event_handler(pygame.KEYDOWN)
def toggle_debug(event):
    if event.key == pygame.K_F12:
        state_handler.set_state('debug_view', not state_handler.get_state('debug_view'))
