import numpy as np
import random

def place_shipwreck(Z):
    x_wreck = random.randint(0, len(Z) - 1)
    y_wreck = random.randint(0, len(Z) - 1)
    z_wreck = Z[x_wreck, y_wreck]
    return x_wreck, y_wreck, z_wreck

def detection_probability(distance, detection_range=100.0):
    if distance <= detection_range:
        return 1.0
    ratio = distance / detection_range
    return 0.5 ** (ratio - 1.0)

class Submarine:
    def __init__(self, x, y, z, speed=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.target_x = None
        self.target_y = None

    def get_position(self):
        return (self.x, self.y, self.z)

    def generate_report(self, wreck_pos):
        bx, by, bz = self.get_position()
        wx, wy, wz = wreck_pos
        dist = np.sqrt((bx - wx)**2 + (by - wy)**2 + (bz - wz)**2)
        prob = detection_probability(dist, detection_range=100.0)
        return (bx, by, bz), prob

    def pick_new_waypoint(self, Z):
        size = len(Z) - 1
        self.target_x = random.uniform(0, size)
        self.target_y = random.uniform(0, size)

    def navigate_random_waypoint(self, Z, threshold=20.0):
        if self.target_x is None or self.target_y is None:
            self.pick_new_waypoint(Z)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist_2d = np.sqrt(dx**2 + dy**2)
        if dist_2d < threshold:
            self.pick_new_waypoint(Z)
        self.move_toward(self.target_x, self.target_y, self.z)

    def move_toward(self, tx, ty, tz):
        dx = tx - self.x
        dy = ty - self.y
        dz = tz - self.z 
        dist = np.sqrt(dx**2 + dy**2 + dz**2)
        if dist > 0:
            step = min(self.speed, dist)
            frac = step / dist
            self.x += dx * frac
            self.y += dy * frac

def simulate_search(Z, wreck_pos, submarines, time_steps=200,
                    detect_threshold=0.2):
    x_w, y_w, z_w = wreck_pos
    history = []
    for _ in range(time_steps):
        step_data = []
        for sub in submarines:
            pos, prob = sub.generate_report((x_w, y_w, z_w))
            if prob > detect_threshold:
                sub.move_toward(x_w, y_w, sub.z)
            else:
                sub.navigate_random_waypoint(Z)
            step_data.append({'pos': sub.get_position(), 'prob': prob})
        history.append(step_data)
    return history