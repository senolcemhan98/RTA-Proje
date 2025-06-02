from kafka import KafkaConsumer
import json

if __name__ == "__main__":
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

    try:
        for message in consumer:
            print("Received message:")
            #print(json.dumps(message.value, indent=4))
            car_info = message.value.get("Car")
            
            # TODO: GPS1 ve GPS2 nin infolarini oku
            # TODO: Car a gore distancelarina bak ve local-global(E1 VE E2) errorleri print et
            # TODO: Daha sonra bu 2 konumu bir sekilde birlestirecek bir algoritma yaz BU NOKTANINDA LOCAL VE GLOBALINI AL
            # TODO: Daha sonra global error ve bu fonksiyonun ciktisinin Car a gore distanceina bak
            # TODO: Fonksiyondan onceki ve sonraki distancelar nasil degismis bir iyilesme katetmis miyiz onlara bak!    
            if car_info:
                print("Car information:", car_info)

    except KeyboardInterrupt:
        consumer.close()
