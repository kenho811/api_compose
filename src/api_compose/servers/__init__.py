def setup_api_server_one():
    """Entrypoint for Jupyter server proxy"""
    return {
        'command': ['python', '-m', 'api_compose.servers.api_server_one.app', '{port}'],
        'port': 8080,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '$HOME/.jupyter/api_server_one.svg',
            'title': 'ApiServerOne',
        },
    }
