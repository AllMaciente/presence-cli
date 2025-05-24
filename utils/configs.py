import json
import os
import subprocess

import typer
from rich import print

CONFIG_PATH = os.path.expanduser("~/.config/presence-cli/config.json")
ALLOWED_KEYS = {
    "clientId": "the client id of discord application",
}
config_app = typer.Typer()


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {key: None for key in ALLOWED_KEYS}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_config(key: str):
    """
    Obtém o valor de uma configuração permitida.
    """
    config = load_config()
    if key not in ALLOWED_KEYS:
        print(
            f"Erro: A chave '{key}' não é permitida. Chaves permitidas: {', '.join(ALLOWED_KEYS)}"
        )
        raise typer.Exit(code=1)
    return config.get(key, None)


def save_config(config):
    os.makedirs(
        os.path.dirname(CONFIG_PATH), exist_ok=True
    )  # Garante que o diretório exista
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


@config_app.command("set")
def set_config(key: str, value: str):
    """
    Define uma configuração permitida.
    """
    if key not in ALLOWED_KEYS:
        print(
            f"Erro: A chave '{key}' não é permitida. Chaves permitidas: {', '.join(ALLOWED_KEYS)}"
        )
        raise typer.Exit(code=1)

    config = load_config()
    config[key] = value
    save_config(config)
    print(f"Configuração '{key}' atualizada para '{value}'.")


@config_app.command("show")
def show_config():
    """
    Mostra todas as configurações atuais.
    """
    config = load_config()
    for key, desc in ALLOWED_KEYS.items():
        value = config.get(key, None)
        print(f"{key}: {value}  # {desc}")


@config_app.command("edit")
def edit_config():
    """
    Edita manualmente o arquivo de configuração, com aviso.
    """
    editor = os.getenv("EDITOR", "nano")
    if not os.path.exists(CONFIG_PATH):
        save_config({key: None for key in ALLOWED_KEYS})
    subprocess.call([editor, CONFIG_PATH])
