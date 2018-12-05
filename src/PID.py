class PID:
    kp = 0
    ki = 0
    kd = 0
    last_error = 0.0
    integral = 0.0
    derivative = 0.0

    def __init__(self, P, I, D):
        self.kp = P
        self.ki = I
        self.kd = D

    def regulate(self, system_error, tn):
        self.integral = system_error * tn + self.integral
        self.derivative = (system_error - self.last_error) / tn
        output = self.kp*system_error + self.ki * self.integral + self.kd * self.derivative
        self.last_error = system_error
        return output
