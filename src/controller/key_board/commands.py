import pygame

class Commands:

    commands = ["up", "down", "left", "right"]
    commands_int = [0, 1, 2, 3]
    commands_keyboard = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right"
    }

    @staticmethod
    def get_from_int(index: int):
        return Commands.commands[index]

    @staticmethod
    def get_from_key_board(*args):
        keys = pygame.key.get_pressed()
        command = "None"
        if keys[pygame.K_LEFT]:
            command = "left"
        if keys[pygame.K_RIGHT]:
            command = "right"
        if keys[pygame.K_UP]:
            command = "up"
        if keys[pygame.K_DOWN]:
            command = "down"
        return command


