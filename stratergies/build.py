import os
import sys
import subprocess
import importlib.util
import jpype
import ctypes

def compile_c(filename):
    output_filename = os.path.splitext(filename)[0] + '.dll' if os.name == 'nt' else os.path.splitext(filename)[0] + '.so'
    compile_command = ['gcc', '-shared', '-o', output_filename, filename]
    if os.name != 'nt':
        compile_command.insert(1, '-fPIC')
    try:
        subprocess.check_call(compile_command)
        return output_filename
    except subprocess.CalledProcessError:
        print(f"Error: Compilation of {filename} failed.")
        return None

def compile_java(filename):
    try:
        subprocess.check_call(['javac', filename])
        class_name = os.path.splitext(os.path.basename(filename))[0]
        return class_name + '.class'
    except subprocess.CalledProcessError:
        print(f"Error: Compilation of {filename} failed.")
        return None

def check_python(filename):
    module_name = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, filename)
    strategy_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(strategy_module)
    except Exception as e:
        print(f"Error: Execution of {filename} failed with error: {e}")
        return False

    if not hasattr(strategy_module, 'strategy'):
        print("Error: 'strategy' function not found in the Python file.")
        return False

    if not hasattr(strategy_module, 'initial_move'):
        print("Error: 'initial_move' variable not found in the Python file.")
        return False

    return True

def check_c(filename):
    lib = ctypes.CDLL(filename)
    if not hasattr(lib, 'strategy'):
        print("Error: 'strategy' function not found in the C library.")
        return False

    try:
        initial_move_ptr = ctypes.c_char_p.in_dll(lib, 'initial_move')
    except ValueError:
        print("Error: 'initial_move' variable not found in the C library.")
        return False

    return True

def check_java(classname):
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['.'])
    strategy_class = jpype.JClass(classname)
    if not hasattr(strategy_class, 'strategy'):
        print("Error: 'strategy' method not found in the Java class.")
        return False

    try:
        initial_move = strategy_class.initial_move
    except AttributeError:
        print("Error: 'initial_move' variable not found in the Java class.")
        return False

    return True

def main(filename):
    if not os.path.exists(filename):
        print(f"Error: File {filename} does not exist.")
        return

    file_extension = os.path.splitext(filename)[1]

    if file_extension == '.c':
        compiled_filename = compile_c(filename)
        if compiled_filename and check_c(compiled_filename):
            print(f"Success: {filename} compiled and verified successfully.")
    elif file_extension == '.java':
        compiled_filename = compile_java(filename)
        if compiled_filename and check_java(os.path.splitext(compiled_filename)[0]):
            print(f"Success: {filename} compiled and verified successfully.")
    elif file_extension == '.py':
        if check_python(filename):
            print(f"Success: {filename} verified successfully.")
    else:
        print(f"Error: Unsupported file type {file_extension}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build.py <filename>")
        sys.exit(1)

    main(sys.argv[1])
