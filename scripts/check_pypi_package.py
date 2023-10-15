import json
import sys

import requests

from helpers.const import package_name
from helpers.get_release_version import dump_release_version
from helpers.write import write_exists_in_kv_format


def is_package_exist(
        base_url: str,
        package_name: str,
        package_version: str,
) -> bool:
    url = f"{base_url}/{package_name}/{package_version}/json"
    print(f"querying {url=}")

    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        if package_data.get("info"):
            print(json.dumps(package_data, indent=4))
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        raise ValueError('Usage: python check_pypi_package.py {output_file_path}')

    base_url = "https://pypi.org/pypi"
    version = dump_release_version()

    if is_package_exist(base_url, package_name, version):
        print(f'Package {package_name=} with version {version=} already exists on {base_url=}')
        exists = True
    else:
        print(f"Package {package_name=} with version {version=} does not exist on {base_url=}")
        exists = False

    write_exists_in_kv_format(
        file_path,
        # key value pairs
        exists=exists,
        version=version
    )
