import random

class F1NorrisEnv:
    def __init__(self):
        self.n_states = 3        # 0=pole, 1=P2-P3, 2=P4-P6
        self.n_actions = 3       # 0=cons,1=norm,2=agre

        self.base_points = {
            "Norris": 408,
            "Verstappen": 396,
            "Piastri": 392
        }

        self.points_table = {
            1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
            6: 8, 7: 6, 8: 4, 9: 2, 10: 1
        }

    def reset(self):
        self.state = random.choice([0, 1, 2])
        return self.state
    
    def _get_finish_sample(self, dist):
        # Extraer positions (population) y probabilidades (weights)
        positions = [item[0] for item in dist]
        weights = [item[1] for item in dist]
        
        return random.choices(positions, weights=weights, k=1)[0]


    def sample_finish_norris(self, state, action):
        if state == 0:
            if action == 0:
                dist = [(1, 0.4), (2, 0.3), (3, 0.2), (4, 0.1)]
            elif action == 1:
                dist = [(1, 0.5), (2, 0.25), (3, 0.15), (4, 0.1)]
            else:
                dist = [(1, 0.55), (2, 0.20), (3, 0.10), (4, 0.10), (20, 0.05)]
        elif state == 1:
            if action == 0:
                dist = [(1, 0.30), (2, 0.35), (3, 0.20), (4, 0.10), (5, 0.05)]
            elif action == 1:
                dist = [(1, 0.35), (2, 0.30), (3, 0.20), (4, 0.10), (10, 0.05)]
            else:
                dist = [(1, 0.40), (2, 0.25), (3, 0.15), (4, 0.10), (20, 0.10)]
        else:
            if action == 0:
                dist = [(2, 0.25), (3, 0.30), (4, 0.20), (5, 0.15), (6, 0.10)]
            elif action == 1:
                dist = [(1, 0.20), (2, 0.25), (3, 0.25), (4, 0.15), (10, 0.15)]
            else:
                dist = [(1, 0.25), (2, 0.20), (3, 0.20), (5, 0.15), (20, 0.20)]

        #r = random.random()
        #acum = 0
        #for pos, p in dist:
        #    acum += p
        #    if r <= acum:
        #        return pos
        #return dist[-1][0]
        return self._get_finish_sample(dist)

    def sample_finish_rival(self, driver_name):
        if driver_name == "Verstappen":
            dist = [(1, 0.35), (2, 0.25), (3, 0.20), (4, 0.10), (5, 0.05), (10, 0.05)]
        else:
            dist = [(1, 0.30), (2, 0.25), (3, 0.20), (4, 0.10), (5, 0.10), (10, 0.05)]

        #r = random.random()
        #acum = 0
        #for pos, p in dist:
        #    acum += p
        #    if r <= acum:
        #        return pos
        #return dist[-1][0]
        return self._get_finish_sample(dist)

    def points_for_position(self, pos):
        return self.points_table.get(pos, 0)

    def step(self, action):
        state = self.state

        pos_n = self.sample_finish_norris(state, action)
        pos_v = self.sample_finish_rival("Verstappen")
        pos_p = self.sample_finish_rival("Piastri")

        # Puntos ganados en la carrera.
        pts_n_carrera = self.points_for_position(pos_n)
        pts_v_carrera = self.points_for_position(pos_v)
        pts_p_carrera = self.points_for_position(pos_p)

        # ------------------------------------------------------------------------------------------------------------------------------
        # ESTRATEGIA CORTO PLAZO: MAXIMIZAR LA CARRERA.
        #max_carrera = max(pts_n_carrera, pts_v_carrera, pts_p_carrera)
        #reward = 1 if (pts_n_carrera == max_carrera and pts_n_carrera > pts_v_carrera and pts_n_carrera > pts_p_carrera) else 0
        #--------------------------------------------------------------------------------------------------------------------------------

        # TOTAL FINAL del Campeonato.
        pts_n = self.base_points["Norris"] + pts_n_carrera
        pts_v = self.base_points["Verstappen"] + pts_v_carrera
        pts_p = self.base_points["Piastri"] + pts_p_carrera


        #ESTRATEGIA LARGO PLAZO: ASEGURAR EL CAMPEONATO.
        max_pts = max(pts_n, pts_v, pts_p)
        # Global. Puntos iniciales y puntos ganados.
        reward = 1 if (pts_n == max_pts and pts_n > pts_v and pts_n > pts_p) else 0

        next_state = state
        done = True

        # LARGO PLAZO
        return next_state, reward, done, {
            "pos_norris": pos_n,
            "pos_ver": pos_v,
            "pos_pias": pos_p,
            "pts_norris": pts_n,
            "pts_ver": pts_v,
            "pts_pias": pts_p,
        }


        #return next_state, reward, done, {
        #    "pos_norris": pos_n,
        #    "pos_ver": pos_v,
        #    "pos_pias": pos_p,
        #    "pts_norris": pts_n_carrera,
        #    "pts_ver": pts_v_carrera,
        #    "pts_pias": pts_p_carrera,
        #}
