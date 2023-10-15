import os
import sys

from helpers.write import write_exists_in_kv_format
from helpers.get_release_version import dump_release_version

parent_folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        output_file_path = sys.argv[1]
    else:
        raise ValueError('Usage: python dump_release_version.py {output_file_path}')

    write_exists_in_kv_format(
        output_file_path,
        # key value pairs
        version=dump_release_version(),
    )
