# Iterated Prisoner's Dilemma

## Overview

This project simulates the **Iterated Prisoner's Dilemma** game to analyze the performance of various strategies. It allows participants to implement strategies in **Python**, **Java**, and **C**, enabling cross-language strategy development. The project supports flexible integration using **Jype** (for Java) and **ctypes** (for C), and features a **round-robin tournament** or **one-on-one** match setup to evaluate different strategies.

## Key Features

- **Cross-language compatibility**: Supports strategy implementation in **Java**, **C**, and **Python**.
- **Strategy Functions**: Each strategy must define an `initial_move` and `strategy` function.
- **Flexible Integration**: Use of **Jype** for Java integration and **ctypes** for C integration.
- **Round-robin Tournament**: Compete multiple strategies against each other in a tournament.
- **One-on-One Matches**: Select and play one-on-one matches between two chosen strategies.

## Setup Instructions

### Prerequisites

- **Python** (>= 3.x)
- **Java** (>= 8) with **Jype** installed for Java integration.
- **C compiler** (gcc, clang, etc.) with **ctypes** support for C integration.

### Install Dependencies

1. **Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Java setup**:
   - Install **Jype** to integrate Java with Python.

3. **C setup**:
   - Ensure **ctypes** is installed (it’s part of the Python standard library).

### Clone the Repository

```bash
git clone https://github.com/yourusername/Iterated-Prisoners-Dilemma.git
cd Iterated-Prisoners-Dilemma
```

## Project Structure

- `master.py`: Main logic for running the game, integrating different strategies.
- `strategies/`: Folder containing different strategy files in Python, Java, and C.
- `README.md`: This file, providing an overview and usage instructions.

## Strategy Functions

Each strategy should implement two functions:

1. **`initial_move()`**: Returns the strategy’s first move ('C' or 'D').
2. **`strategy(opponent_move)`**: Defines the strategy logic, where it takes the opponent's last move and returns the current move ('C' or 'D').

### Example Strategy in Python

```python
# File: strategies/example.py
initial_move = "d"

def strategy(opponent_move):
    return opponent_move  # Mimic opponent's move
```

### Example Strategy in Java

```java
// File: strategies/JavaStrategy.class
public class JavaStrategy {
    public static String initial_move = "d";

    public static String strategy(String opponent_move) {
        return opponent_move;  // Mimic opponent's move
    }
}
```

### Example Strategy in C

```c
// File: strategies/CStrategy.so
#include <string.h>

char* initial_move = "d";

char* strategy(char* opponent_move) {
    return opponent_move;  // Mimic opponent's move
}
```

## Gameplay

The game proceeds as follows:

- Players submit their strategies as files in Python, Java, or C.
- The strategies are loaded dynamically based on their file type (Java: `.class`, C: `.so`, Python: `.py`).
- A round-robin tournament or one-on-one match can be started to evaluate the strategies.

### Running the Tournament

```bash
python master.py
```

1. The program will list all available strategy files.
2. Choose to run a **round-robin tournament** or a **one-on-one match**.
3. The game will play out for 10 rounds between each pair of strategies, calculating the final scores.

### Example One-on-One Match

- Choose two strategies from the list.
- The game will run 10 rounds and output the scores for each strategy.

## Contributing

We encourage contributions to improve and extend the project. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Implement your feature or fix a bug.
4. Push your changes and create a pull request.

