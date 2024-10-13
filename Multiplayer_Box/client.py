import pygame
import asyncio
from network import Network

print("Initializing Pygame and setting up the game window")
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WebSocket Game")
font = pygame.font.Font(None, 36)

network = Network()

def draw_game_state(positions):
    screen.fill((255, 255, 255))  # Fill screen with white
    print(f"Drawing positions: {positions}")  # Debug print
    for client_id, pos in positions.items():
        color = pygame.Color(pos["color"])
        pygame.draw.rect(screen, color, (pos["x"], pos["y"], 50, 50))
        print(f"Drew rectangle at {pos['x']}, {pos['y']} with color {color}")  # Debug print

    if network.color:
        text = f"You are: {network.color}"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topright = (WIDTH - 10, 10)
        screen.blit(text_surface, text_rect)
        print(f"Drew text: {text}")  # Debug print

    pygame.display.flip()
    print("Screen updated")  # Debug print

async def game_loop():
    print("Connecting to WebSocket server")
    await network.connect()

    def on_position_update(positions):
        draw_game_state(positions)

    network.on_position_update = on_position_update

    clock = pygame.time.Clock()
    running = True

    # Initial draw
    if network.positions:
        draw_game_state(network.positions)

    while running:
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
            await network.send_move(move)

        # Redraw the game state every frame
        if network.positions:
            draw_game_state(network.positions)

        await asyncio.sleep(0.01)  # Short sleep to allow other tasks to run
        clock.tick(60)

    await network.disconnect()
    pygame.quit()

print("Starting the game loop")
asyncio.get_event_loop().run_until_complete(game_loop())