import time

from pypresence import Presence


class DiscordRPC:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.RPC = None
        self.connected = False

    def connect(self):
        self.RPC = Presence(self.client_id)
        self.RPC.connect()
        self.connected = True
        print("✅ Conectado ao Discord RPC")

    def update_presence(
        self,
        state: str = "Online",
        details: str = "Usando CLI",
        large_image: str = None,
    ):
        if not self.connected:
            raise Exception("Não conectado ao Discord RPC.")
        self.RPC.update(state=state, details=details, large_image=large_image)
        print(f"✅ Presença atualizada: {details} | {state}")

    def close(self):
        if self.RPC:
            self.RPC.close()
            self.connected = False
            print("❌ Desconectado do Discord RPC")
