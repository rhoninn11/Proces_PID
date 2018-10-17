class PID:
    kp = 0
    ki = 0
    kd = 0
    last_error = 0.0
    last_sum = 0.0

    def __init__(self, P, I, D):
        self.kp = P
        self.ki = I
        self.kd = D

    def regulate(self, error, tn):
        self.last_sum = error + self.last_sum
        output = (self.kp + self.ki * self.last_sum + self.kd * (error - self.last_error)) * tn
        self.last_error = error
        return output
