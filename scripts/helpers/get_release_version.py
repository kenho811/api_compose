import os
from distutils.util import convert_path


parent_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def dump_release_version():
    main_ns = {}
    file_path = os.path.join(parent_folder_path, 'src', 'api_compose', 'version.py')
    print(file_path)
    path = convert_path(file_path)
    with open(path) as file:
        exec(file.read(), main_ns)
    return main_ns['__version__']
