import csv

def save_to_csv(heart_rate_data):
    with open("csv/heart_rate.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["packet_id", "received_at", "heart_rate", "rr_intervals"])
        writer.writeheader()

        for packet_id, sample in enumerate(heart_rate_data, start=1):
            writer.writerow({
                "packet_id": packet_id,
                "received_at": sample["received_at"],
                "heart_rate": sample["heart_rate"],
                "rr_intervals": sample["rr_intervals"],
            })

    with open("csv/rr_intervals.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["packet_id", "received_at", "rr_index", "rr_interval_ms"],
        )
        writer.writeheader()

        for packet_id, sample in enumerate(heart_rate_data, start=1):
            for rr_index, rr in enumerate(sample["rr_intervals"], start=1):
                writer.writerow({
                    "packet_id": packet_id,
                    "received_at": sample["received_at"],
                    "rr_index": rr_index,
                    "rr_interval_ms": rr,
                })