// Global Variable for Final Results
var resultData = {}

// Global Variable for Selection Criterias
var inputData = '';
var inputDict = {};

// xValues for Early Mission 
var earlyMission_xValues = [5.88, 9.80, 13.72, 17.64, 21.56, 25.48, 29.4, 35.28, 43.12, 50.96,
    58.8, 70.56, 86.24, 101.92, 117.6, 141.12, 172.48, 203.84, 235.2, 282.24, 
    344.96, 407.68, 470.4, 564.48, 689.92, 815.36, 940.8, 1128.96, 1379.84, 1630.72, 
    1881.6, 2257.92, 2759.68, 3261.44, 3763.2, 4515.84, 5519.36, 6522.88, 7526.4, 9031.68, 
    11038.72, 13045.75, 15052.79, 18063.35, 22077.43, 26091.51, 30105.59];

var lateMission_xValues = [3.92, 3.92, 7.84, 15.19, 19.6, 23.52, 27.44, 31.85, 39.2, 47.04, 
    54.88, 63.7, 78.4, 94.08, 109.76, 127.4, 156.8, 188.16, 219.52, 254.8,
    313.6, 376.32, 439.04, 509.6, 627.2, 752.64, 878.08, 1019.2, 1254.4, 1505.28,
    1756.16, 2038.4, 2508.8, 3010.56, 3512.32, 4076.8, 5017.6, 6021.12, 7024.643,
    8153.6, 10035.2, 12042.2, 14049.29, 16307.21, 20070.4, 24084.48, 28098.57];

// TODO: Undecided for both missions
var bothMissions_xValues =  [5.88, 9.80, 13.72, 17.64, 21.56, 25.48, 29.4, 35.28, 43.12, 50.96,
    58.8, 70.56, 86.24, 101.92, 117.6, 141.12, 172.48, 203.84, 235.2, 282.24, 
    344.96, 407.68, 470.4, 564.48, 689.92, 815.36, 940.8, 1128.96, 1379.84, 1630.72, 
    1881.6, 2257.92, 2759.68, 3261.44, 3763.2, 4515.84, 5519.36, 6522.88, 7526.4, 9031.68, 
    11038.72, 13045.75, 15052.79, 18063.35, 22077.43, 26091.51, 30105.59];


// Function that extracts user input and performs validation before sending to backend
function generateSpectra() {
   
    // Get User Input
    var [inputDict, inputData] = getUserInput();

    if (!inputDict || !inputData) {
        alert('Error Processing User Inputs');
    }

    // Display data in the modal if there is any input or selection
    if (validateFilters()) {
        if (inputData.trim() !== ''){
            // Summary Statistics
            var inputData = createFilterSelectionSummary(inputDict);
            
            // Send data to backend
            sendDataToBackend(inputDict).then(result => {    
                
                // Assign to global Variable
                resultData = JSON.parse(result);
                
                if (resultData.result == 0) {
                    clearFilters();
                    alert("No Datasets found for the criterias you've selected");
                } else {

                    // Create Charts
                    createCharts();

                    // Open the modal
                    openModal();
                }

            }).catch(error => {
                console.error('Error:', error);
            });
        }
        else {
            clearFilters();
            alert("No Filters Selected");
        }
    }
}


// Send data to backend in a dictionary format from generateSpectra()
function sendDataToBackend(data) {  

    return fetch('/process-data', { 
        method: 'POST', 
        headers: { 
          'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({data: data}) 
      }) 
      .then(response => response.text()) 
      .catch(error => { 
        console.error('Error:', error); 
        throw error; 
      }); 
}


// Displays Selection Criteria in modal 
function createSelectionCriteriaBoxes(text){
    
    // Select the container
    const container = document.getElementById('selectionCriteriaContainter');

    // Create a box container element
    const box = document.createElement('div');
    box.classList.add('selectionCriteriaBox'); 

    // Create a paragraph element for the text
    const textElement = document.createElement('p');
    textElement.textContent = text;

    // Append the text element to the box
    box.appendChild(textElement);

    // Append the box to the container
    container.appendChild(box);
}


// Generate Filter Selection Summary for users
function createFilterSelectionSummary(inputDict) {

    listOfSelections = []; 
    
    for (let selectionCriteria in inputDict) {
        var selectionAndFilterSummary = ''; 

        selectionAndFilterSummary += selectionCriteria + " : ";
        
        var selection = inputDict[selectionCriteria];

        // check if value is a dictionary
        if (typeof selection === 'object') {
            if (selection.hasOwnProperty('Hemisphere')) {
                selectionAndFilterSummary += selection["Hemisphere"] + ", ";
            }
    
            if (selection.hasOwnProperty("Range")) {
                if (selection["Range"] == "Between") {
                    selectionAndFilterSummary += " Between " + selection["minRange"] + " and " + selection["maxRange"];
                }
                else if (selection["Range"] == "Lesser Than") {
                    selectionAndFilterSummary += " Lesser Than " + selection["lesserThanValue"];
                }
                else if (selection["Range"] == "Greater Than") {
                    selectionAndFilterSummary += " Greater Than " + selection["greaterThanValue"];
                }
                else {
                    selectionAndFilterSummary += " Invalid Range";
                }
            }    

            // If selection criteria is mechanism, it should only have one element since its a radio button
            if (selectionCriteria == "MECHANISMS" && selection.length == 1) {
                selectionAndFilterSummary += selection[0];   
            }
        }

        // if value is not a dictionary, it is an array 
        if (selectionCriteria === "Statistics" ||
            selectionCriteria === "Spectra" ||
            selectionCriteria === "Normalization" ||
            selectionCriteria === "Mission") {
            
            selectionAndFilterSummary += inputDict[selectionCriteria].join(', ');
        }

        listOfSelections.push(selectionAndFilterSummary);
    }

    // Remove the comma at the end
    if (selectionAndFilterSummary.endsWith(',')) {
        selectionAndFilterSummary = selectionAndFilterSummary.slice(0, -1);
    }

    // Dynamically create selection criteria to display in modal 
    listOfSelections.forEach(selection => {
        createSelectionCriteriaBoxes(selection);
    });

    return listOfSelections
}


// Gets Early and Late Mission Data
function generateMissionCount() {

    var earlyMissionData = document.getElementById('earlyMissionRowData');
    var lateMissionData = document.getElementById('lateMissionRowData');
    earlyMissionData.innerHTML = "--";
    lateMissionData.innerHTML = "--";

    // Toggle the 'active' class on the button
    var generateMissionButton = document.getElementById('generateMissionButton');
    generateMissionButton.classList.toggle('active');

    // userInput = [inputDict, inputData]
    var userInput = getUserInput();
    var data = userInput[0];

    if (validateFilters()) {
        fetch('/mission-data', { 
            method: 'POST', 
            headers: { 
              'Content-Type': 'application/json'
            }, 
            body: JSON.stringify({data: data}) 
        }) 
        .then(response => response.json()) 
        .then(result => { 

            earlyMissionData.innerHTML = result.result[0].toString() + " row(s) of Data";
            lateMissionData.innerHTML = result.result[1].toString() + " row(s) of Data";

            if (generateMissionButton.classList.contains('active')) {
                // If the button already has 'active' class, remove it
                generateMissionButton.classList.remove('active');
            }

        }) 
        .catch(error => { 
        console.error('Error:', error); 
        }); 
    }
}


// Gets User input and stores them in both a dictionary and a text format
function getUserInput() {
   
       // Gather data from visible text input fields
       var textInputs = document.querySelectorAll('input[type="text"]:not([style*="display:none"])');
       textInputs.forEach(function (input) {
           var filterTitle = input.closest('.filterContainer').querySelector('.filterTitle').textContent;
           if (input.value.trim() !== '') {
               // Check if filter title exists in inputDict
               if (!inputDict[filterTitle]){
                   // Create a new dictionary for the filter title
                   inputDict[filterTitle] = {}; 
               }
   
               // Assign the new value to the placeholder in the filter title dictionary
               inputDict[filterTitle][input.name] = input.value;
               
               // Display results 
               inputData += filterTitle + ' : ' + input.name + ': ' + input.value + '<br>';
           }
       });
   
       // Gather data from visible checkboxes (both regular and radio)
       var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
       checkboxes.forEach(function (checkbox) {
           var filterTitle = checkbox.closest('.spectraGenerationRequirementCategory').querySelector('.filterTitle').textContent;
           
           // Check if filter title exists in inputDict        
           if (filterTitle in inputDict) {
               inputDict[filterTitle].push(checkbox.parentNode.textContent.trim());
           } else {
               inputDict[filterTitle] = [checkbox.parentNode.textContent.trim()];
           }
   
           // Display results 
           inputData += filterTitle + ' : ' + checkbox.parentNode.textContent.trim() + '<br>';
       });
   
       // Gather data from visible radio buttons
       var radioButtons = document.querySelectorAll('input[type="radio"]:checked');
       radioButtons.forEach(function (radio) {
           // Check if the radio button is within a filterContainer
           var filterContainer = radio.closest('.filterContainer');
           if (filterContainer && filterContainer.style.display !== 'none') {
               var filterTitleElement = filterContainer.querySelector('.filterTitle');
               if (filterTitleElement) {
                   var filterTitle = filterTitleElement.textContent;
                   inputData += filterTitle + ' : ' + radio.parentNode.textContent.trim() + '<br>';
   
                   if (filterTitle in inputDict) {
                       inputDict[filterTitle].push(radio.parentNode.textContent.trim());
                   } else {
                       inputDict[filterTitle] = [radio.parentNode.textContent.trim()];
                   }
               }
           } 
   
           // Check if the radio button is within a spectraGenerationRequirementCategory
           var spectraCategory = radio.closest('.spectraGenerationRequirementCategory');
           if (spectraCategory) {
               var filterTitleElement = spectraCategory.querySelector('.filterTitle');
               if (filterTitleElement) {
                   var filterTitle = filterTitleElement.textContent;

                   inputData += filterTitle + ' : ' + radio.parentNode.textContent.trim() + '<br>';
                   
                   if (filterTitle in inputDict) {
                       inputDict[filterTitle].push(radio.parentNode.textContent.trim());
                   } else {
                       inputDict[filterTitle] = [radio.parentNode.textContent.trim()];
                   }
               }
           }
       });
   
       // Gather data from visible dropdown menus
       var selectElements = document.querySelectorAll('select');
       selectElements.forEach(function (select) {
           var filterTitle = select.closest('.filterContainer').querySelector('.filterTitle').textContent;
           var selectedOption = select.options[select.selectedIndex].text;
           if (selectedOption.trim() !== 'Select a Hemisphere' && selectedOption.trim() !== 'Select a Range' ) {
               inputData += filterTitle + ' : ' + selectedOption + '<br>';
               
               // Check if filter title exists in inputDict
               if (!inputDict[filterTitle]){
                   // Create a new dictionary for the filter title
                   inputDict[filterTitle] = {}; 
               }
   
               if (selectedOption == "Northern Hemisphere" || selectedOption == "Southern Hemisphere" || selectedOption == "Either" ){
                   inputDict[filterTitle]["Hemisphere"] = selectedOption;
               }
               else {
                   // Assign the new value to the placeholder in the filter title dictionary
                   inputDict[filterTitle]["Range"] = selectedOption;
               }
           }
       });

    return [inputDict, inputData]
}


// Exports DataSets as a CSV file format
function exportCSV() {

    if (Object.keys(resultData).length === 0) {
        alert('Error Downloading CSV. Invalid Datasets');
    }

    var jsonData = JSON.parse(resultData); 
    yAxisValues = jsonData.result.yAxis;

    // Prepare CSV content for x-values
    let csvContent = 'X-Values: energy (eV)\n';
    if (inputDict["Mission"][0] == "Early Mission"){
        var xValues = earlyMission_xValues
    }
    // Late Mission
    else if (inputDict["Mission"][0] == "Late Mission") {
        var xValues = lateMission_xValues;
    }
    // What would be the value for Both Missions? 
    else {
        var xValues = bothMissions_xValues;
    }
    csvContent += xValues.join(',') + '\n\n';

    // Add each y-values array to the CSV content
    csvContent += `Y-Values: dEFlux\n`
    for (const key in yAxisValues) {
        if (yAxisValues.hasOwnProperty(key)) {

            if (key == "+1σ") {
                var updatedKey = "+1 sigma";
            }
            else if (key == "-1σ") {
                var updatedKey = "-1 sigma";
            }
            else {
                var updatedKey = key; 
            }

            csvContent += `${updatedKey}\n`;
            csvContent += yAxisValues[key].join(',') + '\n\n';
        }
    }

    // Add selection criteria to the CSV content
    csvContent += 'Selection Criteria\n';
    for (let selectionCriteria in inputDict) {

        csvContent += selectionCriteria + ",";
        
        var selection = inputDict[selectionCriteria];

        // check if value is a dictionary
        if (typeof selection === 'object') {
            if (selection.hasOwnProperty('Hemisphere')) {
                csvContent += selection["Hemisphere"] + ", ";
            }
    
            if (selection.hasOwnProperty("Range")) {
                if (selection["Range"] == "Between") {
                    csvContent += " Between " + selection["minRange"] + " and " + selection["maxRange"];
                }
                else if (selection["Range"] == "Lesser Than") {
                    csvContent += " Lesser Than " + selection["lesserThanValue"];
                }
                else if (selection["Range"] == "Greater Than") {
                    csvContent += " Greater Than " + selection["greaterThanValue"];
                }
                else {
                    csvContent += " Invalid Range";
                }
            }    

            // If selection criteria is mechanism, it should only have one element since its a radio button
            if (selectionCriteria == "MECHANISMS" && selection.length == 1) {
                csvContent += selection[0];   
            }
        }

        // if value is not a dictionary, it is an array 
        if (selectionCriteria === "Statistics" ||
            selectionCriteria === "Spectra" ||
            selectionCriteria === "Normalization" ||
            selectionCriteria === "Mission") {

            // CSV cannot read sigma symbol 
            var finalStatisticsArr = []
            for (const ele of inputDict[selectionCriteria]){
                if (ele == "+1σ") {
                    finalStatisticsArr.push("+1 sigma");
                }
                else if (ele == "-1σ") {
                    finalStatisticsArr.push("-1 sigma");
                }
                else {
                    finalStatisticsArr.push(ele);
                }
            }

            csvContent += finalStatisticsArr.join(', ');
        }

        csvContent += '\n';
    }

    // Create a Blob with the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

    // Generate download link for the CSV file
    const link = document.createElement('a');
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);

        // Get current date and time
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0'); 
        const day = String(currentDate.getDate()).padStart(2, '0'); 
        const hours = String(currentDate.getHours()).padStart(2, '0'); 
        const minutes = String(currentDate.getMinutes()).padStart(2, '0'); 
        const dateString = `${year}${month}${day}_${hours}${minutes}`;
        link.setAttribute('download', `datasets_${dateString}.csv`);

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}


// Exports graph as a JPEG format
function exportJPEG() {
    var canvas = document.getElementById('myChart');

    // Convert the chart to a base64-encoded JPEG image
    var imageData = canvas.toDataURL('image/jpeg');
    var link = document.createElement('a');

    // Set the href attribute to the base64-encoded image data
    link.href = imageData;

    // Get current date and time
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0'); 
    const day = String(currentDate.getDate()).padStart(2, '0'); 
    const hours = String(currentDate.getHours()).padStart(2, '0'); 
    const minutes = String(currentDate.getMinutes()).padStart(2, '0'); 
    const dateString = `${year}${month}${day}_${hours}${minutes}`;

    // Set the download attribute to specify the filename
    link.download = `spectra_graph_${year}${month}${day}_${hours}${minutes}.jpg`;

    // Programmatically trigger the download
    link.click();
}


// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add this line to get the reference to the close button
    var modal = document.getElementById('spectraPanel');
    var span = document.querySelector('.close');

    // When the user clicks on x, close the modal
    span.onclick = function() {
        modal.style.display = "none";
        clearFilters();
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            clearFilters();
        }
    }
});


// Function to open the modal
function openModal() {
    var modal = document.getElementById('spectraPanel');
    modal.style.display = 'block';
}


// Function to close the modal
function closeModal() {
    var modal = document.getElementById('spectraPanel');
    modal.style.display = 'none';
}


// Function to clear filters in modalContainer and global variabls inputData and inputDict
function clearFilters() {

    inputData = '';
    inputDict = {};

    const container = document.getElementById("selectionCriteriaContainter");
    if (container) {
        container.innerHTML = '';
    } else {
        console.error('Container not found');
    }
}
