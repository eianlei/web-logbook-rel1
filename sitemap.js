let LeafletMap = null;

/**
Leaflet map 
**/

/**
 * parses DMS formatted coordinate to decimal
 * @param {*} input  60°2'31.19"N,19°53'52.31"E
 * @returns [60.04199722222222, 19.89786388888889]
 */
 function ParseDMS(input) {
  var parts = input.split(/[^\d\w\.]+/);  
  var lat = ConvertDMSToDD(parts[0], parts[1], parts[2], parts[3]);
  var lon = ConvertDMSToDD(parts[4], parts[5], parts[6], parts[7]);
  return [lat, lon];
}
function ConvertDMSToDD(degrees, minutes, seconds, direction) {
  var dd = Number(degrees) + Number(minutes)/60 + Number(seconds)/(60*60);

  if (direction == "S" || direction == "W") {
      dd = dd * -1;
  } // Don't do anything for N or E
  return dd;
}

function showMapTEST(div_id, lat, lon ){ //, id){
  console.log(div_id ,lat, lon) //, id);
  //var placeIndex = tablesMaps.Place[id];
  //var thisPlace = tables.Place[placeIndex];
  // viewChange("Map");
  if (LeafletMap == null){
    LeafletMap= new L.map(div_id).setView([lat, lon], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(LeafletMap);
  } else {
    LeafletMap.setView(new L.LatLng(lat, lon), 13);
  }
  /*
  var marker = L.marker([lat, lon]).addTo(LeafletMap);
  //marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
  marker.bindPopup(`<b>${id}</b><br>${thisPlace.Place}`).openPopup();
  */
}

/**
 * 
 */
function makeMapAllPlaces(all_places, div_id){
  let FirstPos = [60.1, 24.4];
  LeafletMap= new L.map(div_id).setView(FirstPos, 8);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(LeafletMap);

  // Icon options
    var iconOptions = {
      iconUrl: 'MapPinPlace.png',
      /*
      iconUrl: 'html/32px-Alfa_flag.svg.png',
      iconSize: [32, 32]
      */
    }
  // Creating a custom icon
    var divesite = L.icon(iconOptions);

    var scale = L.control.scale(); // Creating scale control
    scale.addTo(LeafletMap); // Adding scale control to the map

  //for(i=0; i< tables["Place"].length; i++) {
  for (let thisPlace of all_places)  {
    //var thisPlace = tables.Place[i];
    var lat, lon;
    if(thisPlace.Lat != null && thisPlace.Lon != null &&
      thisPlace.Lat != "" && thisPlace.Lon != "" ){
      var LatLon = `${thisPlace.Lat},${thisPlace.Lon}`;
      [lat, lon] = ParseDMS(LatLon);
      var markerOptions = {
        title:  `${LatLon}`, //`${thisPlace.Place}`,
        icon: divesite
      }
      var marker = L.marker([lat, lon], markerOptions).addTo(LeafletMap);
      marker.bindTooltip(`${thisPlace.Place}`, permanent=true).openTooltip();
      marker.bindPopup(`<b><u>${thisPlace.Place}</b></u><br>${lat.toFixed(4)}<br>${lon.toFixed(4)}<br><button onclick="showSiteDetails(${thisPlace.ID})">details</button>`+`
      <button onclick="zoomSite(${[lat, lon]}, ${thisPlace.ID})">zoom</button>`);
      thisPlace["marker"] = marker;
      thisPlace["LatLonArray"] = [lat, lon];
    }
  }
  LeafletMap.panTo(FirstPos);
  /*
  setTimeout(function () {
    LeafletMap.invalidateSize(true);
 }, 1000);*/
}

function showMap(LatLon, this_place_index){
  document.getElementById("MapButton").click()
  LeafletMap.setView(LatLon, 13);
  let this_place = places_summary[this_place_index]
  this_place.marker.openPopup();

}

function showSiteDetails(id){
  console.log("map site button ", id);
  show_place(id)
  document.getElementById("PlaceButton").click()
}

function zoomSite(lat, lon, id){
  //var placeIndex = tablesMaps.Place[id];
  //var thisPlace = tables.Place[placeIndex];
  LeafletMap.setView([lat, lon], 13);
  // thisPlace.marker.openPopup();
}

function showTripArea(maxNW, minSE){
    console.log("showTripArea", maxNW, minSE)
  //LeafletMap.flyToBounds(DBdata.getRowColByID("Trip", ID, "MapBounds"));
  LeafletMap.fitBounds([maxNW, minSE]);
  document.getElementById("MapButton").click()
  // L.flyToBounds(bounds);
}
