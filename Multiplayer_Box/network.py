import asyncio
import websockets
import json

class Network:
    def __init__(self, uri="ws://localhost:8765"):
        self.uri = uri
        self.websocket = None
        self.connected = False
        self.color = None
        self.on_position_update = None
        self.on_connection = None
        self.positions = {}  # Add this line to initialize positions

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            print("Connected to WebSocket server")

            # Receive initial color information
            initial_data = await self.websocket.recv()
            initial_data = json.loads(initial_data)
            if "your_color" in initial_data:
                self.color = initial_data["your_color"]
                print(f"Your assigned color is: {self.color}")

            if self.on_connection:
                self.on_connection(self.color)

            asyncio.create_task(self.receive_loop())
        except Exception as e:
            print(f"Connection failed: {e}")

    async def receive_loop(self):
        while self.connected:
            try:
                response = await self.websocket.recv()
                data = json.loads(response)
                print(f"Received data: {data}")  # Debug print
                if "positions" in data:
                    self.positions = data["positions"]
                    if self.on_position_update:
                        self.on_position_update(self.positions)
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                self.connected = False
                break
            except Exception as e:
                print(f"Error in receive loop: {e}")

    async def send_move(self, move):
        if self.connected:
            await self.websocket.send(json.dumps({"move": move}))

    async def disconnect(self):
        if self.connected:
            await self.websocket.close()
            self.connected = False
            print("Disconnected from WebSocket server")