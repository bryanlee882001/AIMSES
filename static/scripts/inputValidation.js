

// A function that calls all validating functions 
function validateFilters() {    
    
    // Array to store the results of each filter function
    var results = [];

    // Check MLT Filter and store the result
    results.push(validateMLT("filter_mlt"));

    // Check ILAT Filter and store the result
    results.push(validateILAT("filter_ilat"));

    // Check ALT Filter and store the result 
    results.push(validateALT("filter_alt"));

    // Check SZA Filter and store the result 
    results.push(validateSZA("filter_sza"));

    // Check F10.7 Filter and store the result
    results.push(validateF107("filter_f107"));

    // Check EFLUX Filter and store the result
    results.push(validateSZA("filter_eflux"));

    // Check NFLUX Filter and store the result
    results.push(validateSZA("filter_nflux"));

    // Check Conjugate SZA Filter and store the result
    results.push(validateConjugateSZA("filter_conjugate_sza"));

    // Check KP Filter and store the result
    results.push(validateKP("filter_kp"));

    // Check AE Filter and store the result
    results.push(validateAE("filter_ae"));

    // Check DST Filter and store the result
    results.push(validateDST("filter_dst"));

    // Check Newell Flux Filter and store the result
    results.push(validateNewellFlux("filter_newell_flux"));

    // Check LCA Filter and store the result
    results.push(validateLCA("filter_lca"));

    // Check Mechs Filter and store the result
    results.push(validateMECHS("filter_mechs"));

    // Check if any of the results are false
    for (var i = 0; i < results.length; i++) {
        if (!results[i]) {
            // If any result is false, return false
            return false;
        }
    }   


    // If all results are true, return true
    return true;
}


// A helper function to clear all error messages in a filterContainer
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

    // Clear Red-colored borders for filterContainer 
    if (container.style.borderColor == 'rgb(222,82,82)'){
        container.style.borderColor = '1px solid white';
    }
}


// A function that is used to validate generic filters with only range: between, lessThan, greaterThan options
function validateGenericFilters(containerId, rangeMinLimit, rangeMaxLimit) {

    var isTrue = true;
    var container = document.getElementById(containerId);
    var rangeSelect = container.querySelector('#rangeSelect');
    var errorMessage = container.querySelector("#error_message_range");

    // Check Text Inputs Based on rangeSelect
    if (rangeSelect.value === 'between') {
        // Get Min and Max Range
        var minRange = container.querySelector('#minRange');
        var maxRange = container.querySelector('#maxRange');

        var minRangeVal = parseFloat(minRange.value);
        var maxRangeVal = parseFloat(maxRange.value);

        if (minRangeVal < rangeMinLimit) {
            errorMessage.innerText = "Min Range should be greater than or equal to ".concat(rangeMinLimit);
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (maxRangeVal > rangeMaxLimit) {
            errorMessage.innerText = "Max Range should be lesser than or equal to ".concat(rangeMaxLimit);
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
        if (minRangeVal >= maxRangeVal) {
            errorMessage.innerText = "Max Range cannot be lesser than or equal to Min Range";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (minRangeVal > rangeMaxLimit) {
            errorMessage.innerText = "Min Range should be lesser than or equal to ".concat(rangeMaxLimit);
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)'; 
        }
        if (maxRangeVal < rangeMinLimit) {
            errorMessage.innerText = "Max Range should be greater than or equal to ".concat(rangeMinLimit);
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)'; 
        }
        if ((minRangeVal < rangeMinLimit && maxRangeVal > rangeMaxLimit) || (minRangeVal > rangeMaxLimit && maxRangeVal < rangeMinLimit)) {
            errorMessage.innerText = "Min Range should be greater than or equal to  ".concat(rangeMinLimit, " and Max Range should be lesser than or equal to ", rangeMaxLimit);
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        

    } else if (rangeSelect.value === 'lesserThan') {
        
        // Get lesserThan value
        var lesserThan = container.querySelector('#lesserThanValue');
        var lesserThanVal = parseFloat(lesserThan.value);

        if (lesserThanVal < rangeMinLimit) {
            errorMessage.innerText = "Lesser Than Value should be greater than or equal to  ".concat(rangeMinLimit);
            errorMessage.style.display = "block";
            lesserThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (lesserThanVal > rangeMaxLimit) {
            errorMessage.innerText = "Lesser Than Value should be lesser than or equal to ".concat(rangeMaxLimit);
            errorMessage.style.display = "block";
            lesserThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
    } else if (rangeSelect.value === 'greaterThan') {

        // Get greaterThan value
        var greaterThan = container.querySelector('#greaterThanValue');
        var greaterThanVal = parseFloat(greaterThan.value);

        if (greaterThanVal < rangeMinLimit) {
            errorMessage.innerText = "Greater Than Value should be greater than or equal to ".concat(rangeMinLimit);
            errorMessage.style.display = "block";
            greaterThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (greaterThanVal > rangeMaxLimit) {
            errorMessage.innerText = "Greater Than Value should be lesser than or equal to ".concat(rangeMaxLimit);
            errorMessage.style.display = "block";
            greaterThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
    }

    // Highlight filterContainer Red if there's an Error
    if (!isTrue) {
        container.style.borderColor = 'rgb(222,82,82)';
    }
    else {
        container.style.borderColor = 'white'
    }

    return isTrue 
}


// A function that validates if all inputs in a filterContainer are numeric and non-empty
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

    // Get Error Message ID 
    var errorMessage = container.querySelector("#error_message_range");

    // Check selected value of rangeSelect
    var rangeSelect = container.querySelector('#rangeSelect');
    if (rangeSelect.options[rangeSelect.selectedIndex].text == "Select a Range") {
        errorMessage.innerText = "Please select a Range option";
        errorMessage.style.display = "block";
        rangeSelect.style.borderColor = 'rgb(222,82,82)';
        isTrue = false;
    }

    // Only applicable for ILAT for checking hemisphere
    if (containerId == "filter_ilat"){
        // Check selected value of hemisphereSelect 
        var errorMessageHemisphere = container.querySelector("#error_message_hemisphere");
        var hemisphereSelect = container.querySelector('#hemisphereSelect');
        if (hemisphereSelect.options[hemisphereSelect.selectedIndex].text == "Select a Hemisphere") {
            errorMessageHemisphere.innerText = "Please select a Hemisphere option";
            errorMessageHemisphere.style.display = "block";
            hemisphereSelect.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    }


    // Check Text Inputs Based on rangeSelect
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
            errorMessage.innerText = "Please enter a valid number for Lesser Than Range";
            errorMessage.style.display = "block";
            lesserThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    } else if (rangeSelect.value === 'greaterThan') {
        // Check if greaterThanValue is filled and is a number
        var greaterThanValue = container.querySelector('#greaterThanValue');

        if (greaterThanValue.value.trim() === '' || isNaN(greaterThanValue.value)) {
            errorMessage.innerText = "Please enter a valid number for Greater Than Range";
            errorMessage.style.display = "block";
            greaterThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    }

    // Highlight filterContainer Red if there's an Error
    if (!isTrue) {
        container.style.borderColor = 'rgb(222,82,82)';
    }
    else {
        container.style.borderColor = 'white'
    }
    
    return isTrue;
}


// A function that validates if all time inputs in a filterContainer are numeric and non-empty
function validateMLT(containerId) {

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

    // Check selected value of rangeSelect
    var errorMessage = container.querySelector("#error_message_range");
    
    // Regular expression to match the format "HH:MM:SS"
    var regex = /^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$/;

    if (rangeSelect.value === 'between') {
        // Check if minRange and maxRange are filled and are in time format
        var minRange = container.querySelector('#minRange');
        var maxRange = container.querySelector('#maxRange');

        if (!regex.test(minRange.value.trim())) {
            errorMessage.innerText = "Please enter a valid time in the format 'HH:MM:SS' for Min Range";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }

        if (!regex.test(maxRange.value.trim()))  {
            errorMessage.innerText = "Please enter a valid time in the format 'HH:MM:SS' for Max Range";
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }

        if (!regex.test(maxRange.value.trim()) && !regex.test(minRange.value.trim()))  {
            errorMessage.innerText = "Please enter a valid time in the format 'HH:MM:SS' for both Min and Max Ranges";
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    } else if (rangeSelect.value === 'lesserThan') {
        // Check if lesserThanValue is filled and is in time format
        var lesserThanValue = container.querySelector('#lesserThanValue');

        if (!regex.test(lesserThanValue.value.trim())) {
            errorMessage.innerText = "Please enter a valid time in the format 'HH:MM:SS' for Lesser Than Range";
            errorMessage.style.display = "block";
            lesserThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    } else if (rangeSelect.value === 'greaterThan') {
        // Check if greaterThanValue is filled and is in time format
        var greaterThanValue = container.querySelector('#greaterThanValue');

        if (!regex.test(greaterThanValue.value.trim())) {
            errorMessage.innerText = "Please enter a valid time in the format 'HH:MM:SS' for Greater Than Range";
            errorMessage.style.display = "block";
            greaterThanValue.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
    }

    // Highlight filterContainer Red if there's an Error
    if (!isTrue) {
        container.style.borderColor = 'rgb(222,82,82)';
    }
    else {
        container.style.borderColor = 'white'
    }

    return isTrue;
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
                errorMessage.innerText = "Nothern Hemisphere: Min Range should be greater than or equal to 0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (maxRangeVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Max Range should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Nothern Hemisphere: Max Range cannot be lesser than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (minRangeVal < 0 && maxRangeVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Min Range should be greater than or equal to 0 and Max Range should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (minRangeVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Min Range should be greater than or equal to -90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (maxRangeVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Max Range should be lesser than or equal to 0";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Southern Hesmiphere: Max Range cannot be lesser than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (minRangeVal < -90 && maxRangeVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Min Range should be greater than or equal to -90 and Max Range should be lesser than or equal to 0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
        } else if (hemisphereSelect.value == 'either') {
            if (minRangeVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be greater than or equal to  0";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (maxRangeVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Max Range should be lesser than or equal to  90";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal >= maxRangeVal) {
                errorMessage.innerText = "Either Hemisphere: Max Range cannot be lesser than or equal to Min Range";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (minRangeVal < 0 && maxRangeVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be greater than or equal to 0 and Max Range should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal != Math.abs(minRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Min Range should be a positive value";
                errorMessage.style.display = "block";
                minRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
            if (maxRangeVal != Math.abs(maxRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Max Range should be a positive value";
                errorMessage.style.display = "block";
                maxRange.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (minRangeVal != Math.abs(minRangeVal) && maxRangeVal != Math.abs(maxRangeVal)) {
                errorMessage.innerText = "Either Hemisphere: Both Min and Max Ranges should be positive values";
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
                errorMessage.innerText = "Nothern Hemisphere: Lesser Than Value should be greater than or equal to 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (lesserThanVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Lesser Than Value should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (lesserThanVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Lesser Than Value should be greater than or equal to -90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (lesserThanVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Lesser Than Value should be lesser than or equal to 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        } else if (hemisphereSelect.value == 'either') {
            if (lesserThanVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be greater than or equal to 0";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (lesserThanVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                lesserThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (lesserThanVal != Math.abs(lesserThanVal)) {
                errorMessage.innerText = "Either Hemisphere: Lesser Than Value should be a positive value";
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
                errorMessage.innerText = "Nothern Hemisphere: Greater Than Value should be greater than or equal to 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (greaterThanVal > 90) {
                errorMessage.innerText = "Nothern Hemisphere: Greater Than Value should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
        } else if (hemisphereSelect.value == 'southernhemisphere') {
            if (greaterThanVal < -90) {
                errorMessage.innerText = "Southern Hesmiphere: Greater Than Value should be greater than or equal to -90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (greaterThanVal > 0) {
                errorMessage.innerText = "Southern Hesmiphere: Greater Than Value should be lesser than or equal to 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        } else if (hemisphereSelect.value == 'either') {
            if (greaterThanVal < 0) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be greater than or equal to 0";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }
            if (greaterThanVal > 90) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be lesser than or equal to 90";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            } 
            if (greaterThanVal != Math.abs(greaterThanVal)) {
                errorMessage.innerText = "Either Hemisphere: Greater Than Value should be a positive value";
                errorMessage.style.display = "block";
                greaterThan.style.borderColor = 'rgb(222,82,82)';
                isTrue = false;
            }  
        }
    }

    // Highlight filterContainer Red if there's an Error
    if (!isTrue) {
        container.style.borderColor = 'rgb(222,82,82)';
    }
    else {
        container.style.borderColor = 'white'
    }

    return isTrue 
}


// A function that validates ALT inputs
function validateALT(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 334.131, 4175.79);
}


// A function that validates SZA Inputs
function validateSZA(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    return validateGenericFilters(containerId, 0, 180);
}


// A function that validates F10.7 Inputs
function validateF107(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 64.6, 999.9);
}


// A function that validates EFLUX Inputs
function validateEFLUX() {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, -10022.1, 9391460);
}


// A function that validates NFLUX Inputs
function validateNFLUX() {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, -1029355012096.0000000000, 101642582097920.0000000000);
}


// A function that validates Conjugate SZA Inputs 
function validateConjugateSZA(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 0, 180);
}


// A function that validates KP Inputs 
function validateKP(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    // Note: minRange >= 0 and maxRange < 9 (NOT <= 9 like the rest of the filters)
    var isTrue = true;
    var container = document.getElementById(containerId);
    var rangeSelect = container.querySelector('#rangeSelect');
    var errorMessage = container.querySelector("#error_message_range");

    // Check Text Inputs Based on rangeSelect
    if (rangeSelect.value === 'between') {
        // Get Min and Max Range
        var minRange = container.querySelector('#minRange');
        var maxRange = container.querySelector('#maxRange');

        var minRangeVal = parseFloat(minRange.value);
        var maxRangeVal = parseFloat(maxRange.value);

        if (minRangeVal < 0) {
            errorMessage.innerText = "Min Range should be greater than or equal to 0";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (maxRangeVal >= 9) {
            errorMessage.innerText = "Max Range should be lesser than 9";
            errorMessage.style.display = "block";
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
        if (minRangeVal >= maxRangeVal) {
            errorMessage.innerText = "Max Range should be greater than or equal to Min Range";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (minRangeVal >= 9) {
            errorMessage.innerText = "Min Range should be lesser than 9";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)'; 
        }
        if (maxRangeVal < 0) {
            errorMessage.innerText = "Max Range should be greater than or equal to 0";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)'; 
        }
        if ((minRangeVal < 0 && maxRangeVal >= 9) || (minRangeVal >= 9 && maxRangeVal < 0)) {
            errorMessage.innerText = "Min Range should be greater than or equal to 0 and Max Range should be lesser than 9";
            errorMessage.style.display = "block";
            minRange.style.borderColor = 'rgb(222,82,82)';
            maxRange.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        

    } else if (rangeSelect.value === 'lesserThan') {
        
        // Get lesserThan value
        var lesserThan = container.querySelector('#lesserThanValue');
        var lesserThanVal = parseFloat(lesserThan.value);

        if (lesserThanVal < 0) {
            errorMessage.innerText = "Lesser Than Value should be greater than or equal to 0";
            errorMessage.style.display = "block";
            lesserThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (lesserThanVal >= 9) {
            errorMessage.innerText = "Lesser Than Value should be lesser than 9";
            errorMessage.style.display = "block";
            lesserThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
    } else if (rangeSelect.value === 'greaterThan') {

        // Get greaterThan value
        var greaterThan = container.querySelector('#greaterThanValue');
        var greaterThanVal = parseFloat(greaterThan.value);

        if (greaterThanVal < 0) {
            errorMessage.innerText = "Greater Than Value should be greater than or equal to 0";
            errorMessage.style.display = "block";
            greaterThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        }
        if (greaterThanVal >= 9) {
            errorMessage.innerText = "Greater Than Value should be lesser than 9";
            errorMessage.style.display = "block";
            greaterThan.style.borderColor = 'rgb(222,82,82)';
            isTrue = false;
        } 
    }

    // Highlight filterContainer Red if there's an Error
    if (!isTrue) {
        container.style.borderColor = 'rgb(222,82,82)';
    }
    else {
        container.style.borderColor = 'white'
    }

    return isTrue 

}


// A function that validates AE Inputs 
function validateAE(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 0, 4192);
}


// A function that validates DST Inputs 
function validateDST(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, -422, 65);
}


// A function that validates Newell Flux Inputs 
function validateNewellFlux(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 0, 97633.1);
}


// A function that validates LCA Inputs
function validateLCA(containerId) {

    // Check if inputs are numeric and not empty
    if (!validateNonEmptyNumericInputs(containerId)) {
        return false;
    }

    // Min and Max values queried from database
    return validateGenericFilters(containerId, 28.7549, 72.2185);
}


// A function that validates LCA Inputs
function validateMECHS(containerId) {

    // Get container and clear existing errors
    var container = document.getElementById(containerId);
    clearErrors(container); 

    // Get the computed style of the container element
    var computedStyle = window.getComputedStyle(container);

    // Check if the display property is set to 'none'
    if (computedStyle.display === 'none') {
        // If the container is hidden, return true immediately
        return true;
    }

    // Find all radio buttons within the container that have the name "mechs"
    var checkboxes = container.querySelectorAll('input[type="radio"][name="mechs"]');
    var isChecked = false;

    // Loop through each checkbox
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            isChecked = true;
        }
    });

    if (!isChecked ) {
        // Highlight filterContainer Red if there's an Error
        container.style.borderColor = 'rgb(222,82,82)';

        var errorMessage = container.querySelector('.error_message');
        errorMessage.style.display = 'block';
        errorMessage.innerText = 'Please select at least one option';
    }
    else {
        container.style.borderColor = 'white'
    }

    return isChecked
}
