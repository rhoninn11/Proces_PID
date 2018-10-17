import time as tm
from math import *
import math
from PID import PID

import matplotlib.pyplot as plt


def model():
    czas_probkowania = 0.01
    last_V = 50.0
    last_CA = 0
    CA = 0.0
    CA_zadane = 0.4
    czas_symulacji = 0
    q1 = 1
    q2 = 2
    q3 = 3

    c2 = 0.3

    CA_samples = []
    C1_samples = []
    t_samples = []
    controller = PID(12, 0.1, 0.1)

    while czas_symulacji < 600:
        czas_symulacji += czas_probkowania

        E = CA_zadane - CA
        c1 = controller.regulate(E, czas_probkowania)
        c1 = min(c1, 1.0)
        C1_samples.append(c1)

        V = (q1 + q2 - q3) * czas_probkowania + last_V
        CA = ((c1 * q1 + c2 * q2) * czas_probkowania + V * last_CA) / (2 * V - last_V + q3 * czas_probkowania)
        CA_samples.append(CA)

        t_samples.append(czas_symulacji)

        last_CA = CA
        last_V = V


    plt.plot(t_samples, C1_samples)
    plt.plot(t_samples, CA_samples)
    plt.show()


def main():
    model()


if __name__ == "__main__":
    main()
