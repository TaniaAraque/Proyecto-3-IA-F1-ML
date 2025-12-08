import pygame
import numpy as np
import time
import random
import os
import math

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

        # Cargar y escalar autos - rival ligeramente más grande
        self.car_norris = pygame.image.load("assets/car_norris.png")
        self.car_norris = pygame.transform.scale(self.car_norris, (70, 40))
        self.car_norris.set_colorkey((0, 0, 0))  # Hacer transparente el negro

        self.car_rival = pygame.image.load("assets/car_rival.png")
        self.car_rival = pygame.transform.scale(self.car_rival, (100, 58))
        self.car_rival.set_colorkey((0, 0, 0))  # Hacer transparente el negro

        # Definir trayectoria del circuito (ajusta estos puntos según tu imagen)
        self.track_path = self.create_track_path()
        self.total_distance = self.calculate_path_length()

    def create_track_path(self):
        """
        Define los puntos que forman la trayectoria del circuito.
        Waypoints mapeados desde la imagen real del circuito.
        """
        path = [
            (406, 225),
            (403, 466),
            (415, 475),
            (481, 470),
            (511, 468),
            (529, 458),
            (542, 431),
            (553, 403),
            (569, 385),
            (586, 374),
            (605, 371),
            (632, 381),
            (654, 393),
            (686, 409),
            (742, 414),
            (822, 416),
            (844, 416),
            (857, 406),
            (863, 398),
            (859, 382),
            (784, 341),
            (622, 238),
            (427, 122),
            (402, 107),
            (373, 88),
            (359, 79),
            (355, 93),
            (355, 108),
            (347, 118),
            (327, 121),
            (293, 126),
            (266, 138),
            (237, 154),
            (201, 188),
            (167, 229),
            (132, 263),
            (102, 298),
            (74, 340),
            (35, 408),
            (22, 428),
            (19, 454),
            (30, 477),
            (44, 484),
            (63, 484),
            (87, 469),
            (120, 331),
            (167, 275),
            (217, 271),
            (227, 277),
            (228, 327),
            (236, 341),
            (259, 349),
            (283, 351),
            (293, 323),
            (296, 241),
            (296, 206),
            (307, 180),
            (343, 161),
            (371, 151),
            (389, 147),
            (404, 153),
            (406, 179),
            (406, 225),  # Vuelta al inicio
        ]
        return path

    def calculate_path_length(self):
        """Calcula la longitud total del circuito"""
        total = 0
        for i in range(len(self.track_path) - 1):
            x1, y1 = self.track_path[i]
            x2, y2 = self.track_path[i + 1]
            total += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return total

    def get_position_on_track(self, distance, y_offset=0):
        """
        Obtiene la posición (x, y) y ángulo en el circuito dada una distancia recorrida.
        y_offset permite colocar autos en diferentes carriles.
        """
        # Normalizar distancia
        distance = distance % self.total_distance
        
        # Encontrar segmento del circuito
        accumulated = 0
        for i in range(len(self.track_path) - 1):
            x1, y1 = self.track_path[i]
            x2, y2 = self.track_path[i + 1]
            segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            if accumulated + segment_length >= distance:
                # Interpolación en este segmento
                t = (distance - accumulated) / segment_length
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                
                # Calcular ángulo de la tangente
                angle = math.atan2(y2 - y1, x2 - x1)
                
                # Aplicar offset perpendicular (para diferentes carriles)
                x += y_offset * math.sin(angle)
                y -= y_offset * math.cos(angle)
                
                return x, y, math.degrees(angle)
            
            accumulated += segment_length
        
        # Si llegamos aquí, estamos al final
        x, y = self.track_path[-1]
        return x, y, 0

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

    def draw_car_rotated(self, car_image, x, y, angle):
        """Dibuja un auto rotado según el ángulo de la pista"""
        # Rotar la imagen (invertido para que mire hacia adelante)
        rotated = pygame.transform.rotate(car_image, -angle + 180)
        # Mantener la transparencia
        rotated.set_colorkey((0, 0, 0))
        # Centrar la imagen rotada
        rect = rotated.get_rect(center=(int(x), int(y)))
        self.screen.blit(rotated, rect)


    def run(self):
        alpha = 0.1
        eps = 0.2

        for ep in range(self.episodes):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Distancia recorrida en el circuito (en lugar de posición x)
            norris_distance = 0
            rival_distance = 0

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

            # Carrera: una vuelta completa al circuito
            while norris_distance < self.total_distance and rival_distance < self.total_distance:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                # Avanzar en el circuito
                norris_distance += n_speed
                rival_distance += r_speed

                # Obtener posiciones en el circuito
                # Offset reducido para mantener ambos autos dentro de la pista
                norris_x, norris_y, norris_angle = self.get_position_on_track(norris_distance, y_offset=-8)
                rival_x, rival_y, rival_angle = self.get_position_on_track(rival_distance, y_offset=8)

                # Limpiar pantalla completamente
                self.screen.fill((0, 0, 0))
                
                # Dibujar fondo
                self.screen.blit(self.track, (0,0))

                # Dibujar autos rotados según la curva del circuito
                self.draw_car_rotated(self.car_norris, norris_x, norris_y, norris_angle)
                self.draw_car_rotated(self.car_rival, rival_x, rival_y, rival_angle)

                self.draw_panel(state, action_name, ep)

                pygame.display.update()
                time.sleep(0.02)

            # Determinar ganador
            if norris_distance >= self.total_distance and norris_distance < rival_distance + n_speed:
                reward = 1

            self.Q[state, action] += alpha * (reward - self.Q[state, action])

        pygame.quit()

