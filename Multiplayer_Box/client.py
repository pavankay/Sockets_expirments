import pygame
import asyncio
from network import Network

print("Initializing Pygame and setting up the game window")
pygame.init()

WIDTH, HEIGHT = 800, 600
BORDER_WIDTH = 5
PLAYER_SIZE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WebSocket Game")
font = pygame.font.Font(None, 36)

network = Network()

def draw_game_state(positions):
    screen.fill((255, 255, 255))  # Fill screen with white
    print(f"Drawing positions: {positions}")

    # Draw border
    border_color = (0, 0, 0)  # Black color for the border
    pygame.draw.rect(screen, border_color, (0, 0, WIDTH, HEIGHT), BORDER_WIDTH)

    # Calculate the playable area
    play_area = pygame.Rect(BORDER_WIDTH, BORDER_WIDTH,
                            WIDTH - 2*BORDER_WIDTH, HEIGHT - 2*BORDER_WIDTH)

    for client_id, pos in positions.items():
        color = pygame.Color(pos["color"])
        # Adjust rectangle position to be within the border
        rect = pygame.Rect(pos["x"] + BORDER_WIDTH, pos["y"] + BORDER_WIDTH, PLAYER_SIZE, PLAYER_SIZE)
        # Ensure the rectangle stays within the play area
        rect.clamp_ip(play_area)
        pygame.draw.rect(screen, color, rect)
        print(f"Drew rectangle at {rect.x}, {rect.y} with color {color}")

    if network.color:
        text = f"You are: {network.color}"
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topright = (WIDTH - BORDER_WIDTH - 10, BORDER_WIDTH + 10)
        screen.blit(text_surface, text_rect)
        print(f"Drew text: {text}")

    pygame.display.flip()
    print("Screen updated")

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