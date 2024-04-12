# Creado por: [@MrCabss69]
# Fecha de creación: Fri Apr 12 2024

import math
import random
from constants import CONSTANTES, grid_size

class ProjectileShot:
    def __init__(self):
        self.initial_velocity = 30
        self.angle_x = 90
        self.angle_y = 45
        self.trajectory = []
        self.wind_speed = random.uniform(-5, 5)  # m/s
        self.wind_direction = random.uniform(0, 360)  # Degrees

    def calculate_trajectory(self, x0, y0, z0):
        wind_direction_rad = math.radians(self.wind_direction)
        wind_speed_x = self.wind_speed * math.cos(wind_direction_rad)
        wind_speed_y = self.wind_speed * math.sin(wind_direction_rad)

        angle_x_rad, angle_y_rad = math.radians(self.angle_x), math.radians(self.angle_y)
        vx, vy, vz = self.initial_velocity * math.cos(angle_x_rad) * math.cos(angle_y_rad), self.initial_velocity * math.sin(angle_x_rad) * math.cos(angle_y_rad), self.initial_velocity * math.sin(angle_y_rad)
        dt, t, trajectory = 0.01, 0, []

        while True:
            x, y, z = x0 + vx * t, y0 + vy * t, z0 + vz * t - 0.5 * CONSTANTES["GRAVITY"] * t**2
            if z < 0 or x < 0 or x > grid_size or y < 0 or y > grid_size: 
                break

            air_resistance = 0.5 * CONSTANTES["AIR_DENSITY"] * (vx**2 + vy**2) * CONSTANTES["CROSS_SECTIONAL_AREA"] * CONSTANTES["DRAG_COEFFICIENT"]
            vx -= air_resistance * dt - wind_speed_x * dt  # Adjusted for wind
            vy -= air_resistance * dt - wind_speed_y * dt  # Adjusted for wind
            vz -= CONSTANTES["GRAVITY"] * dt
            trajectory.append((x, y, z))
            t += dt

        return trajectory

    def calculate_reward(self, trajectory, target_pos):
        if trajectory:
            last_point = trajectory[-1]
            target_distance = math.sqrt((last_point[0] - target_pos[0])**2 + (last_point[1] - target_pos[1])**2)
            return max(grid_size - target_distance, 0)
        return 0
