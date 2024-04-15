import random
import gym
from gym import spaces
import numpy as np
from utils import calculate_trajectory, calculate_reward
from constants import grid_size

class ParabolicShotEnv(gym.Env):
    metadata = {'render.modes': ['human', 'console']}

    def __init__(self, mode='human'):
        self.grid_size = grid_size
        self.mode = mode
        # Corrección y expansión del espacio de observaciones
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 5]),  # x inicial, z inicial, x objetivo, z objetivo, ángulo x, ángulo y, velocidad mínima
            high=np.array([self.grid_size, self.grid_size, self.grid_size, self.grid_size, 180, 90, 100]),  # x inicial, z inicial, x objetivo, z objetivo, ángulo x máximo, ángulo y máximo, velocidad máxima
            dtype=np.float32
        )
        self.action_space = spaces.Box(low=np.array([0, 0, 5]), high=np.array([180, 90, 100]), dtype=np.float32)

    def reset(self):
        self.v0, self.angle_x, self.angle_y = 30, 45, 45
        self.trajectory = []
        self.fired = False
        self.initial_pos = (0,0,0)
        self.target_pos = (10,10,0)
        self.state = self._update_state()
        self.reward = 0
        self.done = False
        return self.state

    def step(self, action):
        # Acción directa y disparo
        self.angle_x = action['angle_x']
        self.angle_y = action['angle_y']
        self.v0 = action['v0']
        self.shoot()

        self.state = self._update_state()
        info = {"trajectory_length": len(self.trajectory)}
        return self.state, self.reward, self.done, info, self.trajectory

    def _update_state(self):
        # Función para actualizar el estado
        return np.array([*self.initial_pos, *self.target_pos, self.angle_x / 180, self.angle_y / 90, (self.v0 - 5) / 95])

    def shoot(self):
        # Ejecución del disparo y cálculo de la recompensa
        self.trajectory = calculate_trajectory(self.initial_pos[0],self.initial_pos[1],self.initial_pos[2], self.v0, self.angle_x, self.angle_y)
        self.reward = calculate_reward(self.trajectory, self.target_pos)
        self.fired = True
        self.done = True

    def render(self, mode='human'):
        if mode == 'human':
            print("Rendering Environment")
            print(f"Initial Position: {self.initial_pos}")
            print(f"Target Position: {self.target_pos}")
            print(f"Current State: {self.state}")
            print(f"Trajectory: {self.trajectory}")

    def close(self):
        print("Environment closed.")