import typer

from utils import configs

app = typer.Typer()

app.add_typer(configs.config_app, name="config")


@app.command()
def hello(name: str):
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
