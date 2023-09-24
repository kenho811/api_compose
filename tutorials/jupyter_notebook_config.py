# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'api-server-one': {
        'command': ['openrefine/openrefine-2.8/refine', '-p', '{port}','-d','/home/jovyan/openrefine'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '$HOME/.jupyter/api_server_one.svg',
            'title': 'OpenRefine',
        },
    },
}