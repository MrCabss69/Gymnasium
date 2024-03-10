## Q-Learning

### Tips para la implementación
- Utilizar una estructura de datos eficiente para almacenar la tabla Q, como un diccionario de Python para entornos con espacios de estado-acción discretos.
- Para entornos con espacios continuos, considerar la aproximación de función, como las redes neuronales.
- Asegurarse de explorar el espacio de acciones usando una política como ε-greedy para balancear la exploración y la explotación.
- Ajustar cuidadosamente los parámetros α (tasa de aprendizaje) y γ (factor de descuento) para optimizar el rendimiento del algoritmo.
- Considerar el decaimiento de ε en la política ε-greedy para reducir la exploración a medida que el agente aprende.

### Pseudocódigo
1. Inicializar la tabla Q arbitrariamente para todos los pares estado-acción.
2. Para cada episodio:
    - 2.1. Inicializar el estado S.
    - 2.2. Elegir una acción A desde el estado S usando la política derivada de Q (por ejemplo, ε-greedy).
    - 2.3. Repetir para cada paso del episodio:
        - 2.3.1. Tomar la acción A, observar la recompensa R y el nuevo estado S'.
        - 2.3.2. Elegir A' desde S' usando la política derivada de Q (ε-greedy).
        - 2.3.3. Actualizar la tabla Q usando la ecuación:
            Q(S, A) <- Q(S, A) + α[R + γ Q(S', A') - Q(S, A)]
        - 2.3.4. S <- S'; A <- A' (Actualizar el estado y la acción para el próximo paso).
    - 2.4. Hasta que el episodio termine.