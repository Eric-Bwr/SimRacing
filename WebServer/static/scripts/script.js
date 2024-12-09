const socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('updateSystemInfo', function (data) {
    const {cpu, ram} = data;
    const cpuProgress = document.getElementById('cpuProgress');
    const ramProgress = document.getElementById('ramProgress');

    cpuProgress.style.width = `${cpu}%`;
    ramProgress.style.width = `${ram}%`;
});

const map = L.map('map').setView([52.399858608592396, 7.8445644139198745], 19);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19}).addTo(map);

let marker = L.circleMarker([52.399858608592396, 7.8445644139198745], {
    radius: 3,
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.8
}).addTo(map);

const markerElement = marker._path;
if (markerElement) {
    markerElement.classList.add('blinking-marker');
}

let latlngs = [];

let polyline = L.polyline(latlngs, {color: 'blue'}).addTo(map);

map.on('click', function (e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;

    socket.emit('mapClick', {
        lat: lat,
        lon: lon
    });

    const wooshCircle = L.circleMarker([lat, lon], {
        color: '#666',
        fillColor: '#666',
        fillOpacity: 0.5,
        radius: 2,
        className: 'wooshCircle'
    }).addTo(map);

    let currentRadius = 2;
    let currentOpacity = 0.5;
    const growInterval = setInterval(() => {
        currentRadius += 1;
        currentOpacity -= 0.05;
        wooshCircle.setRadius(currentRadius);
        wooshCircle.setStyle({fillOpacity: currentOpacity});

        if (currentOpacity <= 0) {
            clearInterval(growInterval);
            map.removeLayer(wooshCircle);
        }
    }, 30);
});

let followMarker = true;

const followButton = document.getElementById('follow');

function updateFollowButton() {
    if (followMarker) {
        followButton.innerHTML = "<span style='color: green;'>⊕</span>";
    } else {
        followButton.innerHTML = "<span style='color: red;'>⊕</span>";
    }
}

document.getElementById('follow').addEventListener('click', function () {
    followMarker = !followMarker;
    updateFollowButton();
});

updateFollowButton();

socket.on('updateCoordinates', function (data) {
    const {lat, lon, alt, status, closestDistance} = data;

    latlngs.push([lat, lon]);
    if (latlngs.length > 100) {
        latlngs.shift();
    }

    marker.setLatLng([lat, lon]);

    polyline.setLatLngs(latlngs);
    updateWiFiStatus(status);

    if (followMarker) {
        map.setView([lat, lon]);
    }

    document.getElementById('lat').innerText = lat.toFixed(6);
    document.getElementById('lon').innerText = lon.toFixed(6);
    document.getElementById('alt').innerText = alt.toFixed(2);
    if (closestDistance != null) {
        document.getElementById('closestDistance').innerText = closestDistance.toFixed(2);
    }
});

function updateWiFiStatus(status) {
    const wifiSymbol = document.querySelector('.status');
    switch (status) {
        case -1: // STATUS_NO_FIX
            wifiSymbol.innerHTML = "<span style='color: #E00000;'>ᯤ</span>";
            break;
        case 0: // STATUS_FIX
            wifiSymbol.innerHTML = "<span style='color: #000000;'>ᯤ</span>";
            break;
        case 1: // STATUS_SBAS_FIX
            wifiSymbol.innerHTML = "<span style='color: #ffc40c;'>ᯤ</span>";
            break;
        case 2: // STATUS_GBAS_FIX
            wifiSymbol.innerHTML = "<span style='color: #009000;'>ᯤ</span>";
            break;
        default:
            wifiSymbol.innerHTML = "<span style='color: #FFFFFF;'>ᯤ</span>";
            break;
    }
}