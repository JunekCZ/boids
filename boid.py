import random
import pygame
from config import BOID_SPEED, BOID_RADIUS, SEPARATION_DISTANCE, WIDTH, HEIGHT

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * BOID_SPEED

    def update(self, neighbors, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR):
        """ Aktualizace směru pohybu na základě okolních boidů """
        if not neighbors:
            return
        
        separation = pygame.Vector2(0, 0)
        alignment = pygame.Vector2(0, 0)
        cohesion = pygame.Vector2(0, 0)
        
        for neighbor in neighbors:
            distance = self.position.distance_to(neighbor.position)
            if distance < SEPARATION_DISTANCE:
                separation += (self.position - neighbor.position).normalize() / distance  
        
            alignment += neighbor.velocity  
            cohesion += neighbor.position  
        
        num_neighbors = len(neighbors)
        if num_neighbors > 0:
            alignment /= num_neighbors
            cohesion = (cohesion / num_neighbors) - self.position
        
        self.velocity += (
            cohesion * COHESION_FACTOR +
            alignment * ALIGNMENT_FACTOR +
            separation * SEPARATION_FACTOR
        )
        self.velocity = self.velocity.normalize() * BOID_SPEED  
        
        self.position += self.velocity

        # Ošetření okrajů
        self.handle_edges()

    def handle_edges(self):
        """ Boid se buď odrazí, nebo teleportuje na druhou stranu """
        mode = "teleport"  # Může být "bounce" nebo "teleport"

        if mode == "bounce":
            if self.position.x <= 0 or self.position.x >= WIDTH:
                self.velocity.x *= -1
            if self.position.y <= 0 or self.position.y >= HEIGHT:
                self.velocity.y *= -1
        
        elif mode == "teleport":
            if self.position.x < 0:
                self.position.x = WIDTH
            elif self.position.x > WIDTH:
                self.position.x = 0
            if self.position.y < 0:
                self.position.y = HEIGHT
            elif self.position.y > HEIGHT:
                self.position.y = 0

    def draw(self, screen):
        """ Vykreslení boida jako trojúhelníku """
        p1 = self.position
        p2 = self.position + self.velocity.rotate(150) * BOID_RADIUS
        p3 = self.position + self.velocity.rotate(-150) * BOID_RADIUS
        pygame.draw.polygon(screen, (0, 255, 0), [p1, p2, p3])
