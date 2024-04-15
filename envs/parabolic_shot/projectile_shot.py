# Creado por: [@MrCabss69]
# Fecha de creación: Fri Apr 12 2024

import math

class ProjectileShot:
    def __init__(self, initial_velocity=30, angle_x=90, angle_y=45, wind_speed=0, wind_direction=0):
        self.initial_velocity = initial_velocity
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
    
    def calculate_trajectory(self, x0, y0, z0):
        wind_direction_rad = math.radians(self.wind_direction)
        wind_speed_x = self.wind_speed * math.cos(wind_direction_rad)
        wind_speed_y = self.wind_speed * math.sin(wind_direction_rad)
        angle_x_rad, angle_y_rad = math.radians(self.angle_x), math.radians(self.angle_y)
        vx = self.initial_velocity * math.cos(angle_x_rad) * math.cos(angle_y_rad)
        vy = self.initial_velocity * math.sin(angle_x_rad) * math.cos(angle_y_rad)
        vz = self.initial_velocity * math.sin(angle_y_rad)
        dt, t, trajectory = 0.01, 0, []

        while z >= 0:
            x = x0 + vx * t
            y = y0 + vy * t
            z = z0 + vz * t - 0.5 * 9.81 * t**2  # Usar constante de gravedad directamente
            trajectory.append((x, y, z))
            vx += wind_speed_x * dt
            vy += wind_speed_y * dt
            vz -= 9.81 * dt  # Actualizar vz por gravedad
            t += dt
            if z < 0:  # Romper cuando el proyectil alcanza el suelo
                break

        return trajectory

    def calculate_reward(self, trajectory, target_pos):
        if trajectory:
            last_point = trajectory[-1]
            target_distance = math.sqrt((last_point[0] - target_pos[0])**2 + (last_point[1] - target_pos[1])**2)
            return max(1 - target_distance, 0)  # Normalizar y evitar recompensas negativas
        return 0
