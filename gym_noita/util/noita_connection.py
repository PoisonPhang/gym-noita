import asyncio
import websockets
import json
import os

noita_ws_token_file = "D:\\SteamLibrary\\steamapps\\common\\Noita\\mods\\cheatgui\\token.json"
file_not_found = "FileNotFound!"

radar_string = ''.join(open("C:\\Users\\poiso\\projects\\gym-noita\\gym_noita\\util\\radar.lua").readlines())

debug = True


class NoitaConnection():

    def __init__(self) -> None:
        self.connected = False
        self.token = self.get_token()
        self.state = {}
        self.is_dead = False

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
            print("Connecting with token: ", self.token)
            async with websockets.connect(uri) as connection:

                connection_string = f'AUTH "{self.token}"';
                await connection.send(connection_string)
                self.connected = True

                data = ""
                not_state_data = True

                try:
                    while not_state_data:
                        await connection.send(radar_string)
                        data = await connection.recv()
                        data = data.split('> ')[1]
                    
                        if "player is dead" in data:
                            self.is_dead = True
                            print("Player died. Reset necessary")

                        if (data[0] == '{'):
                            self.state = json.loads(data)
                            not_state_data = False
                        elif "[no value]" not in data:
                            print("Non-State Message: ", data)


                except websockets.exceptions.ConnectionClosedError:
                    print("Connection closed by game. Exiting...")
                    self.connected = False
                except json.decoder.JSONDecodeError:
                    print('Error parsing JSON: ', data)

            await connection.close()
            self.connected = False

            return self.state
        else:
            print(f"Failed to get token from {noita_ws_token_file}\nExiting...")

    def __del__(self):
        if os.path.exists(noita_ws_token_file):
                    os.remove(noita_ws_token_file)
# test = NoitaConnection()
# print(test.token)

# asyncio.run(test.start())

