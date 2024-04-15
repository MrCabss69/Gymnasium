import random
import time 
import gym
from gym import spaces
import pygame
import numpy as np
import plotly.graph_objects as go
from projectile_shot import ProjectileShot
from constants import grid_size
from render_ply import Renderer

# pygame.init()

# class EventHandler:
#     def handle_events(self, env):
#         for event in pygame.event.get():
#             print(f"Event: {event}")  # Debugging: ver eventos
#             if event.type == pygame.QUIT:
#                 return False
#             elif event.type == pygame.KEYDOWN:
#                 env.adjust_parameters(event.key)
#         return True

# class ParabolicShotEnv(gym.Env):
#     metadata = {'render.modes': ['human']}

#     def __init__(self, mode='human'):
#         self.grid_size = grid_size
#         super().__init__()
#         self.dynamics = ProjectileShot()
#         self.mode = mode
#         self.observation_space = spaces.Box(low=np.zeros(7), high=np.array([self.grid_size, self.grid_size, 180, 90, 100, self.grid_size, self.grid_size]), dtype=np.float32)
#         self.action_space = spaces.Dict({
#             "continuous": spaces.Box(low=np.array([-5, -5, -5]), high=np.array([5, 5, 5]), dtype=np.float32),
#             "discrete": spaces.Discrete(2)  # 0 no fire, 1 fire
#         })

#     def reset(self):
#         self.v0, self.angle_x, self.angle_y = 30, 90, 45  # Initial conditions for the projectile
#         self.trajectory = []
#         self.fired = False
#         self.initial_pos = (self.grid_size / 2, self.grid_size / 10, 0)  # Slightly raised initial position
#         self.target_pos = (random.uniform(10, self.grid_size - 10), random.uniform(10, self.grid_size - 10))
#         self.state = np.array([self.initial_pos[0], self.initial_pos[1], self.target_pos[0], self.target_pos[1], self.angle_x, self.angle_y, self.v0])
#         self.wind_speed = random.uniform(-5, 5)
#         self.wind_direction = random.uniform(0, 360)
#         self.reward = 0
#         self.done = False
#         return self.state

#     def step(self, action):
#         continuous_actions = action["continuous"]
#         discrete_action = action["discrete"]
        
#         self.angle_x = np.clip(self.angle_x + continuous_actions[0], 0, 180)
#         self.angle_y = np.clip(self.angle_y + continuous_actions[1], 0, 90)
#         self.v0 = np.clip(self.v0 + continuous_actions[2], 5, 100)

#         if discrete_action == 1 and not self.fired:
#             self.shoot()

#         info = {"trajectory_length": len(self.trajectory)}
#         return self.state, self.reward, self.done, info

#     def shoot(self):
#         self.dynamics.set_conditions(self.v0, self.angle_x, self.angle_y, self.wind_speed, self.wind_direction)
#         self.trajectory = self.dynamics.calculate_trajectory(self.initial_pos)
#         self.reward = self.dynamics.calculate_reward(self.trajectory, self.target_pos)
#         self.fired = True
#         self.done = True  # Optionally set to true if the environment should reset after each shot

#     def render(self, mode='human'):
#         print("Rendering...")  # Debugging
#         if mode == 'human':
#             fig = go.Figure()
#             if self.trajectory:
#                 fig.add_trace(go.Scatter(x=[pos[0] for pos in self.trajectory],
#                                         y=[pos[1] for pos in self.trajectory],
#                                         mode='lines+markers',
#                                         name='Trajectory'))
#             fig.add_trace(go.Scatter(x=[self.initial_pos[0], self.target_pos[0]],
#                                      y=[self.initial_pos[1], self.target_pos[1]],
#                                      mode='markers',
#                                      marker=dict(size=10, color='red'),
#                                      name='Start & Target'))
#             fig.update_layout(title='Projectile Trajectory',
#                               xaxis_title='X Position',
#                               yaxis_title='Y Position',
#                               yaxis=dict(scaleanchor="x", scaleratio=1),
#                               xaxis=dict(constrain='domain'),
#                               width=600,
#                               height=600)
#             fig.show()
#         else:
#             print("No trajectory to render.")  # Debugging

#     def shoot(self):
#         print("Shooting...")  # Debugging
#         self.dynamics.wind_speed = random.uniform(-5, 5)
#         self.dynamics.wind_direction = random.uniform(0, 360)
#         self.dynamics.angle_x = self.angle_x
#         self.dynamics.angle_y = self.angle_y
#         self.dynamics.initial_velocity = self.v0
#         self.trajectory = self.dynamics.calculate_trajectory(*self.initial_pos)
#         self.reward = self.dynamics.calculate_reward(self.trajectory, self.target_pos)
#         self.fired = True
#         self.done = True

#     def adjust_parameters(self, key):
#         mapping = {
#             pygame.K_UP: ["continuous", 0, 1, 0],
#             pygame.K_DOWN: ["continuous", 0, -1, 0],
#             pygame.K_RIGHT: ["continuous", -1, 0, 0],
#             pygame.K_LEFT: ["continuous", 1, 0, 0],
#             pygame.K_c: ["continuous", 0, 0, -1],
#             pygame.K_v: ["continuous", 0, 0, 1],
#             pygame.K_SPACE: ["discrete", 1]
#         }
#         if key == pygame.K_r:
#             return self.reset()
#         elif key in mapping:
#             action_type, values = mapping[key]
#             if action_type == "continuous":
#                 action = {"continuous": np.array(values[:3], dtype=np.float32), "discrete": 0}
#             else:  # Discrete
#                 action = {"continuous": np.array([0, 0, 0], dtype=np.float32), "discrete": values}
#             return self.step(action)

#     def close(self):
#         if self.mode == 'human':
#             pygame.quit()




class ParabolicShotEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, mode='human'):
        self.grid_size = grid_size
        super().__init__()
        self.dynamics = ProjectileShot()
        self.mode = mode
        self.renderer = Renderer(window_size=600)  # Assuming a window size for visualizations
        self.observation_space = spaces.Box(low=np.zeros(7), high=np.array([self.grid_size, self.grid_size, 180, 90, 100, self.grid_size, self.grid_size]), dtype=np.float32)
        self.action_space = spaces.Dict({
            "continuous": spaces.Box(low=np.array([-5, -5, -5]), high=np.array([5, 5, 5]), dtype=np.float32),
            "discrete": spaces.Discrete(2)  # 0 no fire, 1 fire
        })

    def reset(self):
        self.v0, self.angle_x, self.angle_y = 30, 90, 45
        self.trajectory = []
        self.fired = False
        self.initial_pos = (self.grid_size / 2, self.grid_size / 10)
        self.target_pos = (random.uniform(10, self.grid_size - 10), random.uniform(10, self.grid_size - 10))
        self.state = np.array([self.initial_pos[0], self.initial_pos[1], self.target_pos[0], self.target_pos[1], self.angle_x, self.angle_y, self.v0])
        self.wind_speed = random.uniform(-5, 5)
        self.wind_direction = random.uniform(0, 360)
        self.reward = 0
        self.done = False
        return self.state

    def step(self, action):
        continuous_actions = action["continuous"]
        discrete_action = action["discrete"]
        
        self.angle_x = np.clip(self.angle_x + continuous_actions[0], 0, 180)
        self.angle_y = np.clip(self.angle_y + continuous_actions[1], 0, 90)
        self.v0 = np.clip(self.v0 + continuous_actions[2], 5, 100)

        if discrete_action == 1 and not self.fired:
            self.shoot()

        self.state = np.array([self.initial_pos[0], self.initial_pos[1], self.target_pos[0], self.target_pos[1], self.angle_x, self.angle_y, self.v0])
        info = {"trajectory_length": len(self.trajectory)}
        return self.state, self.reward, self.done, info

    def render(self, mode='human'):
        if mode == 'human':
            self.renderer.render(self.trajectory, self.initial_pos, self.target_pos, self.wind_speed, self.wind_direction)

    def shoot(self):
        # Simulate shooting based on the dynamics model
        self.trajectory = self.dynamics.calculate_trajectory(self.initial_pos, self.v0, self.angle_x, self.angle_y, self.wind_speed, self.wind_direction)
        self.reward = self.dynamics.calculate_reward(self.trajectory, self.target_pos)
        self.fired = True
        self.done = True

    def close(self):
        print("Environment closed.")
        
        
if __name__ == '__main__':
    env = ParabolicShotEnv()
    running = True
    env.reset()
    while running:
        env.render()
        
    env.close()
