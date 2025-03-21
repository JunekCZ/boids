import pygame
import pygame_gui
import random
import time
from boid import Boid
from quadtree import QuadTreeManager
from ui import UIManager
from config import NUM_BOIDS, WIDTH, HEIGHT, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR, SEPARATION_DISTANCE, VISION_RADIUS

cf = COHESION_FACTOR
af = ALIGNMENT_FACTOR
sf = SEPARATION_FACTOR
vr = VISION_RADIUS
sd = SEPARATION_DISTANCE

show_grid = False
use_quadtree = True

def draw_quadtree_grid(screen, qt_manager):
    if not show_grid:
        return

    grid_boxes = qt_manager.get_grid_boxes()
    for bbox in grid_boxes:
        x1, y1, x2, y2 = bbox
        pygame.draw.rect(screen, (255, 0, 0), (x1, y1, x2 - x1, y2 - y1), 1)

def get_all_neighbors(boid, boids, radius):
    return [other for other in boids
            if other != boid and boid.position.distance_to(other.position) <= radius]

pygame.init()

WINDOW_WIDTH = WIDTH + 200
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((WINDOW_WIDTH, HEIGHT))
ui_manager = UIManager(manager, use_quadtree)

boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

qt_manager = QuadTreeManager(WIDTH, HEIGHT)

running = True
while running:
    start_time = time.perf_counter()
    time_delta = clock.tick(60) / 1000.0
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (33, 33, 33), (WIDTH, 0, 200, HEIGHT))

    qt_manager.rebuild(boids)

    draw_quadtree_grid(screen, qt_manager)

    for i, boid in enumerate(boids):
        if use_quadtree:
            neighbors = qt_manager.get_neighbors(boid, radius=vr)
        else:
            neighbors = get_all_neighbors(boid, boids, radius=vr)

        boid.update(neighbors, cf, af, sf, sd)
        if i == 0:
            pygame.draw.circle(screen, (0, 0, 255), boid.position, vr, 1)
            pygame.draw.circle(screen, (255, 0, 0), boid.position, sd, 1)
        boid.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_grid = not show_grid
            elif event.key == pygame.K_q:
                use_quadtree = not use_quadtree
                ui_manager.update_mode_label(use_quadtree)

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
            elif key == "vision_radius":
                vr = value
            elif key == "separation_distance":
                sd = value

    manager.update(time_delta)
    manager.draw_ui(screen)

    end_time = time.perf_counter()
    elapsed_ms = (end_time - start_time) * 1000

    font = pygame.font.SysFont("Consolas", 16)
    text = font.render(f"{elapsed_ms:.2f} ms", True, (255, 200, 100))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()