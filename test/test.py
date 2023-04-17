import psycopg2
import pickle
import folium
from geopy.geocoders import Nominatim
conn = psycopg2.connect(
    host="containers-us-west-33.railway.app",
    database="railway",
    user="postgres",
    password="NWlmu2CXH3nEtOCImkJk",
    port="5678"
)
cur = conn.cursor()
map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

cur.execute("SELECT * FROM drowsiness_tbl")

rows = cur.fetchall()
for row in rows:
    pickled_data = row[3]
    deserialized_data = pickle.loads(pickled_data)
    print(deserialized_data)
    length_of_deserialized_data = len(deserialized_data)
cur.close()
conn.close()