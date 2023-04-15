var mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
    '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  tileSize: 512,
  zoomOffset: -1
}).addTo(mymap);

// Loop through the locations array and add markers to the map
for (var i = 0; i < locations.length; i++) {
  var marker = L.marker(locations[i]).addTo(mymap);
}
