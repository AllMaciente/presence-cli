import re
import time

import typer

from utils import configs
from utils.rich_presence import DiscordRPC

app = typer.Typer()

app.add_typer(configs.config_app, name="config")


@app.command()
def hello(name: str):
    typer.echo(f"Hello, {name}!")


@app.command()
def start(
    state: str = "Online",
    details: str = "Usando CLI",
    image: str = "default",
    duration: int = 0,
):
    """
    Inicia o Discord Rich Presence.
    """
    rpc_instance = DiscordRPC(configs.get_config("clientId"))
    rpc_instance.connect()
    rpc_instance.update_presence(state=state, details=details, large_image=image)

    print(
        f"⏳ Mantendo a presença ativa por {'tempo indeterminado' if duration == 0 else f'{duration} segundos'}..."
    )
    print("Pressione Ctrl+C para interromper.")
    try:
        if duration == 0:
            while True:
                time.sleep(1)
        else:
            time.sleep(duration)
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário.")

    rpc_instance.close()


def to_snake_case(text: str) -> str:
    """
    Converte um texto para snake_case.
    Exemplo: 'Stardew Valley' -> 'stardew_valley'
    """
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)  # Remove caracteres especiais
    text = re.sub(r"\s+", "_", text)  # Substitui espaços por _
    return text


@app.command()
def game(
    name: str,
    state: str = "Online",
    default: bool = False,
    duration: int = 0,
):
    rpc_instance = DiscordRPC(configs.get_config("clientId"))
    rpc_instance.connect()
    if default:
        rpc_instance.update_presence(state=state, details=name, large_image="default")
    else:
        rpc_instance.update_presence(
            state=state, details=name, large_image=to_snake_case(name)
        )
    print(
        f"⏳ Mantendo a presença ativa por {'tempo indeterminado' if duration == 0 else f'{duration} segundos'}..."
    )
    print("Pressione Ctrl+C para interromper.")
    try:
        if duration == 0:
            while True:
                time.sleep(1)
        else:
            time.sleep(duration)
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário.")

    rpc_instance.close()


if __name__ == "__main__":
    app()
