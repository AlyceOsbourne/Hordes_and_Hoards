import pygame

from pygame_core import get_game

game = get_game()
eh, am, sm = game.handles

# monospace font
font = pygame.font.SysFont("monospace", 12)


def init():
    sm.add_states(debug_view=False)


def render_debug_info(screen):
    if sm.get_state('debug_view'):
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
            f'Images: {am.number_of_images()} '
            f'Fonts: {am.number_of_fonts()} '
            f'Sounds: {am.number_of_sounds()}',
            True,
            (255, 255, 255)
        )
        outputs.append(num_assets_text)

        # get name of all currently pressed keys
        pressed_keys = pygame.key.get_pressed()
        # get name for every key that is pressed
        pressed_keys_names = [
            pygame.key.name(key) for key in range(pygame.K_SPACE, pygame.K_DELETE + 1) if
            pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_0, pygame.K_9 + 1) if pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_a, pygame.K_z + 1) if pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_KP0, pygame.K_KP9 + 1) if pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_KP_DIVIDE, pygame.K_KP_PLUS + 1) if
            pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_KP_MULTIPLY, pygame.K_KP_EQUALS + 1) if
            pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in range(pygame.K_KP_MINUS, pygame.K_KP_PERIOD + 1) if
            pressed_keys[key]]
        pressed_keys_names += [
            pygame.key.name(key) for key in [
                pygame.K_ESCAPE,
                pygame.K_TAB,
                pygame.K_RETURN,
                pygame.K_BACKSPACE,
                pygame.K_DELETE]
            if pressed_keys[key]]
        # ctrl, alt, shift, etc
        pressed_keys_names += [
            pygame.key.name(key) for key in [
                pygame.K_LCTRL,
                pygame.K_RCTRL,
                pygame.K_LALT,
                pygame.K_RALT,
                pygame.K_LSHIFT,
                pygame.K_RSHIFT,
                pygame.K_CAPSLOCK,
                pygame.K_SCROLLOCK,
                pygame.K_NUMLOCK,
                pygame.K_PRINT,
                pygame.K_PAUSE,
            ]
            if pressed_keys[key]]

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

        states = sm.get_all_states()
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


@eh(pygame.KEYDOWN)
def toggle_debug(event):
    if event.key == pygame.K_F12:
        sm.set_state('debug_view', not sm.get_state('debug_view'))
