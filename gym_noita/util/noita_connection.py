import asyncio
import websockets
import json
import os

noita_ws_token_file = "D:\\SteamLibrary\\steamapps\\common\\Noita\\mods\\cheatgui\\token.json"
file_not_found = "FileNotFound!"

radar_string = ''.join(open("C:\\Users\\poiso\\projects\\gym-noita\\gym_noita\\util\\radar.lua").readlines())


class NoitaConnection():

    def __init__(self) -> None:
        self.connected = False
        self.token = self.get_token()

    def get_token(self):
        if os.path.exists(noita_ws_token_file):
            token_file = open(noita_ws_token_file)
            data = json.load(token_file)
            token_file.close()
            return data["token"]
        else:
            return file_not_found
    
    async def start(self):
        uri = "ws://localhost:9777"

        if self.token != file_not_found:
            async with websockets.connect(uri) as connection:

                connection_string = f'AUTH "{self.token}"';
                await connection.send(connection_string)
                self.connected = True

                try:
                    while self.connected:
                        await connection.send(radar_string)
                        data = await connection.recv()
                        print(f"<<< {data}")
                except:
                    self.connected = False
                    await connection.close()

                if os.path.exists(noita_ws_token_file):
                    os.remove(noita_ws_token_file)
        else:
            print(f"Failed to get token from {noita_ws_token_file}\nExiting...")

test = NoitaConnection()
print(test.token)

asyncio.run(test.start())

