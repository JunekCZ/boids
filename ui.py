import pygame
import pygame_gui
from config import WIDTH, HEIGHT, COHESION_FACTOR, ALIGNMENT_FACTOR, SEPARATION_FACTOR

class UIManager:
    def __init__(self, manager):
        self.manager = manager
        self.create_sliders()

    def create_sliders(self):
        """ Vytvoří posuvníky pro úpravu parametrů """
        self.cohesion_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 10), (180, 30)),
            start_value=COHESION_FACTOR,
            value_range=(0.0, 0.1),
            manager=self.manager
        )
        
        self.alignment_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 50), (180, 30)),
            start_value=ALIGNMENT_FACTOR,
            value_range=(0.0, 0.1),
            manager=self.manager
        )

        self.separation_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH + 10, 90), (180, 30)),
            start_value=SEPARATION_FACTOR,
            value_range=(0.0, 0.2),
            manager=self.manager
        )

    def handle_events(self, event):
        """ Aktualizuje hodnoty na základě UI vstupu """
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.cohesion_slider:
                    return "cohesion", event.value
                elif event.ui_element == self.alignment_slider:
                    return "alignment", event.value
                elif event.ui_element == self.separation_slider:
                    return "separation", event.value
        return None
