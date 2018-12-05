from PID import PID
import matplotlib.pyplot as plt


def main():
    sample_time = 0.01  # czas próbkowania
    last_v = 50.0  # objętość w poprzedniej próbce czasu
    last_ca = 0  # stężenie w poprzedniej próbce czasu
    current_ca = 0.0  # stężenie w danej próbce czasu
    given_ca = 0.4  # zadane stężenie
    given_substance_volume = given_ca * last_v  # zadana objętość substancji w zbiorniku
    simulation_time = 0  # czas symulacji
    q2 = 2  # prędkość przepływu strumienia zakłócającego
    q3 = 3  # prędkość opdływu cieczy ze zbiornika
    c1 = 0.7  # stężenie w strumieniu sterowanym
    c2 = 0.3  # stężenie w strumieniu zakłócającym

    ca_samples = []  # próbki stężenia w zbiorniku
    q1_samples = []  # próbki prędkości przepływu
    substance_volume_samples = []  # próbki objętości substancji
    t_samples = []  # próbki czasu
    v_samples = []  # próbki objętości
    controller = PID(1, 0, 0.1)

    while simulation_time < 200:
        simulation_time += sample_time
        current_substance_volume = current_ca * last_v
        system_error = given_substance_volume - current_substance_volume
        q1 = controller.regulate(system_error, sample_time) / c1
        q1 = min(q1, 5.0)
        q1 = max(q1, 0.0)

        current_v = (q1 + q2 - q3) * sample_time + last_v
        current_ca = ((c1 * q1 + c2 * q2) * sample_time + current_v * last_ca) / (
                2 * current_v - last_v + q3 * sample_time)

        ca_samples.append(current_ca*100)
        v_samples.append(current_v)
        t_samples.append(simulation_time)
        q1_samples.append(q1)
        substance_volume_samples.append(current_substance_volume)

        last_ca = current_ca
        last_v = current_v

    save_to_file('prędkość_przepływu_próbki', q1_samples)
    save_to_file('objętość_w_zbiorniku_próbki', v_samples)
    save_to_file('substancja_w_zbiorniku_próbki', substance_volume_samples)
    save_to_file('próbki_czasu', t_samples)


    plt.figure('Wykres objętości')
    plt.ylabel('objętość [m3]')
    plt.xlabel('czas [s]')
    plt.plot(t_samples, substance_volume_samples, label='Objętość substancji w zbiorniku')
    plt.title('V(t)')

    plt.xlabel('czas [s]')
    plt.ylabel('objętość [m3]')
    plt.plot(t_samples, v_samples, label='Objętość całkowita mieszanki w zbiorniku')
    plt.title('V(t)')
    plt.legend()

    plt.figure('Prędkość przepływu strumienia sterowanego')
    plt.xlabel('czas [s]')
    plt.ylabel('prędkość przepływu [m3/s]')
    plt.plot(t_samples, q1_samples)
    plt.title('q(t)')

    plt.figure('Stężenie w zbiorniku')
    plt.xlabel('czas [s]')
    plt.ylabel('stężenie [%]')
    plt.plot(t_samples, ca_samples)
    plt.title('ca(t)')

    plt.show()


def save_to_file(title, data):
    file = open(title + '.txt', 'w+')
    for i in data:
        file.write(str(i) + ';')
    file.close()


if __name__ == "__main__":
    main()
