import os

def get_abs_path(script_path, file_name):
    current_directory = os.path.dirname(os.path.abspath(script_path))
    return current_directory + os.sep + file_name