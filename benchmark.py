import time
import random
import csv
from boid import Boid
from quadtree import QuadTreeManager
from config import WIDTH, HEIGHT, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR, VISION_RADIUS

def get_all_neighbors(boid, boids, radius):
    return [other for other in boids if other != boid and boid.position.distance_to(other.position) <= radius]

def measure_simulation(num_boids, use_quadtree, steps=100):
    from pygame import Vector2  # Musí být importováno až uvnitř, protože jinak je potřeba inicializace pygame

    boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_boids)]
    qt_manager = QuadTreeManager(WIDTH, HEIGHT)

    times = []

    for _ in range(steps):
        start = time.perf_counter()

        if use_quadtree:
            qt_manager.rebuild(boids)

        for boid in boids:
            if use_quadtree:
                neighbors = qt_manager.get_neighbors(boid, radius=VISION_RADIUS)
            else:
                neighbors = get_all_neighbors(boid, boids, radius=VISION_RADIUS)

            boid.update(neighbors, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR, 15)

        end = time.perf_counter()
        times.append((end - start) * 1000)  # ms

    return sum(times) / len(times)

def run_benchmarks():
    results = []

    for n in [50, 100, 200, 500, 1000, 2000]:
        print(f"Testing {n} boids...")
        bf_time = measure_simulation(n, use_quadtree=False)
        qt_time = measure_simulation(n, use_quadtree=True)

        results.append((n, bf_time, qt_time))
        print(f"{n} boids → BF: {bf_time:.2f} ms | QT: {qt_time:.2f} ms")

    with open("benchmark_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_boids", "brute_force_ms", "quadtree_ms"])
        writer.writerows(results)

if __name__ == "__main__":
    run_benchmarks()
