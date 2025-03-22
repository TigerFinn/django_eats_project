var map;
var marker;

function initMap() {
    var defaultLocation = { lat: 55.86, lng: -4.25 };

    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultLocation,
        zoom: 12
    });

    marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        draggable: true
    });

    google.maps.event.addListener(marker, 'dragend', function() {
        var lat = marker.getPosition().lat();
        var lng = marker.getPosition().lng();

        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lng;
    });

    map.addListener('click', function(event) {
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();

        marker.setPosition(event.latLng);
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lng;
    });
}
