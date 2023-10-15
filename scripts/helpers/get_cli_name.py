import os
from distutils.util import convert_path

# Get the parent folder path using os.path.dirname()
parent_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def get_cli_name():
    main_ns = {}
    file_path = os.path.join(parent_folder_path, 'src', 'api_compose', 'app.py')
    path = convert_path(file_path)
    with open(path) as file:
        exec(file.read(), main_ns)
    return main_ns['__app__']
