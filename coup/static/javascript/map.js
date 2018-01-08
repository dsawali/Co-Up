function initMap() {
    var lat_lng = { lat: 49.267132, lng: -122.968941 };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: lat_lng
    });
    var marker = new google.maps.Marker({
        position: lat_lng,
        map: map,
    });
    var infoWindow = new google.maps.InfoWindow({
        content: '8888 University Dr, Burnaby, BC V5A 1S6'
    });
    var searchField = new google.maps.places.Autocomplete(
        document.getElementById('id_location_addr'),
        { types: ['establishment', 'neighborhood', 'street_address', 'street_number'] }
    );
    var geocoder = new google.maps.Geocoder;
    
    marker.setMap(map);
    infoWindow.open(map, marker);

    map.addListener('click', function(event) {
        var latlng = event.latLng;
        var lat = latlng.lat();
        var lng = latlng.lng();

        marker.setPosition(latlng);
        geocoder.geocode({'location': latlng}, function(results, status) {
            if (status == 'OK'){
                var addr = results[0].formatted_address;
                marker.setMap(map);
                infoWindow.setContent(addr);
                $('input#id_location_lat').val(lat);
                $('input#id_location_lng').val(lng);
                $('input#id_location_addr').val(addr);
            }
        });
    });

    searchField.bindTo('bounds', map);
    searchField.addListener('place_changed', function() {
        var company_addr = searchField.getPlace().formatted_address;
        var company_loc = searchField.getPlace().geometry.location;
        var lat = company_loc.lat();
        var lng = company_loc.lng();
        
        marker.setPosition(company_loc);
        marker.setMap(map);
        infoWindow.setContent(company_addr);
        $('input#id_location_lat').val(lat);
        $('input#id_location_lng').val(lng);
    });
    
    $('button#positions').on('click', function() {
        setTimeout(function(){google.maps.event.trigger(map, "resize");}, 100);
    });
}



