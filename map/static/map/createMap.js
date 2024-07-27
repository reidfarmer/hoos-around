let map;
let markers = [];

/*
Sources for this file (the majority came from the third source in here):

Source: https://stackoverflow.com/questions/29701246/move-all-javascript-to-a-separate-file-in-django
    Used for: moving all of the javascript code to separate static files

Source: https://stackoverflow.com/questions/4252130/passing-javascript-variable-to-html-textbox
    Used for: figuring out how to pass JS variables to HTML variables

Source: https://developers.google.com/maps/documentation/javascript/adding-a-google-map#maps_add_map-html
    Used For: the Google Maps developers tutorial on how to initialize a map

Source: https://stackoverflow.com/questions/15792655/add-marker-to-google-map-on-click
    Used For: figuring out how to add a marker to the map
*/

async function initCreateMap() {

    let map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 38.03172018123903, lng: -78.51068497101028},
        zoom: 15,
        styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }] // Hide points of interest labels
            }
          ]
    });

    google.maps.event.addListener(map, "click", (event) => {
        var myMarker = addMarker(event.latLng, map);  // the remainder of this code is in a function below
        var lat = myMarker.getPosition().lat()
        var long = myMarker.getPosition().lng()
        document.getElementById("id_latitude").value = lat
        document.getElementById("id_longitude").value = long
        displayLatLng(lat,long)
    });
    
}

// simple function to display the latitude and longitude to the consolve and to the screen
function displayLatLng(Latitude, Longitude) {
    // Find the element where you want to display the latilongi value (e.g., by its ID)
    var displayElement = document.getElementById("latitudelongitude-display");
    console.log(Latitude, Longitude)
    // Check if the element exists
    if (displayElement) {
        displayElement.textContent = "Latitude: " + Latitude + ", Longitude: " + Longitude;
    }
}

// Adds a marker to the map.
function addMarker(location, map) {
    // Add the marker at the clicked location, and add the next-available label
    // from the array of alphabetical characters.
    clearMarkers();

    var marker = new google.maps.Marker({
      position: location,
      map: map,
      draggable: true,
    });
    map.panTo(location);
    markers.push(marker); // Add the new marker to the markers array
    return marker;
  }

  function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
  }
  markers = []; // Reset the markers array
}

// this is also from that original tutorial
window.initMap = initCreateMap;
