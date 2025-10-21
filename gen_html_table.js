/* web-logbook, digital scuba diving logbook to web
__author__ = "Ian Leiman"
__copyright__ = "Copyright 2025, Ian Leiman"
__license__ = "CC BY-NC-SA 4.0"
__version__ = "rel1 0.1"
__email__ = "ian.leiman@gmail.com"
__status__ = "development"
*/
// gen_html_table.js

// Function to generate HTML table rows from an array of objects or fetch from a URL
// and insert into a specified div element.
async function generateHtmlTableRows(targetDivId, dataOrUrl) {
    let data = [];
    let table_id = `${targetDivId}_t`;

    // Check if dataOrUrl is a string (assume URL), else use as array
    if (typeof dataOrUrl === 'string') {
        const response = await fetch(dataOrUrl);
        data = await response.json();
    } else if (Array.isArray(dataOrUrl)) {
        data = dataOrUrl;
    } else {
        throw new Error('Second argument must be an array or a URL string');
    }

    if (!Array.isArray(data) || data.length === 0) {
        document.getElementById(targetDivId).innerHTML = '<p>No data available</p>';
        return;
    }

    // Get table headers from keys of first object
    const headers = Object.keys(data[0]);
    let tableHtml = `<table id='${table_id}'><thead><tr>`;
    headers.forEach(h => {
        tableHtml += `<th>${h}</th>`;
    });
    tableHtml += '</tr></thead><tbody>';

    if (table_id === 'place_table_t') {
        places_summary = data;
        makeMapAllPlaces(places_summary, "sitemap")
    }
    // Generate table rows
    data.forEach(row => {
        tableHtml += '<tr>';
        headers.forEach(h => {
            tableHtml += `<td>${row[h]}</td>`;
        });
        tableHtml += '</tr>';
        if (table_id === 'logbook_table_t') {
            logbook_list.push(Number(row[headers[0]])); 
        }
    });
    logbook_list.sort((a, b) => a - b);
    lastDiveNumber = logbook_list[logbook_list.length -1];
    tableHtml += '</tbody></table>';

    document.getElementById(targetDivId).innerHTML = tableHtml;
    setupTableInteractions(table_id, (firstCellValue) => {
        console.log(`${table_id} Row clicked, first cell value: ${firstCellValue}`);
        switch (table_id) {
            case 'logbook_table_t':
                loadDiveData(firstCellValue);  
                document.getElementById("DiveButton").click(); // Switch to Dive tab
                break;   
            // Add more cases as needed for other tables            
            case 'place_table_t':
                loadTableData(firstCellValue, 'place');  
                break

            case 'trip_table_t':
                loadTableData(firstCellValue, 'trip');  
                break;   
            case 'equipment_table_t':
                loadTableData(firstCellValue, 'equipment');  
                break;
            case 'buddy_table_t':
                loadTableData(firstCellValue, 'buddy');  
                break;
            case 'brevets_table_t':
                loadTableData(firstCellValue, 'brevets');  
                break;
            default:
                break;   
        }
    });
}

function link_dive(number) {
    loadDiveData(number);  
    document.getElementById("DiveButton").click(); // Switch to Dive tab
}

function loadTableData(id, table) {
    url = window.location.origin + `/html/${table}_${id}.html`;
    console.log(`Loading data for ${table} ID: ${id} from URL: ${url}`);
    loadHtmlIntoElement(url, `${table}_data`);
}

/*
function loadPlaceData(placeId) {
    url = window.location.origin + `/html/place_${placeId}.html`;
    console.log(`Loading data for place ID: ${placeId} from URL: ${url}`);
    loadHtmlIntoElement(url, 'place_data');
}

function loadTripData(tripId) {
    url = window.location.origin + `/html/trip_${tripId}.html`;
    console.log(`Loading data for trip ID: ${tripId} from URL: ${url}`);
    loadHtmlIntoElement(url, 'trip_data');
}
*/

var svg = null;
var vline = null;
var hline = null;
var coordText = null;
var depth_points = [];

function loadDiveData(number) {
    currently_shown_dive = Number(number);

    url = window.location.origin + `/html/dive_${number}.html`;
    console.log(`Loading data for Dive: ${number} from URL: ${url}`);
    loadHtmlIntoElement(url, 'dive_data', true).then(() => {
  
    waitForElement(`#svg_profile_${number}`, (svgElement) => {

        svg = document.getElementById(`svg_profile_${number}`);
        if (!svg ) {
            console.log("SVG for" + number + "not found, skipping mouse tracker setup");
            return;
        }
        // Clear previous event listener if any
        svg.replaceWith(svg.cloneNode(true)); 
        svg = document.getElementById(`svg_profile_${number}`); // Re-fetch the new element
        vline = document.getElementById("svg_vline");
        hline = document.getElementById("svg_hline");
        coordText = document.getElementById("svg_coordText");
        svg.addEventListener("mousemove", (e) => mouse_tracker(e));
        console.log("SVG mouse tracker set up for dive ", number);
        document.getElementById('dlogGotoNumber').value = currently_shown_dive;
        /*
        svg.addEventListener("mousemove", (e) => {
            const pt = svg.createSVGPoint();
            pt.x = e.clientX;
            pt.y = e.clientY;
            const cursor = pt.matrixTransform(svg.getScreenCTM().inverse());
            try {
                const nearest = getNearestPoint(cursor.x, cursor.y);
                // Update crosshair lines
                vline.setAttribute("x1", nearest.x);
                vline.setAttribute("x2", nearest.x);
                hline.setAttribute("y1", nearest.y);
                hline.setAttribute("y2", nearest.y);
                
                // Update coordinate text
                const time = nearest.t
                const depth = nearest.d
                coordText.textContent = `time: ${time.toFixed(1)}, depth: ${depth.toFixed(1)}`;
            } catch (error) {
                console.error("Error in mouse_tracker:", error);
            }
        }); 
        */
    });
    });
}


function waitForElement(selector, callback) {
  const element = document.querySelector(selector);
  if (element) {
    callback(element);
  } else {
    setTimeout(() => waitForElement(selector, callback), 100);
  }
}



// Function to set up click event handler for table rows
// Highlights the clicked row and calls the callback with the first cell's value
function setupDynamicRowClickHandler(tableId, callback) {
  const table = document.getElementById(tableId);
  if (!table) return;

  // Delegate click event to the table
  table.addEventListener('click', function (event) {
    let row = event.target.closest('tr');
    if (!row || !row.cells.length) return;

    // Remove highlight from all rows
    Array.from(table.getElementsByTagName('tr')).forEach(r => {
      r.classList.remove('highlight');
    });

    // Add highlight to clicked row
    row.classList.add('highlight');

    // Call the callback with the first cell's value
    callback(row.cells[0].textContent.trim());
  });
}

async function loadHtmlIntoElement(url, elementId, loadScripts = false) {
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to load HTML: ${response.status}`);
      }
      return response.text();
    })
    .then(html => {
      const targetElement = document.getElementById(elementId);
      if (targetElement) {
        if (loadScripts) { 
            // Create a temporary container to parse HTML
            const temp = document.createElement('div');
            temp.innerHTML = html;

            // Extract and execute scripts
            const scripts = temp.querySelectorAll('script');
            scripts.forEach(script => {
            const newScript = document.createElement('script');
            if (script.src) {
                newScript.src = script.src;
            } else {
                newScript.textContent = script.textContent;
            }
            document.body.appendChild(newScript);
            });
            targetElement.innerHTML = temp.innerHTML ;
        } else {
            targetElement.innerHTML = html;
        }
      } else {
        console.error(`Element with ID "${elementId}" not found.`);
      }
    })
    .catch(error => {
      console.error("Error loading HTML:", error);
    });
}

function setupTableInteractions(tableId, rowCallback) {
  const table = document.getElementById(tableId);
  if (!table) return;

  let sortDirections = {}; // Track sort direction per column

  table.addEventListener('click', function (event) {
    const cell = event.target.closest('td, th');
    const row = event.target.closest('tr');

    if (!cell || !row) return;

    const isHeader = cell.tagName === 'TH';
    const columnIndex = cell.cellIndex;

    if (isHeader) {
      // Toggle sort direction
      sortDirections[columnIndex] = !sortDirections[columnIndex];
      const ascending = sortDirections[columnIndex];

      const tbody = table.tBodies[0];
      const rows = Array.from(tbody.rows);

      rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();

        return ascending
          ? aText.localeCompare(bText, undefined, { numeric: true })
          : bText.localeCompare(aText, undefined, { numeric: true });
      });

      rows.forEach(row => tbody.appendChild(row));

      // Remove existing arrows
      Array.from(table.querySelectorAll('th')).forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
      });

      // Add arrow to clicked header
      cell.classList.add(ascending ? 'sort-asc' : 'sort-desc');
    } else {
      // Remove highlight from all rows
      Array.from(table.getElementsByTagName('tr')).forEach(r => {
        r.classList.remove('highlight');
      });

      // Highlight clicked row
      row.classList.add('highlight');

      // Call the callback with the first column value
      if (row.cells.length > 0) {
        rowCallback(row.cells[0].textContent.trim());
      }
    }
  });
}

function getNearestPoint(mouseX) {
  for (let pt of depth_points) {
    if (mouseX <= pt.x) {
      return pt
    }
  }
  return pt;
}

function mouse_tracker(e ) {
  const pt = svg.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;
  const cursor = pt.matrixTransform(svg.getScreenCTM().inverse());

  const nearest = getNearestPoint(cursor.x, cursor.y);

  // Update crosshair lines
  vline.setAttribute("x1", nearest.x);
  vline.setAttribute("x2", nearest.x);
  hline.setAttribute("y1", nearest.y);
  hline.setAttribute("y2", nearest.y);
 
  // Update coordinate text
  const time = nearest.t
  const depth = nearest.d
  coordText.textContent = `time: ${time.toFixed(1)}, depth: ${depth.toFixed(1)}`;
}