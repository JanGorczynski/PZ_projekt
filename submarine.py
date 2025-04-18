import numpy as np
import random

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
        self.move_toward(self.target_x, self.target_y)

    def move_toward(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        dist = np.sqrt(dx**2 + dy**2)
        if dist > 0:
            step = min(self.speed, dist)
            frac = step / dist
            self.x += dx * frac
            self.y += dy * frac

    def generate_report(self, wrecks):
        bx, by, bz = self.get_position()
        min_dist = float('inf')
        for wreck in wrecks:
            wx, wy, wz = wreck
            d = np.sqrt((bx - wx)**2 + (by - wy)**2 + (bz - wz)**2)
            if d < min_dist:
                min_dist = d
        prob = detection_probability(min_dist, detection_range=100.0)
        return (bx, by, bz), prob

def simulate_random(Z, submarines, wrecks, time_steps=200):
    history = []
    for _ in range(time_steps):
        step_data = []
        for sub in submarines:
            sub.navigate_random_waypoint(Z)
            pos, prob = sub.generate_report(wrecks)
            step_data.append({'pos': pos, 'prob': prob})
        history.append(step_data)
    return history
