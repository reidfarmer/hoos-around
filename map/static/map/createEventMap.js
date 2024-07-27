// we did not end up using this file anywhere in the code
async function initCreateEventMap() {
    const mapElement = document.getElementById("map");
    
    if (!mapElement) {
        console.error("Map element not found.");
        return;
    }

    const map = new google.maps.Map(mapElement, {
        center: { lat: 38.03172018123903, lng: -78.51068497101028 },
        zoom: 15,
        styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }] // Hide points of interest labels
            }
          ]
    });

    const approvedEventsElement = document.getElementById("approvedEvents");
    
    if (!approvedEventsElement) {
        console.error("Approved events element not found.");
        return;
    }

    const eventsJson = approvedEventsElement.getAttribute("data-events");

    if (!eventsJson) {
        console.error("No approved events data.");
        return;
    }

    try {
        const events = JSON.parse(eventsJson);

        for (const event of events) {
            const eventFields = event.fields;
            const latitude = parseFloat(eventFields.latitude);
            const longitude = parseFloat(eventFields.longitude);
            const approved = eventFields.approved;

            if (!isNaN(latitude) && !isNaN(longitude) && approved) {
                addMarker({ lat: latitude, lng: longitude }, map);
            }
        }
    } catch (error) {
        console.error("Error parsing approved events JSON:", error);
    }
}

function addMarker(location, map) {
    const marker = new google.maps.Marker({
        position: location,
        map: map,
    });
    return marker;
}

window.initCreateEventMap = initCreateEventMap;

