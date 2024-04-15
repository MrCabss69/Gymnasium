import math
from constants import GRAVEDAD

def calculate_trajectory(x0, y0, z0, v0, angulo_x, angulo_y):
    angulo_x_rad = math.radians(angulo_x)
    angulo_y_rad = math.radians(angulo_y)
    vx = v0 * math.cos(angulo_x_rad) * math.cos(angulo_y_rad)
    vy = v0 * math.sin(angulo_x_rad) * math.cos(angulo_y_rad)
    vz = v0 * math.sin(angulo_y_rad)
    
    trayectoria = []
    dt = 0.01  # Intervalo de tiempo
    t = 0
    while z0 >= 0:
        x = x0 + vx * t
        y = y0 + vy * t
        z = z0 + vz * t - 0.5 * GRAVEDAD * t**2
        if z < 0: 
            break
        vz -= GRAVEDAD * dt
        if x and y and z:
            trayectoria.append((x, y, z))
        t += dt
    
    return trayectoria


def calculate_reward(trajectory, target_pos):
    if trajectory:
        last_point = trajectory[-1]
        target_distance = math.sqrt((last_point[0] - target_pos[0])**2 + (last_point[1] - target_pos[1])**2)
        return max(1 - target_distance, 0)  # Normalizar y evitar recompensas negativas
    return 0