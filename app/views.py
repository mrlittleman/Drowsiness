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
    cur = conn.cursor()
    map = folium.Map(location=[14.5995, 120.9842], zoom_start=12)
    max_date = None
    cur.execute("SELECT * FROM drowsiness_tbl")
    rows = cur.fetchall()

    for row in rows:

        pickled_data = row[3]
        deserialized_data = pickle.loads(pickled_data)

        for num, outer_key in enumerate(deserialized_data):
            latitude, longitude = deserialized_data[outer_key]['location']
            drowsiness = deserialized_data[outer_key]['drowsy']
            time_located = deserialized_data[outer_key]['time']

            if max_date is None or time_located > max_date:
                max_date = time_located

        latitude, longitude = deserialized_data[outer_key]['location']
        drowsiness = deserialized_data[outer_key]['drowsy']
        geolocator = Nominatim(user_agent="app/1.0")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        tooltip = f"Location: {location.address}, Date and Time: {max_date}, Drowsy {drowsiness}"
        folium.Marker(location=[latitude, longitude], tooltip=tooltip).add_to(map)

    folium.LayerControl().add_to(map)
    map = map._repr_html_()

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
