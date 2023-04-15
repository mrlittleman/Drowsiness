import psycopg2
import pickle
import folium
from geopy.geocoders import Nominatim
from IPython.display import display

# Connect to the database
conn = psycopg2.connect(
    host="containers-us-west-33.railway.app",
    database="railway",
    user="postgres",
    password="NWlmu2CXH3nEtOCImkJk",
    port="5678"
)

# Create a cursor object
cur = conn.cursor()

# Create a map using Folium
map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Execute the SQL query to select all the rows from the table
cur.execute("SELECT * FROM drowsiness_tbl")

# Fetch all the rows returned by the query
rows = cur.fetchall()

# Loop through each row and deserialize the pickled data
for row in rows:

    # Load the pickled data using the pickle module
    pickled_data = row[3] # Assuming the pickled data is in the first column of the table
    deserialized_data = pickle.loads(pickled_data)
    # print(deserialized_data)
    length_of_deserialized_data = len(deserialized_data)

    for num in range(length_of_deserialized_data):

        outer_key = list(deserialized_data)[num]
        # print(outer_key)

        latitude, longitude = deserialized_data[outer_key]['location']

        # print("this is out lat {} and long {}".format(latitude, longitude))
    # Extract the latitude and longitude coordinates
    # longitude, latitude = deserialized_data['Time23:13:41']['location']

    # Add a marker for each location on the map
        geolocator = Nominatim(user_agent="app/1.0")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        tooltip = f"Location: {location.address}"
        folium.Marker(location=[latitude, longitude], tooltip=tooltip).add_to(map)

# Add a layer control to the map
folium.LayerControl().add_to(map)
map.save('map.html')
# Display the map
display(map)

# Close the cursor and the database connection
cur.close()
conn.close()
