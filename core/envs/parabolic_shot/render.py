# Creado por: [@MrCabss69]
# Fecha de creación: Fri Apr 12 2024

import pygame
import math
from constants import COLORS

class Renderer:
    def __init__(self, window_size, scale_factor):
        self.window_size = window_size
        self.scale_factor = scale_factor
        self.initialize_pygame()
        

    def initialize_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption('Shot Aim 2D Simulation')
        self.font = pygame.font.SysFont('Arial', 20)

    def draw_background(self):
        for x in range(0, self.window_size, 20):
            pygame.draw.line(self.window, COLORS["LIGHT_GRAY"], (x, 0), (x, self.window_size))
        for y in range(0, self.window_size, 20):
            pygame.draw.line(self.window, COLORS["LIGHT_GRAY"], (0, y), (self.window_size, y))

    def draw_wind(self, wind_speed, wind_direction):
        center_x, center_y = 50, 50  # Adjusted for clarity
        length = wind_speed * 10
        end_x = center_x + length * math.cos(math.radians(wind_direction))
        end_y = center_y - length * math.sin(math.radians(wind_direction))

        pygame.draw.line(self.window, COLORS["BLACK"], (center_x, center_y), (end_x, end_y), 3)
        pygame.draw.polygon(self.window, COLORS["BLACK"], [
            (end_x, end_y),
            (end_x - 5 * math.cos(math.radians(wind_direction) - math.pi / 6), end_y + 5 * math.sin(math.radians(wind_direction) - math.pi / 6)),
            (end_x - 5 * math.cos(math.radians(wind_direction) + math.pi / 6), end_y - 5 * math.sin(math.radians(wind_direction) + math.pi / 6))
        ])
        wind_speed_surface = self.font.render(f'{wind_speed:.1f} m/s', True, COLORS["BLACK"])
        self.window.blit(wind_speed_surface, (end_x + 5, end_y))

    def draw_information_panel(self, angle_x, angle_y, v0):
        pygame.draw.rect(self.window, (255, 255, 255, 128), pygame.Rect(10, self.window_size - 90, 180, 80))
        self.blit_text(f'Angle X: {angle_x}°', (20, self.window_size - 80), COLORS["BLACK"])
        self.blit_text(f'Angle Y: {angle_y}°', (20, self.window_size - 60), COLORS["BLACK"])
        self.blit_text(f'V0: {v0} m/s', (20, self.window_size - 40), COLORS["BLACK"])

    def blit_text(self, text, position, color):
        text_surface = self.font.render(text, True, color)
        self.window.blit(text_surface, position)

    def render(self, initial_pos, trajectory, target_pos, angle_x, angle_y, v0, wind_speed, wind_direction):
        self.window.fill(COLORS["WHITE"])
        self.draw_background()
        self.draw_wind(wind_speed, wind_direction)
        self.draw_information_panel(angle_x, angle_y, v0)

        start_pixel_pos = self.convert_to_pixels(*initial_pos[:2])
        target_pixel_pos = self.convert_to_pixels(*target_pos)
        pygame.draw.circle(self.window, COLORS["RED"], start_pixel_pos, 5)
        pygame.draw.circle(self.window, COLORS["GREEN"], target_pixel_pos, 10)

        if trajectory:
            pygame.draw.lines(self.window, COLORS["BLUE"], False, [self.convert_to_pixels(x, y) for x, y, _ in trajectory], 2)

        pygame.display.flip()

    def convert_to_pixels(self, x, y):
        return int(x * self.scale_factor), int(self.window_size - y * self.scale_factor)
