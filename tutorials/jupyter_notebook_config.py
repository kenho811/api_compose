# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'api-server-one': {
        'command': ['acp', 'examples', 'api_server_one', '{port}'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '$HOME/.jupyter/api_server_one.svg',
            'title': 'ApiServerOne',
        },
    },
}