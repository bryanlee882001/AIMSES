
// Function that extracts user input and performs validation before sending to backend
function generateSpectra() {
    // Function to generate Spectra
    var inputData = '';
    var inputDict = {};

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


    // Display data in the modal if there is any input or selection
    if (inputData.trim() !== '' && validateFilters()) {
        // var modalContent = document.getElementById('modalContent');
        modalContent.innerHTML = inputData;

        // Open the modal
        openModal();

        // Send data to backend
        sendDataToBackend(inputDict);
    }
    else {
        // Scroll the page to the top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    inputDict = {};
}


// Send data to backend in a dictionary format from generateSpectra()
function sendDataToBackend(data) {  
    fetch('/process-data', { 
        method: 'POST', 
        headers: { 
          'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({data: data}) 
      }) 
      .then(response => response.text()) 
      .then(result => { 
        console.log(result); 
      }) 
      .catch(error => { 
        console.error('Error:', error); 
      }); 
}


// Helper function to clear all error messages in a filterContainer
function clearErrors(container) {

    // Clear Error Messages
    var errorMessages = container.querySelectorAll('.error_message');
    errorMessages.forEach(function(errorMessage) {
        errorMessage.style.display = "none";
    });

    // Clear Red-colored borders (which are used to indicate error)
    var inputFields = container.querySelectorAll('input, select');
    inputFields.forEach(function(field) {
        if (field.style.borderColor = 'rgb(222,82,82)' && field.id != "hemisphereLabel") {
            field.style.borderColor = 'grey';
        }
    }); 

}


function validateNonEmptyNumericInputs(containerId) {

    // Get Container and Clear Error Messages before validating again
    var container = document.getElementById(containerId);
    clearErrors(container); 

    var isTrue = true; 

    // Get the computed style of the container element
    var computedStyle = window.getComputedStyle(container);

    // Check if the display property is set to 'none'
    if (computedStyle.display === 'none') {
        // If the container is hidden, return true immediately
        return isTrue;
    }

    // Check selected value of rangeSelect
    var rangeSelect = container.querySelector('#rangeSelect');
    if (rangeSelect.options[rangeSelect.selectedIndex].text == "Select a Range") {
        document.getElementById("error_message_range").innerText = "Please select a Range option";
        document.getElementById("error_message_range").style.display = "block";
        rangeSelect.style.borderColor = 'rgb(222,82,82)';
        isTrue = false;
    }

    // Check selected value of hemisphereSelect 
    var hemisphereSelect = container.querySelector('#hemisphereSelect');
    if (hemisphereSelect.options[hemisphereSelect.selectedIndex].text == "Select a Hemisphere") {
        document.getElementById("error_message_hemisphere").innerText = "Please select a Hemisphere option";
        document.getElementById("error_message_hemisphere").style.display = "block";
        hemisphereSelect.style.borderColor = 'rgb(222,82,82)';
        isTrue = false;
    }

    // Check Text Inputs Based on rangeSelect
    var errorMessage = container.querySelector("#error_message_range");
    if (rangeSelect.value === 'between') {
        // Check if minRange and maxRange are filled and are numbers
        var minRange = container.querySelector('#minRange');
        var maxRange = container.querySelector('#maxRange');

        if (minRange.value.trim() === '' || isNaN(minRange.value)) {
            errorMessage.innerText = "Please enter a valid number for Min Range";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }

        if (maxRange.value.trim() === '' || isNaN(maxRange.value)) {
            errorMessage.innerText = "Please enter a valid number for Max Range";
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }

        if ((minRange.value.trim() === '' || isNaN(minRange.value)) && (maxRange.value.trim() === '' || isNaN(maxRange.value))){
            errorMessage.innerText = "Please enter valid numbers for both Min Range and Max Range ";
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    } else if (rangeSelect.value === 'lesserThan') {
        // Check if lesserThanValue is filled and is a number
        var lesserThanValue = container.querySelector('#lesserThanValue');

        if (lesserThanValue.value.trim() === '' || isNaN(lesserThanValue.value)) {
            document.getElementById("error_message_range").innerText = "Please enter a valid number for Lesser Than Range";
            document.getElementById("error_message_range").style.display = "block";
            lesserThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    } else if (rangeSelect.value === 'greaterThan') {
        // Check if greaterThanValue is filled and is a number
        var greaterThanValue = container.querySelector('#greaterThanValue');

        if (greaterThanValue.value.trim() === '' || isNaN(greaterThanValue.value)) {
            document.getElementById("error_message_range").innerText = "Please enter a valid number for Greater Than Range";
            document.getElementById("error_message_range").style.display = "block";
            greaterThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    }

    return isTrue;
}


// A function that calls all inputValidation functions
function validateFilters() {    
    
    var isTrue;

    // Check MLT Filter

    // Check ILAT Filter 
    isTrue = validateILAT("filter_ilat");

    // Check ALT Filter
    // isTrue = validateMLT("filter_mlt");

    return isTrue;
}


function validateMLT(containerId) {

    var isTrue = true;
    var container = document.getElementById(containerId);
    var rangeSelect = container.querySelector('#rangeSelect');
    var errorMessage = container.querySelector("#error_message_range");

    // Check 

}


// A function that validates ILAT inputs
function validateILAT(containerId) {
    
    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    var isTrue = true;
    var container = document.getElementById(containerId);
    var rangeSelect = container.querySelector('#rangeSelect');
    var hemisphereSelect = container.querySelector('#hemisphereSelect');
    var errorMessage = container.querySelector("#error_message_range");

    // Check Text Inputs Based on rangeSelect
    if (rangeSelect.value === 'between') {
        // Get Min and Max Range
        var minRange = container.querySelector('#minRange');
        var maxRange = container.querySelector('#maxRange');

        var minRangeVal = parseFloat(minRange.value);
        var maxRangeVal = parseFloat(maxRange.value);

        if (hemisphereSelect.value == 'northernhemisphere') {
            if (minRangeVal < 0) {
                errorMessage.innerText = "Nothern Hemisphere: Min Range should be above 0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (maxRangeVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Max Range should be less than 90";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Nothern Hemisphere: Max Range cannot be less than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (minRangeVal < 0 && maxRangeVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Min Range should be above 0 and Max Range should be less than 90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (minRangeVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Min Range should be above -90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (maxRangeVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Max Range should be less than 0";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Southern Hesmiphere: Max Range cannot be less than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (minRangeVal < -90 && maxRangeVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Min Range should be more than -90 and Max Range should be less than 0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
        } else if (hemisphereSelect.value == 'either') {
            if (minRangeVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be above 0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (maxRangeVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Max Range should be less than 90";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Either Hemisphere: Max Range cannot be less than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (minRangeVal < 0 && maxRangeVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be above 0 and Max Range should be less than 90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal != Math.abs(minRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be an absolute value";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (maxRangeVal != Math.abs(maxRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Max Range should be an absolute value";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal != Math.abs(minRangeVal) && maxRangeVal != Math.abs(maxRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Both Min and Max Ranges should be absolute values";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
        }
    } else if (rangeSelect.value === 'lesserThan') {
        
        // Get lesserThan value
        var lesserThan = container.querySelector('#lesserThanValue');
        var lesserThanVal = parseFloat(lesserThan.value);

        if (hemisphereSelect.value == 'northernhemisphere') {
            if (lesserThanVal < 0) {
                errorMessage.innerText = "Nothern Hemisphere: Lesser Than Value should be above 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (lesserThanVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Lesser Than Value should be less than 90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (lesserThanVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Lesser Than Value should be above -90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (lesserThanVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Lesser Than Value should be less than 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        } else if (hemisphereSelect.value == 'either') {
            if (lesserThanVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be above 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (lesserThanVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be less than 90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (lesserThanVal != Math.abs(lesserThanVal)) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be an absolute value";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        }
    } else if (rangeSelect.value === 'greaterThan') {

        // Get lesserThan value
        var greaterThan = container.querySelector('#greaterThanValue');
        var greaterThanVal = parseFloat(greaterThan.value);

        if (hemisphereSelect.value == 'northernhemisphere') {
            if (greaterThanVal < 0) {
                errorMessage.innerText = "Nothern Hemisphere: Greater Than Value should be above 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (greaterThanVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Greater Than Value should be less than 90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (greaterThanVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Greater Than Value should be above -90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (greaterThanVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Greater Than Value should be less than 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        } else if (hemisphereSelect.value == 'either') {
            if (greaterThanVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be above 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (greaterThanVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be less than 90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (greaterThanVal != Math.abs(greaterThanVal)) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be an absolute value";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        }
    }

    return isTrue 
}




   // container.querySelectorAll('select').forEach(function (field) {  
    //     // Check Range Selection
    //     if (field.id == "rangeSelect" && field.options[field.selectedIndex].text == "Select a Range") {
    //         document.getElementById("error_message_range").innerText = "Please select a Range option";
    //         document.getElementById("error_message_range").style.display = "block";
    //         field.style.borderColor = 'rgb(222,82,82)';
    //         isTrue = false;
    //     }

    //     // Check Range Selection
    //     if (field.id == "hemisphereSelect" && field.options[field.selectedIndex].text == "Select a Hemisphere") {
    //         document.getElementById("error_message_hemisphere").innerText = "Please select a Hemisphere";
    //         document.getElementById("error_message_hemisphere").style.display = "block";
    //         field.style.borderColor = 'rgb(222,82,82)';
    //         isTrue = false;
    //     }
    // });
    //