/**
 * Created by Jingmei on 16/10/20.
 */

var circles=[];
var markers = [];
var map;
var latitude=0;
var longitude=0;

function initMap() {
   map = new google.maps.Map(document.getElementById('map'), {
             zoom: 5,
             center: {lat: 40.730610, lng: -73.935242}
        });
    google.maps.event.addListener(map, "click", function (event) {
        clearMarkers();
        clearCircles();
    latitude = event.latLng.lat();
    longitude = event.latLng.lng();
        $.post("/w/"+latitude+'_'+longitude, function(data){
            var marker = new google.maps.Marker({
            position: {lat: latitude, lng: longitude},
            map: map
            })
            markers.push(marker)
            tmp=JSON.parse(data);
            res=tmp.b
            //console.log(res.length)
            var circle = new google.maps.Circle({
              strokeColor: '#FF0000',
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: '#FF0000',
              fillOpacity: 0.35,
              map: map,
              center: {lat: latitude, lng: longitude},
              radius: 100000
            });
            circles.push(circle);
            for (var i = 0; i < res.length; i++) {
                    console.log(res[i]['geo'])
                    var marker = new google.maps.Marker({
                        position: {lat: res[i]['geo'][0], lng: res[i]['geo'][1]},
                        map: map
                    })
                    markers.push(marker)
                    var infowindow = new google.maps.InfoWindow( {maxWidth: 200})
                    //var content=res[i]['text']
                    var content=res[i]['user'].bold()+':</br>'+res[i]['text']
                    google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
                        return function () {
                            infowindow.setContent(content);
                            infowindow.open(map, marker);
                        };
                    })(marker, content, infowindow));
                }
        });
        });
}

function drop(value) {
    clearCircles()
    clearMarkers();
    var res=[];
    $.get("/q/"+value, function(data){
            tmp=JSON.parse(data);
            res=tmp.a
        //console.log(res.length)
            for (var i = 0; i < res.length; i++) {
                    console.log(res[i]['geo'])
                    var marker = new google.maps.Marker({
                        position: {lat: res[i]['geo'][0], lng: res[i]['geo'][1]},
                        map: map
                    })
                    markers.push(marker)
                    var infowindow = new google.maps.InfoWindow( {maxWidth: 200})
                    //var content=res[i]['text']
                    var content=res[i]['user'].bold()+':</br>'+res[i]['text']
                    google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
                        return function () {
                            infowindow.setContent(content);
                            infowindow.open(map, marker);
                        };
                    })(marker, content, infowindow));
                }

        });

}

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

function clearCircles() {
  for (var i = 0; i < circles.length; i++) {
    circles[i].setMap(null);
  }
  circles = [];
}
