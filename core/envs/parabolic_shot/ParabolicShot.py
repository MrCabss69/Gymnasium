# Creado por: [@MrCabss69]
# Fecha de creación: Fri Apr 12 2024

import gym
from gym import spaces
import pygame
import numpy as np
from projectile_shot import ProjectileShot
from constants import grid_size
from render import Renderer

class EventHandler:
    def handle_events(self, env):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                env.adjust_parameters(event.key)
        return True

class ParabolicShotEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.grid_size = grid_size
        super().__init__()
        self.dynamics = ProjectileShot()
        self.renderer = Renderer(window_size=600, scale_factor=self.grid_size / 10)
        self.handler = EventHandler()
        self.observation_space = spaces.Box(low=np.array([0]*7), high=np.array([self.grid_size]*2 + [180, 90, 100] + [self.grid_size]*2), dtype=np.float32)
        self.action_space = spaces.Dict({
            "continuous": spaces.Box(low=np.array([-5, -5, -5]), high=np.array([5, 5, 5]), dtype=np.float32),
            "discrete": spaces.Discrete(2)  # 0 no disparar, 1 disparar
        })
        
    def reset(self):
        self.v0, self.angle_x, self.angle_y = 30, 90, 45
        self.trajectory = []
        self.fired = False
        self.initial_pos = (self.grid_size / 2, 5, 0)
        self.target_pos = (np.random.uniform(10, self.grid_size - 10), np.random.uniform(10, self.grid_size - 10))
        self.state = np.array([self.initial_pos[0],self.initial_pos[1],self.target_pos[0],self.target_pos[1], self.angle_x, self.angle_y, self.v0], dtype=np.float32)
        self.wind_speed = 0
        self.wind_direction = 0
        self.reward = 0
        self.done = False
        pygame.quit()
        self.renderer = Renderer(window_size=600, scale_factor=self.grid_size / 10)
        return self.state
    
    def step(self, action):
        continuous_actions = action["continuous"]
        discrete_action = action["discrete"]
        
        delta_angle_x, delta_angle_y, delta_v0 = continuous_actions
        self.angle_x = np.clip(self.angle_x + delta_angle_x, 0, 180)
        self.angle_y = np.clip(self.angle_y + delta_angle_y, 0, 90)
        self.v0 = np.clip(self.v0 + delta_v0, 5, 100)

        if discrete_action == 1 and not self.fired:
            self.shoot()

        info = {"trajectory_length": len(self.trajectory)}
        return self.state, self.reward, self.done, info

    def render(self, mode='human'):
        if mode == 'human':
            self.renderer.render(
                self.initial_pos,
                self.trajectory,
                self.target_pos,
                self.angle_x,
                self.angle_y,
                self.v0,
                self.wind_speed,
                self.wind_direction
            )
            
    def shoot(self):
        self.trajectory = self.dynamics.calculate_trajectory(*self.initial_pos)
        self.reward = self.dynamics.calculate_reward(self.trajectory, self.target_pos)
        self.fired = True
        self.done = True  
    
    def adjust_parameters(self, key):
        mapping = {
            pygame.K_UP: [0, 1, 0, 0],
            pygame.K_DOWN: [0, -1, 0, 0],
            pygame.K_RIGHT: [-1, 0, 0, 0],
            pygame.K_LEFT: [1, 0, 0, 0],
            pygame.K_c: [0, 0, -1, 0],
            pygame.K_v: [0, 0, 1, 0],
            pygame.K_SPACE: [0, 0, 0, 1]
        }
        if key == pygame.K_r:
            return self.reset()
        elif key in mapping:
            return self.step(mapping[key])

    def close(self):
        pygame.quit()

if __name__ == '__main__':
    env = ParabolicShotEnv()
    running = True
    env.reset()
    while running:
        running = env.handler.handle_events(env)
        env.render()
    env.close()
