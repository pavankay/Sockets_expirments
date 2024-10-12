import asyncio
import websockets
import json
import random

clients = set()
positions = {}
colors = ["green", "blue", "red", "yellow", "purple", "orange", "pink", "cyan"]
available_colors = colors.copy()

async def handle_client(websocket, path):
    global available_colors
    print(f"New client connected: {websocket.remote_address}")
    clients.add(websocket)
    client_id = id(websocket)

    if not available_colors:
        available_colors = colors.copy()
    client_color = random.choice(available_colors)
    available_colors.remove(client_color)

    positions[client_id] = {"x": random.randint(0, 750), "y": random.randint(0, 550), "color": client_color}
    print(f"Assigned color to client {client_id}: {positions[client_id]['color']}")

    # Send initial color information to the client
    await websocket.send(json.dumps({"your_color": client_color}))

    try:
        async for message in websocket:
            print(f"Received message from client {client_id}: {message}")
            data = json.loads(message)
            if "move" in data:
                positions[client_id]["x"] += data["move"]["x"]
                positions[client_id]["y"] += data["move"]["y"]
                print(f"Updated position for client {client_id}: {positions[client_id]}")

            await broadcast(json.dumps({"positions": positions}))
            print("Broadcasted updated positions to all clients")
    finally:
        print(f"Client {client_id} disconnected")
        clients.remove(websocket)
        client_color = positions[client_id]["color"]
        available_colors.append(client_color)
        del positions[client_id]
        print(f"Freed up color: {client_color}")

async def broadcast(message):
    print(f"Broadcasting message to {len(clients)} clients: {message}")
    for client in clients:
        await client.send(message)

print("Setting up WebSocket server on localhost:8765")
start_server = websockets.serve(handle_client, "localhost", 8765)

print("Starting the event loop")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()