🏎️ Formula Q - Optimización de Estrategia F1 con Q-Learning

Sistema de aprendizaje por refuerzo para determinar la estrategia óptima de carrera en Fórmula 1 utilizando Q-Learning. El agente aprende qué nivel de agresividad (conservadora, normal, agresiva) maximiza las probabilidades de ganar el campeonato según la posición de salida en parrilla.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Descripción

Este proyecto simula un escenario real de Fórmula 1 donde Lando Norris compite contra Max Verstappen y Oscar Piastri por el campeonato. El agente de Q-Learning aprende la política óptima considerando:

- **Estados**: Posición de salida en parrilla (Pole, P2-P3, P4-P6)
- **Acciones**: Estrategia de carrera (Conservadora, Normal, Agresiva)
- **Objetivo**: Maximizar probabilidad de ganar el campeonato
- **Trade-off**: Velocidad vs. riesgo de DNF (Did Not Finish)

Características

- Implementación completa de Q-Learning con epsilon-greedy
- Ambiente personalizado con distribuciones probabilísticas realistas
- Simulación visual interactiva con PyGame siguiendo trayectoria del circuito
- Visualización de resultados (rewards, Q-table, política óptima)
- Análisis automático de estrategia aprendida
- Logging detallado del proceso de entrenamiento

Instalación

Requisitos
- Python 3.8 o superior
- pip

Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/TaniaAraque/Proyecto-3-IA-F1-ML.git
cd Proyecto-3-IA-F1-ML
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

Uso

### Entrenamiento y Simulación

Para entrenar el agente y ejecutar la simulación visual:

```bash
python main.py
```

Esto ejecutará:
1. Entrenamiento con 10,000 episodios
2. Generación de gráficas en `/results`
3. Análisis de estrategia óptima (en consola)
4. Simulación visual animada (opcional)

Solo Entrenamiento (Modo Rápido)

Si deseas entrenar sin la simulación visual, comenta las líneas en `main.py`:

```python
# sim = F1RaceSim(env, Q, episodes=150)
# sim.run()
```
Herramienta de Mapeo de Circuito

Para crear tus propios waypoints del circuito:

```bash
python utils/track_mapper.py
```

Haz clic en la imagen para marcar puntos siguiendo la trayectoria.

Resultados

El sistema genera:

### 1. **Q-Table Final**
Matriz 3×3 con valores Q aprendidos para cada combinación estado-acción

### 2. **Estrategia Óptima**
```
ESTRATEGIA ÓPTIMA APRENDIDA:
============================================================
🥇 Desde Pole Position:
   → Estrategia: Normal
   → Probabilidad de victoria: 52.34%

🥈 Desde P2-P3:
   → Estrategia: Agresiva
   → Probabilidad de victoria: 48.67%

🥉 Desde P4-P6:
   → Estrategia: Normal
   → Probabilidad de victoria: 39.12%
```

### 3. **Visualizaciones**
- `results/reward_curve.png` - Convergencia del aprendizaje
- `results/Qtable_heatmap.png` - Heatmap de valores Q
- `results/policy.png` - Mejor acción por estado

## Estructura del Proyecto

```
F1-Q-Learning/
├── agent/
│   ├── __init__.py
│   └── q_learning.py          # Algoritmo Q-Learning
├── f1_env/
│   ├── __init__.py
│   └── environment.py         # Ambiente F1 personalizado
├── utils/
│   ├── __init__.py
│   ├── visualization.py       # Generación de gráficas
│   ├── sim_pygame_race.py     # Simulación visual
│   └── track_mapper.py        # Herramienta de mapeo
├── assets/
│   ├── track.png              # Imagen del circuito
│   ├── car_norris.png         # Sprite Norris
│   └── car_rival.png          # Sprite rivales
├── results/                   # Gráficas y datos generados
├── main.py                    # Script principal
├── requirements.txt
└── README.md
```

## Fundamentos Teóricos

### Algoritmo Q-Learning

Actualización de valores Q:

```
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

Donde:
- `α` (alpha) = 0.1: Tasa de aprendizaje
- `γ` (gamma) = 0.95: Factor de descuento
- `ε` (epsilon): 1.0 → 0.05: Exploración vs explotación

### Distribuciones de Probabilidad

El ambiente modela 9 distribuciones diferentes según estado × acción, capturando:
- **Trade-off velocidad-riesgo**: Estrategias agresivas tienen mayor probabilidad de victoria pero también de DNF
- **Impacto de posición inicial**: Desde pole es más fácil ganar que desde atrás
- **Realismo**: Basado en patrones observados en F1


## Autor

**Tania Julieth Araque Dueñas**
- GitHub: [@TaniaAraque](https://github.com/TaniaAraque)
- Proyecto: Introducción a Inteligencia Artificial

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.


- Inspirado en la temporada 2024 de Fórmula 1
- Implementado como proyecto educativo de Aprendizaje por Refuerzo
- Herramientas: Python, NumPy, Matplotlib, PyGame

---

⭐ Si este proyecto te resultó útil, considera darle una estrella!
