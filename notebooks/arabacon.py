from kafka import KafkaConsumer
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('dark_background')  # Dark background


def main():
    SERVER = "broker:9092"
    TOPIC = "car_test4"

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[SERVER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        # group_id="car-visualizer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        api_version=(3, 7, 0),
    )

    fig, ax = plt.subplots()
    # car_x_data, car_y_data = [], []
    # gps1_x_data, gps1_y_data = [], []
    # gps2_x_data, gps2_y_data = [], []

    def update(frame):
        for message in consumer:
            data = message.value
            print(data)

            car_x, car_y = data["Car"]
            gps1_x, gps1_y = data["GP1"]
            gps2_x, gps2_y = data["GP2"]

            # # Append new positions
            # car_x_data.append(car_x)
            # car_y_data.append(car_y)

            # gps1_x_data.append(gps1_x)
            # gps1_y_data.append(gps1_y)

            # gps2_x_data.append(gps2_x)
            # gps2_y_data.append(gps2_y)

            ax.clear()
            ax.plot(car_x, car_y, 'bs', label='Car')          # Blue
            ax.plot(gps1_x , gps1_y, 'rx', label='GPS1')      # Red
            ax.plot(gps2_x, gps2_y, 'g^', label='GPS2')      # Green

            ax.set_xlim(0, 300)  # Adjust if needed
            ax.set_ylim(0, 400)
            ax.set_xlabel("X Position")
            ax.set_ylabel("Y Position")
            ax.set_title("Car and GPS Positions Over Time")
            ax.legend()
            break  # Only handle one message per frame

    ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
    ani.save('car_gps_positions.gif', writer='pillow')  # Optional: comment out if not needed

    try:
        plt.show()
    except KeyboardInterrupt:
        consumer.close()

if __name__ == "__main__":
    main()
