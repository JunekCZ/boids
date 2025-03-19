from pyquadtree import QuadTree

class QuadTreeManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rebuild([])  # Inicializace prázdného stromu

    def rebuild(self, boids):
        """ Vytvoří nový QuadTree a naplní ho boidy """
        self.quadtree = QuadTree(bbox=(0, 0, self.width, self.height), max_elements=10, max_depth=5)
        for boid in boids:
            self.quadtree.add(boid, (boid.position.x, boid.position.y))

    def get_neighbors(self, boid, radius=50):
        """ Najde sousedy boida v rámci jeho zorného pole """
        vision_box = (
            boid.position.x - radius, boid.position.y - radius,
            boid.position.x + radius, boid.position.y + radius
        )
        neighbors = self.quadtree.query(vision_box)
        return [n.item for n in neighbors if n.item != boid]

    def get_grid_boxes(self):
        """ Získá všechny bounding boxy mřížky QuadTree """
        return self.quadtree.get_all_bbox()
