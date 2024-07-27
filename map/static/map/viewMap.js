var prevLatlng = null;

/*
We put the sources with specific implementations above those implementations.

Sources (the majority of our implementation came from the Google Developers tutorial (the first source here):

Source: https://developers.google.com/maps/documentation/javascript/adding-a-google-map#maps_add_map-html
    Used For: initializing the map and learning how to interact with it

Source: https://cbi-analytics.nl/django-google-maps-tutorial-4-creating-a-google-map-maps-javascript-api/
    Used For: This was a nearly identical tutorial to the google developers tutorial. We used it to help us understand
                 better the google tutorial.
Source: https://cbi-analytics.nl/python-django-google-maps-api-set-up-api-in-google-cloud-platform/
    Used For: This was another nearly identical tutorial to the google developers tutorial on how to make sure that our
                 project was aligned with the Google Cloud requirements.
Source: https://stackoverflow.com/questions/29701246/move-all-javascript-to-a-separate-file-in-django
    Used For: recommendation and small tutorial on how to move all of the Javascript code for rendering the map to a
                 different file
Source: https://stackoverflow.com/questions/4252130/passing-javascript-variable-to-html-textbox
    Used For: small solution on how to pass Javascript variables into HTML objects. This was used to help us render
                 events.
*/

function initViewMap() {

    let data = document.getElementById("data").value
    const myLatlng = {lat: 38.03567, lng: -78.50340};
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: {lat: 38.03567, lng: -78.50340},
        styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }] // Hide points of interest labels
            }
          ]
    });
    const academicIcon = {
        url: 'https://cdn4.iconfinder.com/data/icons/miscellaneous-iv-glyph/160/graduation-cap-512.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(40, 40), // Adjust the size as needed
    };
    const artIcon = {
        url: 'https://cdn-icons-png.flaticon.com/512/4893/4893176.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(30, 30), // Adjust the size as needed
    };
    const careerIcon = {
        url: 'https://static.thenounproject.com/png/199301-200.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(40, 40), // Adjust the size as needed
    };
    const clubIcon = {
        url: 'https://cdn-icons-png.flaticon.com/512/3990/3990972.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(40, 40), // Adjust the size as needed
    };
    const foodIcon = {
        url: 'https://openclipart.org/image/800px/289282', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(30, 30), // Adjust the size as needed
    };
    const musicIcon = {
        url: 'https://creazilla-store.fra1.digitaloceanspaces.com/icons/3431524/music-icon-md.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(30, 30), // Adjust the size as needed
    };
    const socialIcon = {
        url: 'https://cdn-icons-png.flaticon.com/512/33/33308.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(35, 35), // Adjust the size as needed
    };
    const sportsIcon = {
        url: 'https://cdn-icons-png.flaticon.com/512/857/857492.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(35, 35), // Adjust the size as needed
    };
    const volunteerIcon = {
        url: 'https://cdn2.iconfinder.com/data/icons/cv-curriculum-vitae/100/set-cv2-06-512.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(40, 40), // Adjust the size as needed
    };
    const baseIcon = {
        url: 'https://static.vecteezy.com/system/resources/thumbnails/016/314/852/small/map-pointer-icon-gps-location-symbol-maps-pin-location-map-icon-free-png.png', // pull the custom marker image off internet
        scaledSize: new google.maps.Size(40, 40), // Adjust the size as needed
    };
    // parse the JSON that was grabbed from the html
    let d = JSON.parse(data);
    for (const e in d) {
        // d[e].lat and d[e].lng --> returns the latitude and longitude for this
        // Only display approved events
        const approved = d[e].approved
        console.log(approved)

        if (approved) {
            const myLatlng = {lat: parseFloat(d[e].lat), lng: parseFloat(d[e].lng)};

            var icon = baseIcon;
            if(d[e].category === 'academic'){ icon = academicIcon; }
            if(d[e].category === 'art'){ icon = artIcon; }
            if(d[e].category === 'career'){ icon = careerIcon; }
            if(d[e].category === 'club'){ icon = clubIcon; }
            if(d[e].category === 'food'){ icon = foodIcon; }
            if(d[e].category === 'music'){ icon = musicIcon; }
            if(d[e].category === 'social'){ icon = socialIcon; }
            if(d[e].category === 'sports'){ icon = sportsIcon; }
            if(d[e].category === 'volunteering'){ icon = volunteerIcon; }

            const marker = new google.maps.Marker({
                position: {lat: parseFloat(d[e].lat), lng: parseFloat(d[e].lng)},
                map: map,
                title: d[e].title,
                icon: icon,
            });
            
            marker.addListener("click", () => {

                // initialize InfoWindow
    //            let infoWindow = new google.maps.InfoWindow({
    //                content: "Click to get event data",
    //                position: myLatlng,
    //            });
    //
    //            // when use clicks, display content
    //            infoWindow = new google.maps.InfoWindow({
    //                position: myLatlng,
    //            });
    //            infoWindow.setContent("content");
    //                infoWindow.open(map);

                var looking_for = myLatlng.lat + ", " + myLatlng.lng;
                // console.log(looking_for);
                if (prevLatlng !== null) {
                    resetElement(prevLatlng);
                }
                toggleElement(looking_for);
                prevLatlng = looking_for;

                // old code used to send post data back to django. Realized it wasn't the correct approach.
                // sendLatLongToDjango(myLatlng, csrftoken);
                // function sendLatLongToDjango(myLatLong, csrftoken) {
                //     fetch('map', {
                //         method: 'POST',
                //         headers: {
                //             'X-CSRFToken': csrftoken,
                //             'Content-Type': 'application/x-www-form-urlencoded',
                //         },
                //         body: new URLSearchParams({
                //             'lat': myLatLong.lat,
                //             'lng': myLatLong.lng,
                //         }),
                //     });
                // }
            });   
        }
    }
}

function toggleElement(id) {
    var event = document.getElementById(id);
    var displaySetting = event.style.display;
    event.style.display = 'block';
//    if ( displaySetting === 'block')  {
//        event.style.display = 'none';
//    }
//    else {
//        event.style.display = 'block';
//    }
}

function resetElement(id) {
    var event = document.getElementById(id);
    var displaySetting = event.style.display;
    event.style.display = 'none';
}

function displayLatLng(Latitude, Longitude) {
    // Find the element where you want to display the latilongi value (e.g., by its ID)
    var displayElement = document.getElementById("latitudelongitude-display");
    console.log(Latitude, Longitude)
    // Check if the element exists
    if (displayElement) {
        displayElement.textContent = "Latitude: " + Latitude + ", Longitude: " + Longitude;
    }
}

window.initMap = initViewMap;




