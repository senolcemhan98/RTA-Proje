from kafka import KafkaConsumer
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

global_errors = {
    "GPS1": 0.0,
    "GPS2": 0.0,
    "Combined": 0.0
}

distances = {
    "GPS1": [],
    "GPS2": [],
    "Combined": []
}

def combine_positions(gps1, gps2):
    combined_x = (gps1[0] + gps2[0]) / 2
    combined_y = (gps1[1] + gps2[1]) / 2
    return (combined_x, combined_y)

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def main():
    SERVER = "broker:9092"
    TOPIC = "car_test1"

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[SERVER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        api_version=(3, 7, 0),
    )

    fig, ax = plt.subplots()
    x_data, y_data_gps1, y_data_gps2, y_data_combined = [], [], [], []

    def update(frame):
        for message in consumer:
            data = message.value
            car_pos = data["Car"]
            gps1_pos = data["GP1"]
            gps2_pos = data["GP2"]

            distance_gps1_to_car = calculate_distance(car_pos, gps1_pos)
            distance_gps2_to_car = calculate_distance(car_pos, gps2_pos)
            
            combined_pos = combine_positions(gps1_pos, gps2_pos)
            distance_combined_to_car = calculate_distance(car_pos, combined_pos)

            global_errors["GPS1"] += distance_gps1_to_car
            global_errors["GPS2"] += distance_gps2_to_car
            global_errors["Combined"] += distance_combined_to_car
            
            distances["GPS1"].append(global_errors["GPS1"])
            distances["GPS2"].append(global_errors["GPS2"])
            distances["Combined"].append(global_errors["Combined"])
            
            x_data.append(len(x_data))
            y_data_gps1.append(global_errors["GPS1"])
            y_data_gps2.append(global_errors["GPS2"])
            y_data_combined.append(global_errors["Combined"])
            
            ax.clear()
            ax.plot(x_data, y_data_gps1, label='GPS1 Error')
            ax.plot(x_data, y_data_gps2, label='GPS2 Error')
            ax.plot(x_data, y_data_combined, label='Combined Error')
            
            ax.legend()
            ax.set_xlabel('Time')
            ax.set_ylabel('Cumulative Error')
            ax.set_title('Real-time GPS Error Tracking')
            break

    ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
    ani.save('gps_errors.gif', writer='pillow')

    try:
        plt.show()
    except KeyboardInterrupt:
        consumer.close()

if __name__ == "__main__":
    main()
