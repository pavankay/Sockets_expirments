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
    client_id = id(websocket)

    try:
        print(f"New client connected: {websocket.remote_address}")
        clients.add(websocket)

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
        except websockets.exceptions.ConnectionClosed:
            print(f"Client {client_id} connection closed unexpectedly")
        except json.JSONDecodeError:
            print(f"Received invalid JSON from client {client_id}")
        except Exception as e:
            print(f"Error handling message from client {client_id}: {e}")

    finally:
        # This block will execute when the client disconnects, either normally or due to an error
        print(f"Client {client_id} disconnected")
        clients.discard(websocket)  # Using discard instead of remove to avoid KeyError
        if client_id in positions:
            client_color = positions[client_id]["color"]
            available_colors.append(client_color)
            del positions[client_id]
            print(f"Freed up color: {client_color}")

        # Broadcast updated positions to remaining clients
        if clients:  # Only broadcast if there are still connected clients
            await broadcast(json.dumps({"positions": positions}))
            print("Broadcasted updated positions after client disconnection")


async def broadcast(message):
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            disconnected_clients.add(client)
        except Exception as e:
            print(f"Error broadcasting to a client: {e}")
            disconnected_clients.add(client)

    # Remove disconnected clients
    for client in disconnected_clients:
        clients.discard(client)

    print(f"Broadcasted message to {len(clients)} clients: {message}")


async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())