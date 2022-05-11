# a pygame console surface to display text, and process user commands

from collections import deque

from pygame_core import *

game = get_game()
eh, am, sm, = game.handles

console_surface = pygame.Surface((game.width, game.height // 4))
console_commands = dict()
current_command = ""
command_history = deque(maxlen=10)
command_history.appendleft("")
command_history_index = 0
output_lines = [f"{game.title} v{game.version}"]
output_lines_index = 0
cursor_pos = (0, 0)
cursor_visible = True
cursor = "|"
cursor_color = (255, 255, 255)
# make transparent
console_surface.set_colorkey((0, 0, 0))

# monospace font
font = pygame.font.Font(None, game.height // 25)


# decorator to register a function as a command
def command(name):
    def decorator(func):
        console_commands[name] = func
        return func

    return decorator


def run_command(_command, *args):
    global console_commands
    if _command in console_commands.keys():
        output_lines.append(_command + " " + " ".join(args))
        returned = console_commands[_command](*args)
        if returned is not None:
            output_lines.append(returned)
    else:
        output_lines.append(f"Unknown command: {_command}")


@eh(pygame.KEYDOWN)
def handle_input(event):
    global current_command
    global command_history_index
    global cursor_pos
    if event.key == pygame.K_F1:
        sm.set_states(console_view=not sm.get_state("console_view"))
    elif sm.get_state("console_view"):
        if event.key == pygame.K_BACKSPACE:
            current_command = current_command[:-1]
            update_cursor()
        elif event.key == pygame.K_DELETE:
            current_command = current_command[1:]
            update_cursor()
        elif event.key == pygame.K_RETURN:
            run_command(*current_command.split(" "))
            command_history.appendleft(current_command)
            current_command = ""
            command_history_index = 0
            update_cursor()

        elif event.key == pygame.K_UP:
            if command_history_index < len(command_history):
                command_history_index += 1
                current_command = command_history[command_history_index]
                update_cursor()
        elif event.key == pygame.K_DOWN:
            if command_history_index > 0:
                command_history_index -= 1
                current_command = command_history[command_history_index]
                update_cursor()
        elif event.key == pygame.K_LEFT:
            if cursor_pos[0] > 0:
                cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
                update_cursor()
        elif event.key == pygame.K_RIGHT:
            if cursor_pos[0] < len(current_command):
                cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
                update_cursor()
        elif event.key == pygame.K_HOME:
            cursor_pos = (0, cursor_pos[1])
            update_cursor()
        elif event.key == pygame.K_END:
            cursor_pos = (len(current_command), cursor_pos[1])
            update_cursor()
        elif event.key == pygame.K_SPACE:
            current_command += " "
        elif event.key == pygame.K_TAB:
            pass
        elif event.key == pygame.K_ESCAPE:
            sm.set_states(console_view=False)
        elif event.key in \
                [key for key in range(pygame.K_a, pygame.K_z + 1)] + \
                [key for key in range(pygame.K_0, pygame.K_9 + 1)] + \
                [pygame.K_MINUS, pygame.K_EQUALS, pygame.K_BACKSLASH, pygame.K_BACKQUOTE, pygame.K_SEMICOLON,
                 pygame.K_QUOTE, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_LEFTBRACKET,
                 pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH]:
            current_command += chr(event.key).upper() \
                if event.mod & pygame.KMOD_SHIFT \
                else chr(event.key)
            update_cursor()


def print_to_console(text):
    global output_lines
    for line in text.split("\n"):
        output_lines.append(line)


def init():
    sm.add_states(console_view=False)


def render(screen):
    global output_lines_index
    if sm.get_state("console_view"):
        screen.blit(font.render(current_command, True, (255, 255, 255)), (10, 10))
        screen.blit(font.render("_", True, (255, 255, 255)), (10 + cursor_pos[0] * font.size("_")[0], 10))
        for i, line in enumerate(output_lines[::-1]):
            screen.blit(font.render(line, True, (255, 255, 255)), (10, 25 + i * font.size("_")[1]))


def update_cursor():
    global cursor_pos
    cursor_pos = (cursor_pos[0], cursor_pos[1])


@command("clear")
def clear():
    """Clears the console."""
    global output_lines
    output_lines = []


@command("help")
def get_help():
    """Prints a list of available commands."""
    for _command in list(console_commands.keys())[::-1]:
        output_lines.append(
            f"    {_command} - {console_commands[_command].__doc__ if console_commands[_command].__doc__ else ''}")
    output_lines.append("Available commands:")


@command("exit")
def exit():
    """Exits the game."""
    eh.handle(pygame.QUIT)
