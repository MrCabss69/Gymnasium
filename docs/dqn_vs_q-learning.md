
# **Diferencias entre Q-Learning y DQN**

Exploramos las diferencias fundamentales entre el enfoque tradicional de Q-Learning y el más avanzado Deep Q-Network (DQN), destacando mejoras clave en términos de eficiencia, estabilidad y capacidad de generalización.

## 1. **Experience Replay**

- **Q-Learning:** Se entrena iterativamente en cada paso, utilizando experiencias recientes. La alta correlación entre muestras consecutivas puede resultar en aprendizaje ineficiente y alta varianza en las actualizaciones.
- **DQN:** Emplea un "buffer de repetición de experiencia", almacenando transiciones pasadas. Muestrea aleatoriamente de este buffer para el entrenamiento, disminuyendo la correlación entre muestras y estabilizando el aprendizaje.

## 2. **Fixed Q-Targets**

- **Q-Learning:** Utiliza la misma red en actualización para calcular los valores objetivo, lo que puede llevar a divergencias o oscilaciones debido a un feedback loop positivo.
- **DQN:** Introduce una red objetivo separada para calcular los valores Q, cuyos pesos se actualizan con menos frecuencia, proporcionando objetivos más estables y reduciendo la varianza.

## 3. **Uso de Políticas Más Complejas**

- **Q-Learning:** Adopta una política codiciosa, seleccionando siempre la acción de mayor valor Q, lo cual puede limitar la exploración.
- **DQN:** Implementa políticas como ε-greedy, alternando entre la mejor acción y una selección aleatoria, promoviendo un balance entre exploración y explotación.

## 4. **Optimizaciones de Red y Algoritmos**

- **Q-Learning:** La configuración de red y algoritmo de optimización son estándar y podrían no ser ideales para tareas específicas.
- **DQN:** Permite la integración de técnicas avanzadas de optimización, como inicializaciones de peso específicas, tasas de aprendizaje adaptativas y regularizaciones, mejorando la estabilidad y eficacia del entrenamiento.

## **Pseudocódigo**

#### Inicialización:

Se establecen los cimientos del algoritmo con tres pasos clave:

1. Se crea la **red Q** con pesos aleatorios, destinada a aprender y tomar decisiones.

2. Se duplica esta red en la **red objetivo Q** para proporcionar estabilidad durante el aprendizaje.

3. Se prepara el **buffer de experiencia**, un almacén de interacciones pasadas del algoritmo, para facilitar el aprendizaje de diversas situaciones.



#### Durante cada episodio de entrenamiento, en cada paso del episodio, el algoritmo:
- Se inicializa el estado inicial

- Elige y ejecuta una acción basada en la política ε-greedy, observando la recompensa y el nuevo estado.

- Guarda la experiencia en el buffer y entrena con un minibatch aleatorio de este, ajustando los pesos de la red Q para minimizar las diferencias entre los valores objetivo y predichos.

- Actualiza la red objetivo Q regularmente para mantener la consistencia en los objetivos de aprendizaje.

Este ciclo se repite a lo largo de múltiples episodios, permitiendo que la red Q refine continuamente su capacidad para tomar decisiones óptimas.

