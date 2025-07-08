class Automation:
    def __init__(self, points):
        self.points = sorted(points)

    def get(self, t):
        if not self.points:
            return 1.0
        for i, (pt, val) in enumerate(self.points):
            if t < pt:
                if i == 0:
                    return val
                t0, v0 = self.points[i - 1]
                t1, v1 = pt, val
                return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
        return self.points[-1][1]
