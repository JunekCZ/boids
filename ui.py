import pygame
import pygame_gui
from config import WIDTH, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR, SEPARATION_DISTANCE, VISION_RADIUS

class UIManager:
    def __init__(self, manager, use_quadtree):
        self.manager = manager
        self.create_sliders(use_quadtree)

    def create_sliders(self, use_quadtree):
        self.cohesion_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 10), (180, 30)),
            text="Cohesion",
            manager=self.manager
        )
        self.cohesion_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 40), (180, 30)),
            start_value=COHESION_FACTOR,
            value_range=(0.0, 0.1),
            manager=self.manager
        )

        self.alignment_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 80), (180, 30)),
            text="Alignment",
            manager=self.manager
        )
        self.alignment_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 110), (180, 30)),
            start_value=ALIGNMENT_FACTOR,
            value_range=(0.0, 0.1),
            manager=self.manager
        )

        self.separation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 150), (180, 30)),
            text="Separation factor",
            manager=self.manager
        )
        self.separation_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 180), (180, 30)),
            start_value=SEPARATION_FACTOR,
            value_range=(0.0, 0.2),
            manager=self.manager
        )

        self.separation_distance_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 290), (180, 30)),
            text="Separation distance",
            manager=self.manager
        )
        self.separation_distance_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 320), (180, 30)),
            start_value=SEPARATION_DISTANCE,
            value_range=(5, 100),
            manager=self.manager
        )

        self.vision_radius_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 220), (180, 30)),
            text="Vision radius",
            manager=self.manager
        )
        self.vision_radius_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 250), (180, 30)),
            start_value=VISION_RADIUS,
            value_range=(10, 200),
            manager=self.manager
        )

        self.mode_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH + 10, 360), (180, 30)),
            text="Mode: " + ("Quadtree" if use_quadtree else "Brute force"),
            manager=self.manager
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.cohesion_slider:
                    return "cohesion", event.value
                if event.ui_element == self.alignment_slider:
                    return "alignment", event.value
                if event.ui_element == self.separation_slider:
                    return "separation", event.value
                if event.ui_element == self.vision_radius_slider:
                    return "vision_radius", event.value
                if event.ui_element == self.separation_distance_slider:
                    return "separation_distance", event.value
        return None

    def update_mode_label(self, use_quadtree):
        self.mode_label.set_text("Mode: " + ("Quadtree" if use_quadtree else "Brute force"))
