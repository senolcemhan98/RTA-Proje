import numpy as np
import json
import random
import sys
from datetime import datetime, timedelta
from time import sleep

from kafka import KafkaProducer



warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')
warnings.filterwarnings("ignore", category=FutureWarning, module='pandas')

if __name__ == "__main__":
    SERVER = "broker:9092"

    producer = KafkaProducer(
        bootstrap_servers=[SERVER],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        api_version=(3, 7, 0),
    )
    # Configsgit
    width, height = 800, 600
    car_x, car_y = 0, height//2 - 25  # Initial position

    # Initialize GPS1 and vis settings
    gps_1_std = 20
    point_radius = 3
    gps_2_std = 5
    # Initialize GPS2 and vis settings
    gps_2_1_std = 31
    gps_2_2_std = 9
    try:
        while True:
            
            t = datetime.now() + timedelta(seconds=random.randint(-15, 0))
            car_x = car_x + 5
            y_offset = 25 # When drawing we are drawing 25 thats why We are adding here
            gps1_x = np.random.normal(car_x, gps_1_std)
            gps1_y = np.random.normal(car_y, gps_1_std)
            gps2_x = np.random.normal(car_x, gps_2_1_std)
            gps2_y = np.random.normal(car_y, gps_2_2_std) + y_offset 
            
            
            message = {
                "time" : str(t),
                "Car" : (car_x,car_y),
                "GP1" : (gps1_x,gps1_y),
                "GP2" : (gps2_x,gps2_y)
            }
            producer.send("car_test1", value=message)
            sleep(1)
    except KeyboardInterr:
        producer.close()