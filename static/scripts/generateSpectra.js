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
   
    // userInput = [inputDict, inputData]
    var userInput = getUserInput();
    var inputDict = userInput[0];
    var inputData = userInput[1];

    // Display data in the modal if there is any input or selection
    if (validateFilters()) {
        if (inputData.trim() !== ''){
            // Summary Statistics (Not in-use at the moment)
            // var modalContent = document.getElementById('modalContent');
            // modalContent.innerHTML = createFilterSelectionSummary(inputDict);
            var inputData = createFilterSelectionSummary(inputDict);
            
            // Send data to backend
            sendDataToBackend(inputDict).then(result => {    
                
                // Assign to global Variable
                resultData = result;
                // console.log(resultData);

                // Create Charts
                createCharts();

                // Open the modal
                openModal();


            }).catch(error => {
                console.error('Error:', error);
            });
        }
        else {
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
        throw error; // rethrow the error to be caught by the caller
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

    var selectionAndFilterSummary = ''; 
    for (let selectionCriteria in inputDict) {

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

        selectionAndFilterSummary += ', ';
    }

    // Remove the comma at the end
    if (selectionAndFilterSummary.endsWith(',')) {
        selectionAndFilterSummary = selectionAndFilterSummary.slice(0, -1);
    }

    // Split the summary into separate elements
    const elements = selectionAndFilterSummary.split(', ');

    elements.forEach(element => {
        if (element.trim() !== '') {
            createSelectionCriteriaBoxes(element.trim());
        }
    });

    return elements
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


function exportCSV() {
    let data = [
        [ 'Id', 'FirstName', 'LastName', 'Mobile', 'Address' ], // This is your header.
        [ 1, 'Richard', 'Roe', '9874563210', 'Address' ],
        [ 2, 'Joe', 'Doakes', '7896541230', 'Address' ],
        [ 3, 'John', 'Smith', '8745632109', 'Address' ],
        [ 4, 'Joe', 'Sixpack', '9875647890', 'Address' ],
        [ 5, 'Richard', 'Thomson', '8632547890', 'Address' ]
    ];

    let excelData = '';

    // Prepare data for excel.You can also use html tag for create table for excel.
    data.forEach(( rowItem, rowIndex ) => {   
        
        if (0 === rowIndex) {
            // This is for header.
        rowItem.forEach((colItem, colIndex) => {
            excelData += colItem + ',';
        });
        excelData += "\r\n";
        } else {
            // This is data.
            rowItem.forEach((colItem, colIndex) => {
        excelData += colItem + ',';   
        })
        excelData += "\r\n";       
        }
    });

    // Create the blob url for the file. 
    excelData = "data:text/xlsx," + encodeURI(excelData);

    // Download the xlsx file.
    let a = document.createElement("A");
    a.setAttribute("href", excelData);
    a.setAttribute("download", "filename.xlsx");
    document.body.appendChild(a);
    a.click();
}