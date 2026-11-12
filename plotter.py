import matplotlib.pyplot as plt

def plot_heart_rate(heart_rate_data):
    if not heart_rate_data:
        print("計測データがありません")
        return

    start_time = heart_rate_data[0]["received_at"]

    elapsed_times = []
    heart_rates = []
    rr_intervals = []

    for sample in heart_rate_data:
        elapsed_times.append(sample["received_at"] - start_time)
        heart_rates.append(sample["heart_rate"])

    plt.plot(elapsed_times, heart_rates)
    plt.title("Heart Rate")
    plt.xlabel("Elapsed time (seconds)")
    plt.ylabel("Heart rate (bpm)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()