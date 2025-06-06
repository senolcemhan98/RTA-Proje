import numpy as np
import json
import random
import sys
from datetime import datetime, timedelta
from time import sleep

from kafka import KafkaProducer

if __name__ == "__main__":
    SERVER = "broker:9092"

    producer = KafkaProducer(
        bootstrap_servers=[SERVER],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        api_version=(3, 7, 0),
    )
    # Configsgit
    car_x, car_y = 50, 200  # Initial position

    # Initialize GPS1 and vis settings
    gps_1_std = 15
    gps_2_std = 5
    # Initialize GPS2 and vis settings
    gps_2_1_std = 10
    gps_2_2_std = 6
    try:
        while True:
            
            t = datetime.now() + timedelta(seconds=random.randint(-15, 0))

            if car_x < 100: 
                car_x = car_x + 10
            elif car_x == 100:
                car_y = car_y - 10
                if car_y <= 130:
                    car_x = car_x + 10
            else: 
                car_x = car_x + 10

             
            gps1_x = np.random.normal(car_x, gps_1_std)
            gps1_y = np.random.normal(car_y, gps_1_std)
            gps2_x = np.random.normal(car_x, gps_2_1_std)
            gps2_y = np.random.normal(car_y, gps_2_2_std) 
            
            
            message = {
                "time" : str(t),
                "Car" : (car_x,car_y),
                "GP1" : (gps1_x,gps1_y),
                "GP2" : (gps2_x,gps2_y)
            }
            producer.send("car_test4", value=message)
            print(message)
            sleep(1)
    except KeyboardInterrupt:
        producer.close()