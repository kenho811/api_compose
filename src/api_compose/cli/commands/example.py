"""
config subcommand
"""

import typer


app = typer.Typer(
    help="Example Servers",
    no_args_is_help=True
)



@app.command(help="Initialise Configuration File")
def api_server_one(port: str) -> None:
    """
    Run api_server_one on a given port

    :return:
    """
    from api_compose.cli.commands.examples.api_server_one.app import app
    app.run(port=port)

