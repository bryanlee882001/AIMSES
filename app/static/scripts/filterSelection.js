// Toggle Visibility of hidden filters
function toggleVisibility(containerID) {
    
    // Toggle the visibility of the corresponding div
    var container = document.getElementById(containerID);
    var isVisible = (container.style.display !== 'none' && container.style.display !== '');

    // If the element is becoming invisible, clear user input
    if (isVisible) {
        ClearAllInputsInContainer(container);
        
        // We don't have to hide the labels for MECHANISMS
        if (containerID != "filter_mechs"){
            // Reset dropdown selection
            container.querySelector('select').selectedIndex = 0;
            
            // Hide specific input fields if necessary
            container.querySelectorAll(".between, .lesserThanInput, .greaterThanInput").forEach(function (field) {
                field.style.display = "none";
            });

            // Hide specific labels if necessary
            container.querySelectorAll("#minRangeLabel, #maxRangeLabel, #lesserThanLabel, #greaterThanLabel").forEach(function (label) {
                label.style.display = "none";
            });

            hideLabels([container.querySelector("#minRangeLabel"), container.querySelector("#maxRangeLabel"), 
                        container.querySelector("#lesserThanLabel"), container.querySelector("#greaterThanLabel"),
                        container.querySelector('#minRangeUnit'),container.querySelector('#maxRangeUnit'),
                        container.querySelector('#lesserThanUnit'),container.querySelector('#greaterThanUnit')]);
        }

        // Clear Error Messages Before Switching Fields
        var errorMessages = container.querySelectorAll('.error_message');
        errorMessages.forEach(function(errorMessage) {
                errorMessage.style.display = "none";
        });

        // Clear Red-colored borders Before Switching Fields (which are used to indicate error)
        var inputFields = container.querySelectorAll('input, select');
        inputFields.forEach(function(field) {
            if (field.style.borderColor = 'rgb(222,82,82)') {
                field.style.borderColor = 'grey';
            }
        }); 
        
        // Clear Red-colored borders for filterContainer 
        if (container.style.borderColor = 'rgb(222,82,82)'){
            container.style.borderColor = 'white';
        }
    }   

    // Toggle the display style
    container.style.display = isVisible ? 'none' : 'block';

    // Toggle the active class for the clicked button
    var clickedButton = event.target;
    clickedButton.classList.toggle('active');

    // Remove active class from other buttons
    var otherButtons = document.querySelectorAll('.toggleButton:not(.active)');
    otherButtons.forEach(function(button) {
        button.classList.remove('active');
    });

    // Update the active button reference
    activeButton = (clickedButton.classList.contains('active')) ? clickedButton : null;
}


// Function to clear all inputs in a container regardless of whether its display is none
function ClearAllInputsInContainer(container) {
    
    // Clear text input fields within the container only if they are hidden
    var textInputs = container.querySelectorAll('input[type="text"]');
    textInputs.forEach(function(input) {
            input.value = '';
    });

    // Reset select elements within the container only if they are hidden
    var selectElements = container.querySelectorAll('select');
    selectElements.forEach(function(select) {
            select.selectedIndex = 0;
    });

    // Uncheck checkboxes within the container only if they are hidden
    var checkboxes = container.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
            checkbox.checked = false;
    });

    // Uncheck radio buttons within the container only if they are hidden
    var radioButtons = container.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(function(radio) {
            radio.checked = false;
    });
}


// Function to clear all inputs in a container if display is set to none
function ClearAllInputsInContainerBasedOnDisplay(container){
   
    // Clear text input fields within the container only if they are hidden
    var textInputs = container.querySelectorAll('input[type="text"]');
    textInputs.forEach(function(input) {
        if (window.getComputedStyle(input).display == 'none'){
            input.value = '';
        }
    });

    // Reset select elements within the container only if they are hidden
    var selectElements = container.querySelectorAll('select');
    selectElements.forEach(function(select) {
        if (window.getComputedStyle(select).display == 'none'){
            select.selectedIndex = 0;
        }
    });

    // Uncheck checkboxes within the container only if they are hidden
    var checkboxes = container.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        if (window.getComputedStyle(checkbox).display == 'none'){
            checkbox.checked = false;
        }
    });

    // Uncheck radio buttons within the container only if they are hidden
    var radioButtons = container.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(function(radio) {
        if (window.getComputedStyle(radio).display == 'none'){
            radio.checked = false;
        }
    });
}


// Function to switch fields for between, lesser than, and greater than options
function toggleFields(containerId) {
    var container = document.getElementById(containerId);
    var select = container.querySelector("#rangeSelect");
    var betweenFields = container.querySelectorAll(".between");
    var lesserThanField = container.querySelector(".lesserThanInput");
    var greaterThanField = container.querySelector(".greaterThanInput");

    // Get label elements
    var minRangeLabel = container.querySelector("#minRangeLabel");
    var maxRangeLabel = container.querySelector("#maxRangeLabel");
    var lesserThanLabel = container.querySelector("#lesserThanLabel");
    var greaterThanLabel = container.querySelector("#greaterThanLabel");
    var minRangeUnit = container.querySelector('#minRangeUnit');
    var maxRangeUnit = container.querySelector('#maxRangeUnit');
    var lesserThanUnit = container.querySelector('#lesserThanUnit');
    var greaterThanUnit = container.querySelector('#greaterThanUnit');

    // Clear Error Messages Before Switching Fields
    var errorMessages = container.querySelectorAll('.error_message');
    errorMessages.forEach(function(errorMessage) {
            errorMessage.style.display = "none";
    });

    // Clear Red-colored borders Before Switching Fields (which are used to indicate error)
    var inputFields = container.querySelectorAll('input, select');
    inputFields.forEach(function(field) {
        if (field.style.borderColor = 'rgb(222,82,82)') {
            field.style.borderColor = 'grey';
        }
    }); 

    // Clear Red-colored border for filterContainer
    if (container.style.borderColor = 'rgb(222,82,82)'){
        container.style.borderColor = 'white';
    }

    // If selected value is between, lesser than, or greater than 
    if (select.value === "between") {
        betweenFields.forEach(function (field) {
            field.style.display = "block";            
        });
        lesserThanField.style.display = "none";
        greaterThanField.style.display = "none";
        showLabels([minRangeLabel, maxRangeLabel, minRangeUnit, maxRangeUnit]);
        hideLabels([lesserThanLabel, greaterThanLabel, lesserThanUnit, greaterThanUnit]);
        
        // Clear Inputs from previous fields after switching
        ClearAllInputsInContainerBasedOnDisplay(container);

    } else if (select.value === "lesserThan") {
        betweenFields.forEach(function (field) {
            field.style.display = "none";
        });
        lesserThanField.style.display = "block";
        greaterThanField.style.display = "none";
        showLabels([lesserThanLabel, lesserThanUnit]);
        hideLabels([minRangeLabel, maxRangeLabel, greaterThanLabel, minRangeUnit, maxRangeUnit, greaterThanUnit]);

        // Clear Inputs from previous fields after switching
        ClearAllInputsInContainerBasedOnDisplay(container);

    } else if (select.value === "greaterThan") {
        betweenFields.forEach(function (field) {
            field.style.display = "none";
        });
        lesserThanField.style.display = "none";
        greaterThanField.style.display = "block";
        showLabels([greaterThanLabel, greaterThanUnit]);
        hideLabels([minRangeLabel, maxRangeLabel, lesserThanLabel, minRangeUnit, maxRangeUnit, lesserThanUnit]);

        // Clear Inputs from previous fields after switching
        ClearAllInputsInContainerBasedOnDisplay(container);

    } else {
        betweenFields.forEach(function (field) {
            field.style.display = "none";
        });
        hideLabels([minRangeLabel, maxRangeLabel, lesserThanLabel, greaterThanLabel, minRangeUnit, maxRangeUnit, lesserThanUnit, greaterThanUnit]);

        // Clear Inputs from previous fields after switching
        ClearAllInputsInContainerBasedOnDisplay(container);
    }
}


// Function to display labels for filter range
function showLabels(labels) {
    labels.forEach(function(label) {
        label.style.display = "block";
    });
}


// Function to hide labels for filter range
function hideLabels(labels) {
    labels.forEach(function(label) {
        label.style.display = "none";
    });
}


// Function to clear all filters and checkboxes
function clearAllFilters() {
    // Clear text input fields
    var textInputs = document.querySelectorAll('input[type="text"]');
    textInputs.forEach(function(input) {
        input.value = '';
    });

    // Uncheck checkboxes
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });

    // Uncheck radio buttons
    var radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(function(radio) {
        radio.checked = false;
    });

    // Reset select elements
    var selectElements = document.querySelectorAll('select');
    selectElements.forEach(function(select) {
        select.selectedIndex = 0;
    });

    // Hide all filter containers
    var filterContainers = document.querySelectorAll('.filterContainer');
    filterContainers.forEach(function(container) {
        container.style.display = 'none';
    });

    // Remove active class from buttons
    var activeButtons = document.querySelectorAll('.selectionButton.active');
    activeButtons.forEach(function(button) {
        button.classList.remove('active');
    });

    var earlyMissionData = document.getElementById('earlyMissionRowData');
    var lateMissionData = document.getElementById('lateMissionRowData');
    earlyMissionData.innerHTML = "--";
    lateMissionData.innerHTML = "--";

}


// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Attach the clearAllFilters function to the "Clear Filters" button
    var clearFiltersButton = document.querySelector('.clearFiltersButton');
    if (clearFiltersButton) {
        clearFiltersButton.addEventListener('click', clearAllFilters);
    } else {
        console.error("Clear Filters button not found in the DOM.");
    }
});


// Check Select elements and remove error messages if they have already been selected
function checkSelect(elementId) {
    var select = document.getElementById(elementId);
    var computedStyle = window.getComputedStyle(select);
    var borderColor = computedStyle.getPropertyValue('border-color');

    if (borderColor === 'rgb(222, 82, 82)' && select.selectedIndex !== 0) {
        select.style.borderColor = 'grey';

        if (elementId == "hemisphereSelect"){
            document.getElementById("error_message_hemisphere").style.display = 'none';
        }

        if (elementId == "minRangeLabel"   || 
            elementId == "maxRangeLabel"   ||
            elementId == "lesserThanLabel" ||
            elementId == "greaterThanLabel" ){
            document.getElementById("error_message_hemisphere").style.display = 'none';
        }
    }
}
