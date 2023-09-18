import json

import requests


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
    from setup import package_name, get_version

    base_url = "https://pypi.org/pypi"
    version = get_version()

    if is_package_exist(base_url, package_name, version):
        raise ValueError(f'Package {package_name=} with version {version=} already exists on {base_url=}')
    else:
        print(f"Package {package_name=} with version {version=} does not exist on {base_url=}")
        exit(0)
