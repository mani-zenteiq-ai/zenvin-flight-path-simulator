let map;
let flightMarkers = {};

function initMap() {
    map = L.map('map').setView([20.5937, 78.9629], 5); // India Center
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    updateFlights();
    setInterval(updateFlights, 1000); // Update every second
}

function updateFlights() {
    fetch('/api/flights')
        .then(response => response.json())
        .then(flights => {
            flights.forEach(flight => {
                const id = flight.Flight_ID;
                const lat = flight.Latitude;
                const lon = flight.Longitude;
                const popupText = `
                    <b>Flight ID:</b> ${flight.Flight_ID}<br>
                    <b>Origin:</b> ${flight.Origin_Country}<br>
                    <b>Altitude:</b> ${flight.Altitude} m<br>
                    <b>Velocity:</b> ${flight.Velocity} m/s<br>
                    <b>Heading:</b> ${flight.Heading}°<br>
                    <b>Vertical Rate:</b> ${flight.Vertical_Rate} m/s
                `;

                if (flightMarkers[id]) {
                    flightMarkers[id].setLatLng([lat, lon]);
                    flightMarkers[id].bindPopup(popupText);
                } else {
                    flightMarkers[id] = L.marker([lat, lon], { icon: L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/149/149059.png', iconSize: [20, 20] })})
                        .addTo(map)
                        .bindPopup(popupText);
                }
            });
        })
        .catch(error => console.error("Error fetching flight data:", error));
}

document.addEventListener("DOMContentLoaded", initMap);