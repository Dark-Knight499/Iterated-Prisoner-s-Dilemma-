import sys
import jpype
import ctypes
import importlib.util
import os

score1 = 0
score2 = 0

# Load and execute Java strategy
def load_java(filename):
    classpath = os.path.dirname(filename)
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=[classpath])
    class_name = os.path.basename(filename).replace('.class', '')
    strategy_class = jpype.JClass(class_name)
    initial_move = str(strategy_class.initial_move)
    def strategy_java(opponents_move): 
        opponents_move = jpype.JClass('java.lang.String')(opponents_move)
        return str(strategy_class.strategy(opponents_move))
    return initial_move, strategy_java

# Load and execute Python strategy
def load_python(filename):
    module_name = os.path.basename(filename).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, filename)
    strategy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strategy_module)
    initial_move = strategy_module.initial_move
    def strategy_py(opponents_move):
        return strategy_module.strategy(opponents_move)
    return initial_move, strategy_py

# Load and execute C/C++ strategy
def load_c(filename):
    lib = ctypes.CDLL(filename)
    lib.strategy.restype = ctypes.c_char_p
    initial_move_ptr = ctypes.c_char_p.in_dll(lib, "initial_move")
    initial_move = initial_move_ptr.value.decode('utf-8')
    def strategy_c(opponents_move):
        move = lib.strategy(opponents_move.encode('utf-8'))
        return move.decode('utf-8')
    return initial_move, strategy_c

# Determine which strategy to load based on file extension
def load_strategy(filename):
    if filename.endswith('.class'):
        return load_java(filename)
    elif filename.endswith('.py'):
        return load_python(filename)
    elif filename.endswith('.so') or filename.endswith('.dll'):
        return load_c(filename)
    else:
        raise ValueError("Unsupported file type")

# Calculate scores based on moves
def calculate(move1, move2):
    global score1, score2
    if move1 == "c" and move2 == "d":
        score2 += 5
    elif move1 == "d" and move2 == "c":
        score1 += 5
    elif move1 == "c" and move2 == "c":
        score1 += 3
        score2 += 3
    elif move1 == "d" and move2 == "d":
        score1 += 1
        score2 += 1

# Main gameplay loop
def gameplay(rounds, filename1, filename2):
    initial_move1, strategy1 = load_strategy(filename1)
    initial_move2, strategy2 = load_strategy(filename2)
    
    move1 = initial_move1
    move2 = initial_move2
    
    while rounds > 0:
        calculate(move1, move2)
        move1 = strategy1(move2)
        move2 = strategy2(move1)
        rounds -= 1
    
    print("Final Scores:")
    print(f"Strategy 1: {score1}")
    print(f"Strategy 2: {score2}")

import os

def start_tournament():
    strategy_folder = "./stratergies"
    if not os.path.exists(strategy_folder):
        print("Strategy folder not found.")
        return
    
    strategies = []

    # Include Python strategies from the main folder
    strategies.extend([os.path.join(strategy_folder, f) for f in os.listdir(strategy_folder) if f.endswith('.py') and f != "build.py"])

    # Include Java and C/C++ strategies from their respective subfolders
    for subfolder in ['.class', '.exe']:
        subfolder_path = os.path.join(strategy_folder, subfolder)
        if os.path.exists(subfolder_path):
            strategies.extend([os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if f.endswith(('.class', '.so', '.dll'))])
    
    if not strategies:
        print("No valid strategy files found.")
        return
    
    # Round-robin tournament
    for i in range(len(strategies)):
        for j in range(i + 1, len(strategies)):
            global score1, score2
            score1 = 0
            score2 = 0
            print(f"Match between {os.path.basename(strategies[i])} and {os.path.basename(strategies[j])}")
            gameplay(10, strategies[i], strategies[j])

def one_on_one():
    strategy_folder = "./stratergies"
    if not os.path.exists(strategy_folder):
        print("Strategy folder not found.")
        return
    
    strategy_files = []

    # Include Python strategies from the main folder
    strategy_files.extend([os.path.join(strategy_folder, f) for f in os.listdir(strategy_folder) if f.endswith('.py') and f != "build.py"])

    # Include Java and C/C++ strategies from their respective subfolders
    for subfolder in ['.class', '.exe']:
        subfolder_path = os.path.join(strategy_folder, subfolder)
        if os.path.exists(subfolder_path):
            strategy_files.extend([os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if f.endswith(('.class', '.so', '.dll'))])
    
    if not strategy_files:
        print("No valid strategy files found.")
        return
    
    print("Available strategies:")
    for idx, file in enumerate(strategy_files):
        print(f"{idx + 1}. {os.path.basename(file)}")
    
    try:
        choice1 = int(input("Choose the first strategy: ")) - 1
        choice2 = int(input("Choose the second strategy: ")) - 1
    except ValueError:
        print("Invalid input. Exiting...")
        return
    
    if choice1 < 0 or choice1 >= len(strategy_files) or choice2 < 0 or choice2 >= len(strategy_files):
        print("Invalid choices. Exiting...")
        return
    
    strategy1 = strategy_files[choice1]
    strategy2 = strategy_files[choice2]
    
    gameplay(10, strategy1, strategy2)

# Example usage in the start function
def start():
    print("Welcome to the Prisoner's Dilemma Game!")
    print("1. Start Tournament")
    print("2. One-on-One Match")
    try:
        choice = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input. Exiting...")
        return
    
    if choice == 1:
        start_tournament()
    elif choice == 2:
        one_on_one()
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    start()
