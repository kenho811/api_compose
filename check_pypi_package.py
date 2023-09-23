import json
import sys
from enum import Enum

import requests


class OutputEnum(Enum):
    Exists: str = 'exists'
    NotExists: str = 'not_exists'


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


def write_output(file_path: str, output: OutputEnum):
    print(f'writing {output} to file {file_path}')
    with open(file_path, 'w') as f:
        f.write(output.value)


if __name__ == '__main__':
    from setup import package_name, get_version
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        raise ValueError('Usage: python check_pypi_package.py {output_file_path}')

    base_url = "https://pypi.org/pypi"
    version = get_version()

    if is_package_exist(base_url, package_name, version):
        print(f'Package {package_name=} with version {version=} already exists on {base_url=}')
        output = OutputEnum.Exists
    else:
        print(f"Package {package_name=} with version {version=} does not exist on {base_url=}")
        output = OutputEnum.NotExists

    write_output(file_path, output=output)
