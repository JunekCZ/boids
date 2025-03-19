import pygame
import pygame_gui
import random
from boid import Boid
from quadtree import QuadTreeManager
from ui import UIManager
from config import NUM_BOIDS, WIDTH, HEIGHT, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR

cf = COHESION_FACTOR
af = ALIGNMENT_FACTOR
sf = SEPARATION_FACTOR

def draw_quadtree_grid(screen, qt_manager):
    """ Vykreslí mřížku QuadTree """
    grid_boxes = qt_manager.get_grid_boxes()
    for bbox in grid_boxes:
        x1, y1, x2, y2 = bbox
        pygame.draw.rect(screen, (255, 0, 0), (x1, y1, x2 - x1, y2 - y1), 1)  # Červené linky

pygame.init()

# Rozšíříme okno pro UI
WINDOW_WIDTH = WIDTH + 200
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Inicializace UI
manager = pygame_gui.UIManager((WINDOW_WIDTH, HEIGHT))
ui_manager = UIManager(manager)

# Vytvoření boidů
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

# Inicializace QuadTree
qt_manager = QuadTreeManager(WIDTH, HEIGHT)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((0, 0, 0))  

    # Aktualizace QuadTree
    qt_manager.rebuild(boids)

    # Vykreslení mřížky QuadTree
    draw_quadtree_grid(screen, qt_manager)

    # Aktualizace boidů
    for boid in boids:
        neighbors = qt_manager.get_neighbors(boid, radius=50)
        boid.update(neighbors, cf, af, sf)
        boid.draw(screen)

    # UI aktualizace
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)
        result = ui_manager.handle_events(event)
        if result:
            key, value = result
            if key == "cohesion":
                cf = value
            elif key == "alignment":
                af = value
            elif key == "separation":
                sf = value

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()