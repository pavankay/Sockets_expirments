import pygame
import asyncio
import websockets
import json

print("Initializing Pygame and setting up the game window")
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WebSocket Game")
font = pygame.font.Font(None, 36)

async def game_loop():
    print("Connecting to WebSocket server")
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")
        clock = pygame.time.Clock()
        running = True
        frame_count = 0
        your_color = None

        # Receive initial color information
        initial_data = await websocket.recv()
        initial_data = json.loads(initial_data)
        if "your_color" in initial_data:
            your_color = initial_data["your_color"]
            print(f"Your assigned color is: {your_color}")

        while running:
            frame_count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            move = {"x": 0, "y": 0}
            if keys[pygame.K_LEFT]:
                move["x"] -= 5
            if keys[pygame.K_RIGHT]:
                move["x"] += 5
            if keys[pygame.K_UP]:
                move["y"] -= 5
            if keys[pygame.K_DOWN]:
                move["y"] += 5

            if move["x"] != 0 or move["y"] != 0:
                print(f"Sending move: {move}")
                await websocket.send(json.dumps({"move": move}))

            try:
                print("Waiting for server response")
                response = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                print(f"Received response: {response}")
                data = json.loads(response)
                positions = data["positions"]

                screen.fill((255, 255, 255))
                for client_id, pos in positions.items():
                    color = pygame.Color(pos["color"])
                    pygame.draw.rect(screen, color, (pos["x"], pos["y"], 50, 50))

                # Render text
                if your_color:
                    text = f"You are: {your_color}"
                    text_surface = font.render(text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect()
                    text_rect.topright = (WIDTH - 10, 10)
                    screen.blit(text_surface, text_rect)

                pygame.display.flip()
                print("Updated screen with new positions")
            except asyncio.TimeoutError:
                print("No response from server (timeout)")
                pass

            clock.tick(60)

        pygame.quit()

print("Starting the game loop")
asyncio.get_event_loop().run_until_complete(game_loop())