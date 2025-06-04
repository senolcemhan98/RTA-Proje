import folium
import json
from kafka import KafkaConsumer
import time
from geopy.geocoders import Nominatim
import tkinter as tk


# Kafka Consumer
SERVER = "localhost:9092"
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

# Alanya'nın GPS koordinatları (başlangıç noktası)
alanya_lat = 36.5740
alanya_lon = 31.9984

# Geocoder
geolocator = Nominatim(user_agent="car_simulation")
def show_popup(car_lat, car_lon, country):
    root = tk.Tk()
    root.title("Car Position Information")

    # Pencereyi oluştur
    msg = f"Car Position: {car_lat}, {car_lon}\nCountry: {country}"
    label = tk.Label(root, text=msg, padx=20, pady=20, font=("Helvetica", 12))
    label.pack()

    # Pencereyi göster
    button = tk.Button(root, text="OK", command=root.destroy, padx=10, pady=5)
    button.pack(pady=10)

    root.mainloop()
# Haritayı oluştur
mymap = folium.Map(location=[alanya_lat, alanya_lon], zoom_start=13)

# Araba simülasyonu
car_lat = alanya_lat
car_lon = alanya_lon

# Araba simülasyonu başlat
try:
    for message in consumer:
        data = message.value
        car_pos = data["Car"]
        gps1_pos = data["GP1"]
        gps2_pos = data["GP2"]

        # Yeni GPS koordinatları al
        car_lat = gps1_pos[0]
        car_lon = gps1_pos[1]

        # Reverse geocoding: GPS koordinatından ülke adı al
        location = geolocator.reverse((car_lat, car_lon), language='en')
        country = "Unknown"
        if location:
            address = location.raw.get('address', {})
            country = address.get('country', "Unknown")

        # Haritayı temizle
        mymap = folium.Map(location=[alanya_lat, alanya_lon], zoom_start=13)

        # Araba konumunu işaretle
        folium.Marker(
            location=[car_lat, car_lon],
            popup=f"Car position: {car_lat}, {car_lon}\nCountry: {country}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mymap)

        # Haritayı kaydet
        mymap.save("alanya_car_simulation.html")
        show_popup(car_lat, car_lon, country)
        # 1 saniye bekle
        time.sleep(1)

except KeyboardInterrupt:
    print("\nConsumer kapatıldı.")
finally:
    consumer.close()
    print("Consumer kapatıldı.")
