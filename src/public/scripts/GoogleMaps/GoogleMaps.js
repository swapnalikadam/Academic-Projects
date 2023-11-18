var curLat = null; //user location
var curLon = null;

var placeMarkers = [];
  var input;
  var searchBox;
  var curposdiv;
  var curseldiv;

var isSelected= false;
var currShape ;



var drawingManager;
      var selectedShape;
      var colors = ['#1E90FF', '#FF1493', '#32CD32', '#FF8C00', '#4B0082'];
      var selectedColor;
      var colorButtons = {};

      function clearSelection() {
        if (selectedShape) {
          if (typeof selectedShape.setEditable == 'function') {
            selectedShape.setEditable(false);
            isSelected = false
          }
          selectedShape = null;
        }
        //curseldiv.innerHTML = "<b>cursel</b>:";
      }

      function updateCurSelText(shape) {
        posstr = "" + selectedShape.position;
        if (typeof selectedShape.position == 'object') {
          posstr = selectedShape.position.toUrlValue();
        }
        pathstr = "" + selectedShape.getPath;
        if (typeof selectedShape.getPath == 'function') {
          pathstr = [];
          for (var i = 0; i < selectedShape.getPath().getLength(); i++) {
            const coordinate = selectedShape.getPath().getAt(i).toUrlValue();
            // .toUrlValue(5) limits number of decimals, default is 6 but can do more
            pathstr.push({x : coordinate.split(",")[0], y: coordinate.split(",")[1], });
          }   
          document.getElementById("locationString").value = JSON.stringify(pathstr);
        }
        bndstr = "" + selectedShape.getBounds;
        cntstr = "" + selectedShape.getBounds;
        if (typeof selectedShape.getBounds == 'function') {
          var tmpbounds = selectedShape.getBounds();
          cntstr = "" + tmpbounds.getCenter().toUrlValue();
          bndstr = "[NE: " + tmpbounds.getNorthEast().toUrlValue() + " SW: " + tmpbounds.getSouthWest().toUrlValue() + "]";
        }
        cntrstr = "" + selectedShape.getCenter;
        if (typeof selectedShape.getCenter == 'function') {
          cntrstr = "" + selectedShape.getCenter().toUrlValue();
        }
        radstr = "" + selectedShape.getRadius;
        if (typeof selectedShape.getRadius == 'function') {
          radstr = "" + selectedShape.getRadius();
        }
        //curseldiv.innerHTML = "<b>cursel</b>: " + selectedShape.type + " " + selectedShape + "; <i>pos</i>: " + posstr + " ; <i>path</i>: " + /*pathstr.map(x=> x.join(","))*/pathstr + " ; <i>bounds</i>: " + bndstr + " ; <i>Cb</i>: " + cntstr + " ; <i>radius</i>: " + radstr + " ; <i>Cr</i>: " + cntrstr ;
      }

      function setSelection(shape, isNotMarker) {
        console.log("selected",shape);
       
        clearSelection();
        selectedShape = shape;
        if (isNotMarker){
          shape.setEditable(true);
          isSelected = true;
          debugger;
        }
        selectColor(shape.get('fillColor') || shape.get('strokeColor'));
        updateCurSelText(shape);

      }

      function deleteSelectedShape() {
      
        
        if(selectedShape){
          selectedShape.setMap(null);
          isSelected = false;
          selectedShape=null;
        }
       
      }

      function selectColor(color) {
        selectedColor = color;
        for (var i = 0; i < colors.length; ++i) {
          var currColor = colors[i];
          colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
        }

        // Retrieves the current options from the drawing manager and replaces the
        // stroke or fill color as appropriate.
        // var polylineOptions = drawingManager.get('polylineOptions');
        // polylineOptions.strokeColor = color;
        // drawingManager.set('polylineOptions', polylineOptions);

        // var rectangleOptions = drawingManager.get('rectangleOptions');
        // rectangleOptions.fillColor = color;
        // drawingManager.set('rectangleOptions', rectangleOptions);

        // var circleOptions = drawingManager.get('circleOptions');
        // circleOptions.fillColor = color;
        // drawingManager.set('circleOptions', circleOptions);

        // var polygonOptions = drawingManager.get('polygonOptions');
        // polygonOptions.fillColor = color;
        // drawingManager.set('polygonOptions', polygonOptions);
      }

      function setSelectedShapeColor(color) {
        if (selectedShape) {
          if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
          } else {
            selectedShape.set('fillColor', color);
          }
        }
      }

      function makeColorButton(color) {
        var button = document.createElement('span');
        button.className = 'color-button';
        button.style.backgroundColor = color;
        google.maps.event.addDomListener(button, 'click', function() {
          selectColor(color);
          setSelectedShapeColor(color);
        });

        return button;
      }

       function buildColorPalette() {
         var colorPalette = document.getElementById('color-palette');
         for (var i = 0; i < colors.length; ++i) {
           var currColor = colors[i];
           var colorButton = makeColorButton(currColor);
           colorPalette.appendChild(colorButton);
           colorButtons[currColor] = colorButton;
         }
         selectColor(colors[0]);
       }

function getLocation() {
  //console.log("Navigation&&&&&&&&&&&&",navigator.geolocation);
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
        window.alert("no location");
    }
}
function showPosition(position) {
    curLat = position.coords.latitude;
    curLon = position.coords.longitude;
}
function initMap(){
  getLocation() //finds out user location to fomat the map
  //console.log("SearchResult",searchResult);
  if (curLat == null){
    //curLat = 42.3601;   //if the user location cannot be found, set default ones
    //curLon = -71.0589;   // of boston
    curLat = -1.142307;   //if the user location cannot be found, set default ones
    curLon = -53.370157;
    console.log("random locations");
  }
  var options = {
    zoom:6,
    center:{lat:curLat, lng:curLon},
    disableDefaultUI: false, //added now
    zoomControl: true,
    mapTypeControl: true,
    // mapTypeControlOptions: {
    //   style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
    //   mapTypeIds: ["roadmap", "terrain"],
    // },
    keyboardShortcuts : false,
    mapTypeId: google.maps.MapTypeId.ROADMAP //added now
  }

  //Marker functionality Not Required
  /*var geocoder;
  var bounds = new google.maps.LatLngBounds();
  var locations = [
    ['Location 1 Name', 'New York, NY', 'Location 1 URL'],
    ['Location 2 Name', 'Newark, NJ', 'Location 2 URL'],
    ['Location 3 Name', 'Philadelphia, PA', 'Location 3 URL'],
    ['Location 4 Name', 'Toronto, ON', 'Location 4 URL'],
    ['Location 5 Name', 'St John\'s, NL', 'Location 5 URL'],
];
  geocoder = new google.maps.Geocoder();

    for (i = 0; i < locations.length; i++) {


        geocodeAddress(locations, i);
    }

    function geocodeAddress(locations, i) {
      //var title = locations[i][0];
      var address = locations[i][1];
      //var url = locations[i][2];
      geocoder.geocode({
          'address': locations[i][1]
      },
  
      function (results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
              var marker = new google.maps.Marker({
                  icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                  //icon: 'http:// google.com/mapfiles/ms/micons/orange-dot.png',
                  map: map,
                  position: results[0].geometry.location,
                  //title: title,
                  animation: google.maps.Animation.DROP,
                  address: address,
                  //url: url
              })
              //infoWindow(marker, map, title, address, url);
              infoWindow(marker, map, address);
              bounds.extend(marker.getPosition());
              map.fitBounds(bounds);
          } else {
              alert("geocode of " + address + " failed:" + status);
          }
      });
  }

  /*function infoWindow(marker, map, title, address, url) {
    google.maps.event.addListener(marker, 'click', function () {
        var html = "<div><h3>" + title + "</h3><p>" + address + "<br></div><a href='" + url + "'>View location</a></p></div>";
        iw = new google.maps.InfoWindow({
            content: html,
            maxWidth: 350
        });
        iw.open(map, marker);
    });*/
/*
    function infoWindow(marker, map, address) {
      google.maps.event.addListener(marker, 'click', function () {
          var html = "<div><p>" + address + "<br></div></p></div>";
          iw = new google.maps.InfoWindow({
              content: html,
              maxWidth: 350
          });
          iw.open(map, marker);
      });
}

function createMarker(results) {
  var marker = new google.maps.Marker({
      icon: 'http://maps.google.com/mapfiles/ms/icons/blue.png',
      map: map,
      position: results[0].geometry.location,
      title: title,
      animation: google.maps.Animation.DROP,
      address: address,
      url: url
  })
  bounds.extend(marker.getPosition());
  map.fitBounds(bounds);
  infoWindow(marker, map, title, address, url);
  return marker;
}
*/
//Marker functionality ends

  //bounds.extend(marker.getPosition());
  //map.fitBounds(bounds);
  //infoWindow(marker, map, title, address, url);
 

  function deletePlacesSearchResults() {
    for (var i = 0, marker; marker = placeMarkers[i]; i++) {
      marker.setMap(null);
    }
    placeMarkers = [];
    input.value = ''; // clear the box too
  }

  var map = new google.maps.Map(document.getElementById("map"),options);
  //addMarker({lat:42.4668,lng:-70.94});
  /*var markers = [{
    "decimallatitude": '15.73278',
    "decimallongitude": '-87.58972'
  },{"decimallatitude": '8.97722',
  "decimallongitude": '-83.04389'}];*/

  /*for (i=0; i < markers.length; i++){
    markers[i].decimallatitude = parseFloat(data[i].year, 10)
    markers[i].decimallongitude = parseFloat(data[i].total, 10)
}*/

  /*var locations = markers.map(function(o, i) {
    return [
      i == 0 ? 'Start' : i == markers.length - 1 ? 'End' : i,
      o.decimallatitude,
      o.decimallongitude,
      i + 1
    ]
  });*/

  var addMarker = function (results) {
    //console.log("Results",results);
    var marker = new google.maps.Marker({
      icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
      map: map,
      //position: {lat:42.4668,lng:-70.94},
      //position: results,
      position: {lat: parseFloat(results.decimallatitude),lng: parseFloat(results.decimallongitude)},
      //title: title,
      animation: google.maps.Animation.DROP,
      //address: address,
      //url: url
    });
    //console.log('resuts:',results);
      var infoWindow = new google.maps.InfoWindow({
        //content: {
          //"latitude": parseFloat(results.decimallatitude),
          //"longitude": parseFloat(results.decimallongitude)
        //}
      });

    marker.addListener('click', function(){
      var lat = parseFloat(results.decimallatitude);
      var lng = parseFloat(results.decimallongitude);
      infoWindow.setContent('<h5> latitude =' + lat + ', longitude=' + lng + '</h5>');
      infoWindow.open(map,marker);
    });
  }
  /*for (i = 0; i < markers.length; i++) {
    console.log("Markers",markers[i]);
    addMarker(markers[i]);
}*/

  window.addMarker = addMarker;

  curposdiv = document.getElementById('curpos');
  curseldiv = document.getElementById('cursel');

  var polyOptions = {
    strokeWeight: 0,
    fillOpacity: 0.45,
    editable: true
  };
  // Creates a drawing manager attached to the map that allows the user to draw
  // markers, lines, and shapes.
  drawingManager = new google.maps.drawing.DrawingManager({
    //drawingMode: google.maps.drawing.OverlayType.POLYGON,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.POLYGON,
        google.maps.drawing.OverlayType.POLYLINE,
      ],
    },
    markerOptions: {
      draggable: true,
      editable: true,
    },
    polylineOptions: {
      editable: true
    },
    //rectangleOptions: polyOptions,
    //circleOptions: polyOptions,
    //polygonOptions: polyOptions,
    map: map
  });

  google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
    //~ if (e.type != google.maps.drawing.OverlayType.MARKER) {
      var isNotMarker = (e.type != google.maps.drawing.OverlayType.MARKER);
      // Switch back to non-drawing mode after drawing a shape.
      drawingManager.setDrawingMode(null);

      // Add an event listener that selects the newly-drawn shape when the user
      // mouses down on it.
      var newShape = e.overlay;
      newShape.type = e.type;
      google.maps.event.addListener(newShape, 'click', function() {
        setSelection(newShape, isNotMarker);
      });
      google.maps.event.addListener(newShape, 'drag', function() {
        updateCurSelText(newShape);
      });
      google.maps.event.addListener(newShape, 'dragend', function() {
        updateCurSelText(newShape);
      });
      setSelection(newShape, isNotMarker);
    //~ }// end if
  });

  // remove a rectangle if other rectangl is drawn

//   google.maps.event.addListener(drawingManager, "drawingmode_changed", function() {
//     if ((drawingManager.getDrawingMode() == google.maps.drawing.OverlayType.POLYGON) && (rectangle != null))
//         rectangle.setMap(null);
// });

  // Clear the current selection when the drawing mode is changed, or when the
        // map is clicked.
        google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
        google.maps.event.addListener(map, 'click', clearSelection);
        // google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);

        buildColorPalette();

        //~ initSearch();
        // Create the search box and link it to the UI element.
        //  input = /** @type {HTMLInputElement} */( //var
        //     document.getElementById('pac-input'));
        // map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);

        // Delete button for selected results
        // var DelPlcButDiv = document.createElement('div');
        // //~ DelPlcButDiv.style.color = 'rgb(25,25,25)'; // no effect?
        // DelPlcButDiv.style.backgroundColor = '#fff';
        // DelPlcButDiv.style.cursor = 'pointer';
        // DelPlcButDiv.innerHTML = 'DEL';
        // map.controls[google.maps.ControlPosition.TOP_RIGHT].push(DelPlcButDiv);
        // google.maps.event.addDomListener(DelPlcButDiv, 'click', deletePlacesSearchResults);

      
        
        var DelShapeDiv = document.createElement('div');
        DelShapeDiv.style.backgroundColor = '#007fff';
        DelShapeDiv.style.margin = "10px";
        DelShapeDiv.style.padding = "5px";
        DelShapeDiv.style.cursor = 'pointer';
        DelShapeDiv.innerHTML ='DELETE SHAPE';
        DelShapeDiv.display= 'block';
        DelShapeDiv.position=  'absolute';
        DelShapeDiv.style.height = "30px";
        DelShapeDiv.style.width = "90px";
        DelShapeDiv.style.color = "white";
        map.controls[google.maps.ControlPosition.TOP_RIGHT].push(DelShapeDiv);
        google.maps.event.addDomListener(DelShapeDiv, 'click', deleteSelectedShape);
    

        searchBox = new google.maps.places.SearchBox( //var
          /** @type {HTMLInputElement} */(input));

        // Listen for the event fired when the user selects an item from the
        // pick list. Retrieve the matching places for that item.
        google.maps.event.addListener(searchBox, 'places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
          for (var i = 0, marker; marker = placeMarkers[i]; i++) {
            marker.setMap(null);
          }

          // For each place, get the icon, place name, and location.
          placeMarkers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {
            var image = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            var marker = new google.maps.Marker({
              map: map,
              icon: image,
              title: place.name,
              position: place.geometry.location
            });

            placeMarkers.push(marker);

            bounds.extend(place.geometry.location);
          }

          map.fitBounds(bounds);
        });

        // Bias the SearchBox results towards places that are within the bounds of the
        // current map's viewport.
        google.maps.event.addListener(map, 'bounds_changed', function() {
          var bounds = map.getBounds();
          searchBox.setBounds(bounds);
          //curposdiv.innerHTML = "<b>curpos</b> Z: " + map.getZoom() + " C: " + map.getCenter().toUrlValue();
        }); //////////////////////
      }
      //google.maps.event.addDomListener(window, 'load', initMap);

    


