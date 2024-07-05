import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def low_pass_filter(signal, cutoff_frequency, sampling_rate):
    fft_signal = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1 / sampling_rate)
    filtered_fft_signal = fft_signal.copy()
    filtered_fft_signal[np.abs(frequencies) > cutoff_frequency] = 0
    filtered_signal = np.fft.ifft(filtered_fft_signal).real
    return filtered_signal


def moving_average_filter(signal, window_size):
    return pd.Series(signal).rolling(window=window_size, center=True).mean().bfill().ffill().values

def plot_signal(signal, title, xlabel, ylabel, legend):
    plt.plot(signal, label=legend)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def save_signal_to_csv(signal, filename):
    df = pd.DataFrame(signal, columns=['Filtered_Signal'])
    df.to_csv(filename, index=False)
    print(f"Filtered signal saved to {filename}")

def display_original_signal(signal):
    plot_signal(signal, 'Oscylogram zaszumionego sygnału', 'Próbki', 'Amplituda', 'Zaszumiony sygnał')

def apply_low_pass_filter(signal):
    sampling_rate = int(input("Podaj częstotliwość próbkowania (np. 500): "))
    cutoff_frequency = int(input("Podaj częstotliwość odcięcia (np. 50): "))
    filtered_signal = low_pass_filter(signal, cutoff_frequency, sampling_rate)
    plot_signal(filtered_signal, 'Oscylogram Sygnału po filtrowaniu dolnoprzepustowym', 'Próbki', 'Amplituda', 'Sygnał po filtrowaniu dolnoprzepustowym')
    save_signal_to_csv(filtered_signal, 'filtered_signal_lp.csv')

def apply_moving_average_filter(signal):
    window_size = int(input("Podaj rozmiar okna (np. 5): "))
    filtered_signal = moving_average_filter(signal, window_size)
    plot_signal(filtered_signal, 'Oscylogram sygnału po średniej ruchomej', 'Próbki', 'Amplituda', 'Sygnał po średniej ruchomej')
    save_signal_to_csv(filtered_signal, 'filtered_signal_ma.csv')

def apply_both_filters(signal):
    sampling_rate = int(input("Podaj częstotliwość próbkowania (np. 500): "))
    cutoff_frequency = int(input("Podaj częstotliwość odcięcia (np. 50): "))
    window_size = int(input("Podaj rozmiar okna (np. 5): "))
    
    # Apply low-pass filter first
    filtered_signal_lp = low_pass_filter(signal, cutoff_frequency, sampling_rate)
    
    # Then apply moving average filter
    filtered_signal_both = moving_average_filter(filtered_signal_lp, window_size)
    
    plot_signal(filtered_signal_both, 'Oscylogram Sygnału po Obu Filtrach', 'Próbki', 'Amplituda', 'Sygnał po Obu Filtrach')
    save_signal_to_csv(filtered_signal_both, 'filtered_signal_both.csv')

def main(file_path):
    # Load the CSV file
    data = pd.read_csv(file_path, header=None)

    # Extract signal values
    signal = data.values.flatten()

    while True:
        print("\nProgram odszumiacz (odpluskiwacz nawiązanie)")
        print("1. Wyświetl oryginalny sygnał")
        print("2. Zastosuj filtr dolnoprzepustowy")
        print("3. Zastosuj filtr średniej ruchomej")
        print("4. Zastosuj oba filtry jednocześnie")
        print("5. Zakończ")
        choice = input("Wybierz: ")

        if choice == '1':
            display_original_signal(signal)
        elif choice == '2':
            apply_low_pass_filter(signal)
        elif choice == '3':
            apply_moving_average_filter(signal)
        elif choice == '4':
            apply_both_filters(signal)
        elif choice == '5':
            print("Zamykanie programu.")
            sys.exit(0)
        else:
            print("Nie ma takiej opcji")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
