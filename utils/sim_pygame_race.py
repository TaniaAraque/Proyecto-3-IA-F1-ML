import pygame
import numpy as np
import time
import random
import os

class F1RaceSim:
    def __init__(self, env, Q, episodes=200):
        pygame.init()

        self.env = env
        self.Q = Q
        self.episodes = episodes

        self.W = 1200
        self.H = 600

        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("Simulación F1 – Aprendizaje por Refuerzo")

        self.font = pygame.font.SysFont("Arial", 26)
        self.small = pygame.font.SysFont("Arial", 20)

        self.white = (255,255,255)
        self.black = (0,0,0)
        self.lightgray = (220,220,220)

        self.track = pygame.image.load("assets/track.png")
        self.track = pygame.transform.scale(self.track, (900, 600))

        self.car_norris = pygame.image.load("assets/car_norris.png")
        self.car_norris = pygame.transform.scale(self.car_norris, (70, 40))

        self.car_rival = pygame.image.load("assets/car_rival.png")
        self.car_rival = pygame.transform.scale(self.car_rival, (70, 40))

    def draw_panel(self, state, action_name, ep):
        panel_x = 910
        pygame.draw.rect(self.screen, (245,245,245), (panel_x, 0, 290, 600))

        self.screen.blit(self.font.render("Panel de Control", True, self.black), (panel_x+20, 20))
        self.screen.blit(self.small.render(f"Episodio: {ep}", True, self.black), (panel_x+20, 70))
        self.screen.blit(self.small.render(f"Estado: {state}", True, self.black), (panel_x+20, 100))
        self.screen.blit(self.small.render(f"Acción: {action_name}", True, self.black), (panel_x+20, 130))

        self.screen.blit(self.small.render("Q-Table", True, self.black), (panel_x+20, 170))

        cell_w, cell_h = 80, 50
        row_y = 210

        for s in range(3):
            for a in range(3):
                val = self.Q[s,a]
                rect = pygame.Rect(panel_x+20 + a*cell_w, row_y + s*cell_h, cell_w-5, cell_h-5)
                pygame.draw.rect(self.screen, self.lightgray, rect)
                txt = self.small.render(f"{val:.2f}", True, self.black)
                self.screen.blit(txt, (rect.x + 10, rect.y + 10))

    def run(self):
        alpha = 0.1
        eps = 0.2
        finish_x = 800 

        for ep in range(self.episodes):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            norris_x = 100
            norris_y = 250

            rival_x = 100
            rival_y = 330

            state = self.env.reset()
            action = np.random.randint(3) if random.random() < eps else np.argmax(self.Q[state])
            action_name = ["Conservadora","Normal","Agresiva"][action]

            if action == 0:
                n_speed = 5 + random.random()*1
            elif action == 1:
                n_speed = 7 + random.random()*1.5
            else:
                if random.random() < 0.18:
                    n_speed = 3
                else:
                    n_speed = 9 + random.random()*2

            r_speed = 6 + random.random()*2.5

            reward = 0

            while norris_x < finish_x and rival_x < finish_x:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                norris_x += n_speed
                rival_x += r_speed

                self.screen.blit(self.track, (0,0))

                self.screen.blit(self.car_norris, (norris_x, norris_y))
                self.screen.blit(self.car_rival, (rival_x, rival_y))

                pygame.draw.line(self.screen, self.black, (finish_x, 200),(finish_x, 400),3)

                self.draw_panel(state, action_name, ep)

                pygame.display.update()
                time.sleep(0.02)

            if norris_x >= finish_x and norris_x > rival_x:
                reward = 1

            self.Q[state, action] += alpha * (reward - self.Q[state, action])

        pygame.quit()
