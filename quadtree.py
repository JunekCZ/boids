from pyquadtree import QuadTree
from config import NUM_BOIDS, WIDTH
import math

class QuadTreeManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rebuild([])

    def rebuild(self, boids):
        self.quadtree = QuadTree(bbox=(0, 0, self.width, self.height), max_elements=math.sqrt(NUM_BOIDS) / 2, max_depth=math.log2(WIDTH) - 2)
        for boid in boids:
            self.quadtree.add(boid, (boid.position.x, boid.position.y))

    def get_neighbors(self, boid, radius=50):
        vision_box = (
            boid.position.x - radius, boid.position.y - radius,
            boid.position.x + radius, boid.position.y + radius
        )
        neighbors = self.quadtree.query(vision_box)
        return [n.item for n in neighbors if n.item != boid]

    def get_grid_boxes(self):
        return self.quadtree.get_all_bbox()
