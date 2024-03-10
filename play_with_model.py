# Creado por: [@MrCabss69]
# Fecha de creación: Mon Mar 11 2024
import gymnasium as gym
from tensorflow.keras.models import load_model

class ModelPlayer:
    def __init__(self, model_path, env_name='CartPole-v1'):
        self.model = self.load_model(model_path)
        self.env = gym.make(env_name, render_mode="human")

    def load_model(self, model_path):
        return load_model(model_path)

    def play(self, episodes=5):
        for episode in range(episodes):
            state, _ = self.env.reset()
            done = False
            score = 0
            while not done:
                action = self.predict_action(state)
                state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                score += reward
            print(f"Episode: {episode + 1}, Score: {score}")
        self.env.close()

    def predict_action(self, state):
        q_values = self.model.predict(state.reshape(1, -1))
        return q_values.argmax()

# Ejemplo de uso:
model_player = ModelPlayer('dqn_1k.h5')
model_player.play(episodes=10)
