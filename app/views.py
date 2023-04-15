from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import psycopg2
import pickle
import folium
from geopy.geocoders import Nominatim
# Create your views here.





@login_required(login_url='login')
def Dashboard(request):
    template = 'index.html'
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
    map = folium.Map(location=[14.5995, 120.9842], zoom_start=12)

    # Execute the SQL query to select all the rows from the table
    cur.execute("SELECT * FROM drowsiness_tbl")

    # Fetch all the rows returned by the query
    rows = cur.fetchall()

    # Loop through each row and deserialize the pickled data
    for row in rows:

        # Load the pickled data using the pickle module
        pickled_data = row[3] # Assuming the pickled data is in the first column of the table
        deserialized_data = pickle.loads(pickled_data)
        length_of_deserialized_data = len(deserialized_data)

        for num in range(length_of_deserialized_data):

            outer_key = list(deserialized_data)[num]
            latitude, longitude = deserialized_data[outer_key]['location']
            drowsiness = deserialized_data[outer_key]['drowsy']
            time_located = deserialized_data[outer_key]['time']

            geolocator = Nominatim(user_agent="app/1.0")
            location = geolocator.reverse(f"{latitude}, {longitude}")
            tooltip = f"Location: {location.address}, Date and Time: {time_located}, Drowsy {drowsiness}"
            folium.Marker(location=[latitude, longitude], tooltip=tooltip).add_to(map)

    # Add a layer control to the map
    folium.LayerControl().add_to(map)
    map = map._repr_html_()

    # Close the cursor and the database connection
    cur.close()
    conn.close()
    
    return render(request, template, {'map': map})

def login_view(request):
    template = 'landing.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, template)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')
