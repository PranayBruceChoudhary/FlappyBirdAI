# 🐤 Flappy Bird AI Baseline

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

A lightweight, zero-boilerplate Pygame implementation of **Flappy Bird** built specifically for Reinforcement Learning (RL) and Artificial Intelligence experiments using **PyTorch**.

---

## 📌 Overview

This repository provides a minimal, high-performance environment baseline for training autonomous agents to play Flappy Bird. Instead of relying on raw pixel processing (CNNs), the environment pre-calculates real-time spatial vectors $(dx, dy)$ relative to pipe gap centers. This makes it ideal for training fast feature-based models like **Deep Q-Networks (DQN)**, **PPO**, **Q-Learning**, and **NEAT**.

---

## ✨ Features

- ⚡ **Lightweight & Fast**: Built with minimal Pygame rendering overhead (~100 lines of Python).
- 🧮 **Pre-Engineered State Vectors**: Computes relative horizontal and vertical distances ($dx, dy$) in real time.
- 🎯 **Discrete Action Space**: Binary action model ($0 = \text{fall}$, $1 = \text{jump}$).
- 🚀 **PyTorch Ready**: Pre-configured structure ready for direct integration with PyTorch neural networks.
- 🔄 **Auto-Reset Physics**: Integrated collision detection with immediate episode resets for continuous agent iteration.

---

## 🎮 Game Physics & State Space

### State Representation (Observations)
The environment extracts a 2D continuous vector representing the bird's relative position to the next obstacle:

| Variable | Description | Range (approx) |
| :--- | :--- | :--- |
| `dx` | Horizontal distance from bird to approaching pipe (`pipe_x - bird_x`) | `[-60, 400]` px |
| `dy` | Vertical distance from bird center to pipe gap center (`bird_y - pipe_gap_y`) | `[-300, 300]` px |

$$\text{State Vector } S_t = \begin{bmatrix} dx \\ dy \end{bmatrix}$$

### Action Space
- **`0`**: Do nothing (gravity accelerates bird downwards at $g = 1.2 \, \text{px/frame}^2$).
- **`1`**: Flap / Jump (instantly applies velocity $v = -12.0 \, \text{px/frame}$).

---

## ⚡ Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed along with Pygame and PyTorch:

```bash
pip install pygame torch
```

### 2. Run Human Control Mode
To launch the baseline game and test manual controls (`SPACE` key to jump):

```bash
python flappy.py
```

Console output will display the live $(dx, dy)$ mathematical state vector fed to the AI:
```text
dx: 240.0 | dy: -12.5 | Action: 0
dx: 235.0 | dy: -11.3 | Action: 1
```

---

## 🔍 Code Review & Architecture

The primary script [`flappy.py`](file:///c:/Users/mannu/FlappyBirdAI/flappy.py) is organized into 5 concise stages:

1. **Setup & Physics Config** (`L6-L33`): Sets window dimensions ($400 \times 600$), gravity ($1.2$), jump velocity ($-12.0$), pipe gap ($150\text{px}$), and pipe speed ($-5.0$).
2. **Event & Input Handling** (`L39-L48`): Captures Pygame keyboard events (`K_SPACE`).
3. **Physics Engine** (`L49-L61`): Updates bird vertical velocity and moves pipes leftward. Spawns new pipe gap centers randomly when offscreen.
4. **State Feature Calculation** (`L62-L70`): Calculates $dx$ and $dy$ inputs for reinforcement learning inference.
5. **Collision Detection & Rendering** (`L71-L103`): Detects boundary/pipe intersection, flashes red screen on collision, and draws updated graphics at 30 FPS.

### 💡 Recommendations for AI Extensions
- **Gym Environment Wrapper**: Refactor `flappy.py` into a standard `Gym.Env` or `Gymnasium` class with `.step(action)` returning `(observation, reward, terminated, truncated, info)`.
- **Headless Training Mode**: Add a toggle to disable `pygame.display.flip()` and `clock.tick(30)` to accelerate training speed to thousands of frames per second.
- **Reward Function Engineering**:
  - Survival reward: $+0.1$ per frame survived.
  - Pipe clearance reward: $+1.0$ for passing a pipe gap.
  - Death penalty: $-1.0$ on collision.

---

## 🤖 Next Steps: PyTorch AI Integration Example

Here is a minimal PyTorch Deep Q-Network (DQN) policy template designed to interface directly with this state vector:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FlappyDQN(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=64, output_dim=2):
        super(FlappyDQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x is tensor of shape [batch_size, 2] -> (dx, dy)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x) # Q-values for [Action 0 (fall), Action 1 (jump)]

# Example inference
model = FlappyDQN()
sample_state = torch.tensor([[150.0, -20.0]], dtype=torch.float32)
q_values = model(sample_state)
action = torch.argmax(q_values).item()
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check out the [issues page](../../issues).

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
