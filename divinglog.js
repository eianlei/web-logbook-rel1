/* 2025-10-21 divinglog.js
web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"

The file contains JavaScript functions to handle map display, navigation, 
and gallery features for a web-based scuba diving logbook application.
**********************************************************************************/

// handle URL parameters, TODO: take these into account when loading the page
const queryString = window.location.search;
console.log(`queryString= ${queryString}`);
const urlParams = new URLSearchParams(queryString);
var view2load = urlParams.get('view')
console.log(`file= ${view2load}`);
var id2show = urlParams.get('id')
console.log(`id= ${id2show}`);

// global variables
var logbook_list = []
var places_summary = []
var currently_shown_dive = 0
var lastDiveNumber = 0
var currently_shown_trip = 0
var currently_shown_place = 0
var currently_shown_buddy = 0
var currently_shown_equipment = 0
var gallery = []
var gallery_indexes = []

// load about.html into About tab
fetch('about.html')
  .then(response => response.text())
  .then(data => {  
    document.getElementById('about_container').innerHTML = data;
  })
  .catch(error => {
    console.error('Error loading about.html:', error);
    document.getElementById('about_container').innerHTML = "<p>Error loading about.html</p>";
  });   

// load summary tables, json files are in /json/ folder
// then generate HTML table rows
url = window.location.origin + '/json/Logbook_summary.json';
generateHtmlTableRows("logbook_table", url);
url = window.location.origin + '/json/Trip_summary.json';
generateHtmlTableRows("trip_table", url);
url = window.location.origin + '/json/Place_summary.json';
generateHtmlTableRows("place_table", url);    
url = window.location.origin + '/json/Buddy_summary.json';
generateHtmlTableRows("buddy_table", url);    
url = window.location.origin + '/json/Equipment_summary.json';
generateHtmlTableRows("equipment_table", url);
url = window.location.origin + '/json/Brevets_summary.json';
generateHtmlTableRows("brevets_table", url);

// if gallery use is disabled, hide Photos button
if (typeof GALLERY_USE === 'undefined' || GALLERY_USE === false){
  console.log("Gallery use is disabled");
  document.getElementById("PhotosButton").style.display = "none";
} else {
  console.log("Gallery use is enabled");
  url = window.location.origin + '/json/gallery.json'; 
  get_gallery(url);
} 
 

function get_gallery(url){
  loadJSON(url).then(data => {
    gallery = data;
    gallery_indexes  = gallery.map(item => item.ID).sort((a, b) => a - b);
    console.log('gallery loaded') 
  });
}

async function loadJSON(url) {
  console.log(`start fetch for "${url}"`);
  const response = await fetch(url)
  const data = await response.json()
  return data 
}

// Listen for back/forward navigation
window.addEventListener('popstate', (event) => {
  // Handle route change in your SPA
  console.log('Navigated to:', window.location.pathname, " ", window.location.search);
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  var view2load = urlParams.get('view')
  document.getElementById(view2load + "Button").click();
});


// create navigation    
function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  console.log("activate tab ", tabName )
  
/*
  if (id2show != null && tabName == 'Dive' ){
    history.pushState(null, '', `app?view=${tabName}&id=${currently_shown_dive}`);
  } else {
    history.pushState(null, '', `app?view=${tabName}`);
  }
*/
  
  /*
  if (tabName == 'Logbook'){
  
    console.log("scroll to ", rowIndex)
  } else */
  if (tabName == 'Map'){
    LeafletMap.invalidateSize(true);
  }
  
}
// resizers
  const resizers = document.querySelectorAll('.resizer');

  resizers.forEach((resizer) => {
    let prevPane = resizer.previousElementSibling;
    let nextPane = resizer.nextElementSibling;
    let isResizing = false;

    resizer.addEventListener('mousedown', () => {
      isResizing = true;
      document.body.style.cursor = 'col-resize';

      const onMouseMove = (e) => {
        if (!isResizing) return;

        const container = resizer.parentElement;
        const containerWidth = container.offsetWidth;
        const newPrevWidth = e.clientX - container.offsetLeft;
        const newPrevPercent = (newPrevWidth / containerWidth) * 100;

        prevPane.style.flexBasis = `${newPrevPercent}%`;
        nextPane.style.flexBasis = `${100 - newPrevPercent}%`;
      };

      const onMouseUp = () => {
        isResizing = false;
        document.body.style.cursor = 'default';
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  });



function gotoTab(tab, id=null){
  if (id == null){
        alert("null id given for tab " + tab);
        return;
  }
  switch (tab) {
    // note that tab names start with Capital letter, but table names are lower case
    // buttons are SnakeCase + "Button"
    case "Place":
      loadTableData(id, "place");
      document.getElementById("PlaceButton").click();
      break;
    case "Map":
      var place_number = id
      let this_place_index = places_summary.findIndex(x => x.ID == place_number);
      let this_place = places_summary[this_place_index];
      let LatLon = this_place.LatLonArray;
      showMap(LatLon, this_place_index );
      break;
    case "Buddy":
      loadTableData(id, "buddy");
      document.getElementById("BuddyButton").click();
      break;
    case "Trip":
      loadTableData(id, "trip");
      document.getElementById("TripButton").click();
      break;
    default:
      alert("unknown tab " + tab);
      return;
  }
}

function showTripFromPlace(TripID){
  show_trip(TripID);
  document.getElementById("TripButton").click();
}





function prevLog(){
  var index = logbook_list.indexOf(currently_shown_dive);
  if(index >= 1 ) {
    prevItem = logbook_list[index - 1]
    document.getElementById('dlogGotoNumber').value = prevItem;
    link_dive(prevItem)  
  } else {
    alert("Already at first dive, there is no previous")
  }
}
function nextLog(){
  var index = logbook_list.indexOf(currently_shown_dive);
  if(index >= 0 && index < logbook_list.length - 1){
    nextItem = logbook_list[index + 1]
    document.getElementById('dlogGotoNumber').value = nextItem;
    link_dive(nextItem)
  } else {
    alert("Already at last dive, there is no next")
  }
}
function lastLog(){
    document.getElementById('dlogGotoNumber').value = lastDiveNumber;
    link_dive(lastDiveNumber)  
}

function dlogGotoNumber(){
  let reqNum = Number(document.getElementById("dlogGotoNumber").value);
  if (reqNum > lastDiveNumber){
    alert(`requested number ${reqNum} > ${lastDiveNumber}`);
    return;
  }
  link_dive(reqNum)
}

function makePNG(){
  /*
    var w = window.innerWidth;
    var h = window.innerHeight;
    window.open(`/profile_png/${currently_shown_dive}?width=${w}&height=${h}`, '_blank')
  */
  var w = 1000
  var h = 600
  window.open(`/profile_png/${currently_shown_dive}?width=${w}&height=${h}`, 
      'dive profile', `width=${w},height=${h},menubar=1,titlebar=1`)
}
function makeSVG(){
  var w = 1000
  var h = 600
  window.open(`/profile_svg/${currently_shown_dive}?width=${w}&height=${h}&file=4`, 
      'dive profile', `width=${w},height=${h},menubar=1,titlebar=1`)
}
function makeHTML(){
  var w = 1000
  var h = 800
  window.open(`/divelog_html/${currently_shown_dive}`, //?width=${w}&height=${h}`, 
      'dive profile', `width=${w},height=${h},menubar=1,titlebar=1,scrollbars=1`)
}
function galleryNumber(){
  let num = Number(document.getElementById("galleryNumber").value);
  console.log("Request gallery for dive ", num ) 
  if (gallery_indexes.includes(num)){
    show_gallery(num)
  } else {
    alert(`dive number ${num} has no media`);
    return;
  }
}

var current_g = {}

function show_gallery(num){
    document.getElementById('gallery_h2').innerHTML = `Dive ${num}`
    document.getElementById('galleryNumber').value = num;
    document.getElementById('gallery_container').innerHTML = "<h2>fetching data</h2><div class='loader'></div>";

    current_g = gallery.find(x => x.ID == num);
    console.log(current_g.Url);
    document.getElementById('gallery_h2').innerHTML = `Dive ${num} ${current_g.Date} ${current_g.Sitename}`
    html1 = `<iframe src="${current_g.Url}/embed?thumbstrip=1&bgcolor=1&captions=1" `
    html2 = "width='100%' height='746' frameborder='0' webkitallowfullscreen mozallowfullscreen allowfullscreen scrolling='no'></iframe>"
    document.getElementById('gallery_container').innerHTML =  html1 + html2

}
function gotoGallery(){
  num = Number(currently_shown_dive)
  console.log("Request gallery for dive ", num ) 
  if (gallery_indexes.includes(num)){
    show_gallery(num)
    document.getElementById("PhotosButton").click()
  } else {
    alert(`dive number ${num} has no media`);
    return;
  }  
}

function newGalleryPage(){
  var w = 1000
  var h = 800
  window.open(current_g.Url, 'dive photos', `width=${w},height=${h}`)
}

function show_place(place_number){
  loadTableData(place_number, "place");
  document.getElementById("PlaceButton").click();
}

/////// this always gets executed after loading the page
async function init_page(){
  url = window.location.origin + '/logbook_list/';
  loadJSON(url).then(list => {
    logbook_list = list
    lastDiveNumber = logbook_list[logbook_list.length -1]
    console.log('logbook_list loaded, last dive is:', lastDiveNumber ) 
    currently_shown_dive = Number(lastDiveNumber);

    if (view2load == null){
      show_dive(currently_shown_dive, false)
      view2load = 'Logbook';
      document.getElementById("LogbookButton").click();
    } else {
      if (id2show != null){
        console.log("show view ", view2load, " id ", id2show)
        switch (view2load){
          case 'Dive':
            currently_shown_dive = Number(id2show);
            break
          case 'Trip':
            show_trip(id2show)
            break
          case 'Place':
            show_place(id2show)
            break
          case 'Buddy':
            show_buddy(id2show)
            break
          case 'Equipment':
            show_equipment(id2show)
            break  
          case 'Brevets':
            show_brevets(id2show);
            break 
          default:
            break
        }
      } else {
        console.log("no dive id given, show last dive")
      }
      show_dive(currently_shown_dive, false)
      document.getElementById(view2load + "Button").click();
    }
  });
}
//init_page();
console.log("init_page called")
 
// end