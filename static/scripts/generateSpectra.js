
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
    // else {
    //     // Scroll the page to the top
    //     window.scrollTo({ top: 0, behavior: 'smooth' });
    // }

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