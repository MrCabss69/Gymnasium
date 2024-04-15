from flask import Flask, jsonify, request
from flask_cors import CORS
from enviroment import ParabolicShotEnv  # Asegúrate de que este módulo y el nombre estén correctamente definidos
from utils import calculate_trajectory
app = Flask(__name__)
CORS(app)

env = ParabolicShotEnv()

# @app.route('/simulate', methods=['POST'])
# def simulate():
#     data = request.json
#     required_keys = ['v0', 'angulo_x', 'angulo_y', 'x0', 'y0', 'z0']
#     if not all(key in data for key in required_keys):
#         return jsonify({"error": "Missing data for simulation"}), 400
#     try:
#         # Asumimos que 'calculate_trajectory' ha sido adecuadamente actualizado para manejar estos parámetros.
#         trajectory = calculate_trajectory(**data)
#         if trajectory is None or not trajectory:
#             return jsonify({"error": "Invalid trajectory data"}), 400
#         return jsonify(trajectory), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

@app.route('/step', methods=['POST'])
def step():
    action = request.json
    try:
        # Asegurar que los datos recibidos son adecuados para la acción esperada
        if not all(key in action for key in ['angle_x', 'angle_y', 'v0']):
            return jsonify({"error": "Missing parameters for action"}), 400
        # Convertir a los tipos adecuados si necesario
        action_converted = {
            'angle_x': float(action['angle_x']),
            'angle_y': float(action['angle_y']),
            'v0': float(action['v0'])
        }
        state, reward, done, info, trajectory = env.step(action_converted)
        return jsonify({
            "state": state.tolist(),
            "reward": reward,
            "done": done,
            "info": info,
            "trajectory": trajectory
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/reset', methods=['GET'])
def reset():
    try:
        state = env.reset()
        return jsonify(state.tolist()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# RESPONSE:   
# [
#   40.0,
#   8.0,
#   40.0,
#   57.7910197695874,
#   8.0,
#   52.231003245117094,
#   45.0,
#   45.0,
#   30.0
# ]

@app.route('/close', methods=['GET'])
def close():
    try:
        env.close()
        return jsonify({"message": "Environment closed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)