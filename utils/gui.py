import pygame
import numpy as np
import sys

class F1PygameGUI:
    def __init__(self, Q):
        pygame.init()
        self.Q = Q
        self.actions = {0: "Conservadora", 1: "Normal", 2: "Agresiva"}

        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("F1 Q-Learning – Estrategia Óptima")

        self.font = pygame.font.SysFont("Arial", 28)
        
        self.state = None
        self.result_text = ""

    def draw_button(self, text, x, y, w, h, action_value=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        color = (150,150,150)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            color = (200,200,200)
            if click[0] == 1 and action_value is not None:
                self.evaluate(action_value)

        pygame.draw.rect(self.screen, color, (x,y,w,h))
        label = self.font.render(text, True, (0,0,0))
        self.screen.blit(label, (x+10, y+10))

    def evaluate(self, state):
        self.state = state
        action = int(np.argmax(self.Q[state]))
        self.result_text = f"Estado {state} → Estrategia: {self.actions[action]}"

    def run(self):
        running = True

        while running:
            self.screen.fill((255,255,255))

            title = self.font.render("Selecciona la posición de largada (estado)", True, (0,0,0))
            self.screen.blit(title, (40, 40))

            self.draw_button("0 (Pole)", 50, 120, 150, 60, 0)
            self.draw_button("1 (P2-P3)", 225, 120, 150, 60, 1)
            self.draw_button("2 (P4-P6)", 400, 120, 150, 60, 2)

            if self.result_text:
                result_label = self.font.render(self.result_text, True, (0,0,150))
                self.screen.blit(result_label, (50, 250))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()

        pygame.quit()
        sys.exit()
