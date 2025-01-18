// Global Variable for Final Results
var resultData = {};

// Global Variable for Selection Criterias
var inputData = "";
var inputDict = {};

// Early Mission  (Get rid of 30105.59)
var earlyMission_xValues = [
  26091.51, 22077.43, 18063.35, 15052.79, 13045.75, 11038.72, 9031.68, 7526.4,
  6522.88, 5519.36, 4515.84, 3763.2, 3261.44, 2759.68, 2257.92, 1881.6, 1630.72,
  1379.84, 1128.96, 940.8, 815.36, 689.92, 564.48, 470.4, 407.68, 344.96,
  282.24, 235.2, 203.84, 172.48, 141.12, 117.6, 101.92, 86.24, 70.56, 58.8,
  50.96, 43.12, 35.28, 29.4, 25.48, 21.56, 17.64, 13.72, 9.8, 5.88,
];

// Late Mission  (Get rid of 3.92)
var lateMission_xValues = [
  28098.57, 24084.48, 20070.4, 16307.21, 14049.29, 12042.2, 10035.2, 8153.6,
  7024.643, 6021.12, 5017.6, 4076.8, 3512.32, 3010.56, 2508.8, 2038.4, 1756.16,
  1505.28, 1254.4, 1019.2, 878.08, 752.64, 627.2, 509.6, 439.04, 376.32, 313.6,
  254.8, 219.52, 188.16, 156.8, 127.4, 109.76, 94.08, 78.4, 63.7, 54.88, 47.04,
  39.2, 31.85, 27.44, 23.52, 19.6, 15.19, 7.84, 3.92,
];

// Both Missions
var bothMissions_xValues = [
  29152.08, 25153.495, 21073.915, 17185.28, 14550.04, 12543.975, 10586.96,
  8592.64, 6773.7615, 5770.24, 4766.72, 3946.32, 3375.12, 2909.12, 2526.16,
  2148.16, 1819.28, 1552.5, 1317.12, 1184.08, 1030.04, 910.5, 784.28, 647.6,
  537.04, 454.72, 391, 329.28, 268.52, 227.36, 195.5, 164.64, 134.26, 113.68,
  97, 82.32, 67.13, 56.84, 49, 41.16, 33.565, 28.42, 24.5, 20.58, 16.415, 10.78,
  6.86, 4.9,
];

// Function that extracts user input and performs validation before sending to backend
function generateSpectra() {
  console.log("Generating Spectra...");

  // Get User Input
  var [inputDict, inputData] = getUserInput();

  // Invalid User Input
  if (!inputDict || !inputData) {
    alert("Error Processing User Inputs");
    button.textContent = "Generate Spectra";
    return;
  }

  // Prompt Error if there's no spectral gneerational requirements in user input:
  if (
    !inputDict.hasOwnProperty("Statistics") ||
    !inputDict.hasOwnProperty("Spectra") ||
    !inputDict.hasOwnProperty("Normalization") ||
    !inputDict.hasOwnProperty("Mission")
  ) {
    alert(
      "Ensure that you've selected option(s) for Step 3: Statistics, Spectra, Normalization, and Mission"
    );
    return;
  }

  // Measure the start time
  var startTime = performance.now();

  // Display data in the modal if there is any input or selection
  if (validateFilters()) {
    if (inputData.trim() !== "") {
      // Summary Statistics
      var inputData = createFilterSelectionSummary(inputDict);

      console.log(inputDict);

      // Show loading screen
      document.getElementById("loadingContainer").style.display = "block";
      animateLoadingPanel("loading-text");

      // Send data to backend
      sendDataToBackend(inputDict)
        .then((result) => {
          document.getElementById("loadingContainer").style.display = "none";

          // Assign to global Variable
          resultData = JSON.parse(result);

          if (resultData.result == 0) {
            clearFilters();
            alert("No Datasets found for the criterias you've selected");
            return;
          } else {
            createCharts();
            openModal();
          }

          // Calculate Time Required to Execute function
          var endTime = performance.now();
          var timeDiff = endTime - startTime;

          // Convert milliseconds to seconds
          var totalSeconds = timeDiff / 1000;

          // Output the time difference in seconds
          console.log(
            "Total Time taken to generate Spectra: " + totalSeconds + " seconds"
          );

          inputData = "";
          inputDict = {};
        })
        .catch((error) => {
          clearFilters();
          console.error("Error:", error);
          document.getElementById("loadingContainer").style.display = "none";
          alert("Error Generating Graphs: " + error);
          return;
        });
    } else {
      clearFilters();
      document.getElementById("loadingContainer").style.display = "none";
      alert("Ensure that selection ranges are correct in Step 2");
    }
  }
}

// Send data to backend in a dictionary format from generateSpectra()
function sendDataToBackend(data) {
  return fetch("/process-data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: data }),
  })
    .then((response) => response.text())
    .catch((error) => {
      console.error("Error:", error);
      throw error;
    });
}

// Displays Selection Criteria in modal
function createSelectionCriteriaBoxes(text) {
  // Select the container
  const container = document.getElementById("selectionCriteriaContainter");

  // Create a box container element
  const box = document.createElement("div");
  box.classList.add("selectionCriteriaBox");

  // Create a paragraph element for the text
  const textElement = document.createElement("p");
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
    var selectionAndFilterSummary = "";

    selectionAndFilterSummary += selectionCriteria + " : ";

    var selection = inputDict[selectionCriteria];

    // check if value is a dictionary
    if (typeof selection === "object") {
      if (selection.hasOwnProperty("Hemisphere")) {
        selectionAndFilterSummary += selection["Hemisphere"] + ", ";
      }

      if (selection.hasOwnProperty("Range")) {
        if (selection["Range"] == "Between") {
          selectionAndFilterSummary +=
            " Between " +
            selection["minRange"] +
            " and " +
            selection["maxRange"];
        } else if (selection["Range"] == "Lesser Than") {
          selectionAndFilterSummary +=
            " Lesser Than " + selection["lesserThanValue"];
        } else if (selection["Range"] == "Greater Than") {
          selectionAndFilterSummary +=
            " Greater Than " + selection["greaterThanValue"];
        } else {
          selectionAndFilterSummary += " Invalid Range";
        }
      }

      // If selection criteria is mechanism, it should only have one element since its a radio button
      if (selectionCriteria == "MECHANISMS" && selection.length == 1) {
        selectionAndFilterSummary += selection[0];
      }
    }

    // if value is not a dictionary, it is an array
    if (
      selectionCriteria === "Statistics" ||
      selectionCriteria === "Spectra" ||
      selectionCriteria === "Normalization" ||
      selectionCriteria === "Mission"
    ) {
      selectionAndFilterSummary += inputDict[selectionCriteria].join(", ");
    }

    listOfSelections.push(selectionAndFilterSummary);
  }

  // Remove the comma at the end
  if (selectionAndFilterSummary.endsWith(",")) {
    selectionAndFilterSummary = selectionAndFilterSummary.slice(0, -1);
  }

  // Dynamically create selection criteria to display in modal
  listOfSelections.forEach((selection) => {
    createSelectionCriteriaBoxes(selection);
  });

  return listOfSelections;
}

// Gets Early and Late Mission Data
function generateMissionCount() {
  // Measure the start time
  var startTime = performance.now();

  var earlyMissionData = document.getElementById("earlyMissionRowData");
  var lateMissionData = document.getElementById("lateMissionRowData");
  earlyMissionData.innerHTML = "--";
  lateMissionData.innerHTML = "--";

  // Toggle the 'active' class on the button
  var generateMissionButton = document.getElementById("generateMissionButton");
  generateMissionButton.classList.toggle("active");

  // userInput = [inputDict, inputData]
  var userInput = getUserInput();

  if (!userInput) {
    clearFilters();
    alert("Invalid User Input");
  }

  var data = userInput[0];

  earlyMissionData.innerHTML = "loading...";
  lateMissionData.innerHTML = "loading...";

  if (validateFilters()) {
    fetch("/mission-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: data }),
    })
      .then((response) => response.json())
      .then((result) => {
        var earlyMissionCount = result.result[0].toString();
        var lateMissionCount = result.result[1].toString();

        earlyMissionData.innerHTML =
          earlyMissionCount.replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " event(s)";
        lateMissionData.innerHTML =
          lateMissionCount.replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " event(s)";

        if (generateMissionButton.classList.contains("active")) {
          // If the button already has 'active' class, remove it
          generateMissionButton.classList.remove("active");
        }

        // Calculate Time Required to Execute function
        var endTime = performance.now();
        var timeDiff = endTime - startTime;

        // Convert milliseconds to seconds
        var totalSeconds = timeDiff / 1000;

        // Output the time difference in seconds
        console.log(
          "Total Time taken to calculate mission count: " +
            totalSeconds +
            " seconds"
        );

        // Clear global variables to avoid duplication
        clearFilters();
      })
      .catch((error) => {
        clearFilters();
        console.error("Error:", error);

        earlyMissionData.innerHTML = "--";
        lateMissionData.innerHTML = "--";
      });
  } else {
    clearFilters();
    earlyMissionData.innerHTML = "--";
    lateMissionData.innerHTML = "--";
  }
}

// Gets User input and stores them in both a dictionary and a text format
function getUserInput() {
  // Gather data from visible text input fields
  var textInputs = document.querySelectorAll(
    'input[type="text"]:not([style*="display:none"])'
  );
  textInputs.forEach(function (input) {
    var filterTitle = input
      .closest(".filterContainer")
      .querySelector(".filterTitle").textContent;
    if (input.value.trim() !== "") {
      // Check if filter title exists in inputDict
      if (!inputDict[filterTitle]) {
        // Create a new dictionary for the filter title
        inputDict[filterTitle] = {};
      }

      // Assign the new value to the placeholder in the filter title dictionary
      inputDict[filterTitle][input.name] = input.value;

      // Display results
      inputData +=
        filterTitle + " : " + input.name + ": " + input.value + "<br>";
    }
  });

  // Gather data from visible checkboxes (both regular and radio)
  var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
  checkboxes.forEach(function (checkbox) {
    var filterTitle = checkbox
      .closest(".spectraGenerationRequirementCategory")
      .querySelector(".filterTitle").textContent;

    // Check if filter title exists in inputDict
    if (filterTitle in inputDict) {
      inputDict[filterTitle].push(checkbox.parentNode.textContent.trim());
    } else {
      inputDict[filterTitle] = [checkbox.parentNode.textContent.trim()];
    }

    // Display results
    inputData +=
      filterTitle + " : " + checkbox.parentNode.textContent.trim() + "<br>";
  });

  // Gather data from visible radio buttons
  var radioButtons = document.querySelectorAll('input[type="radio"]:checked');
  radioButtons.forEach(function (radio) {
    // Check if the radio button is within a filterContainer
    var filterContainer = radio.closest(".filterContainer");
    if (filterContainer && filterContainer.style.display !== "none") {
      var filterTitleElement = filterContainer.querySelector(".filterTitle");
      if (filterTitleElement) {
        var filterTitle = filterTitleElement.textContent;
        inputData +=
          filterTitle + " : " + radio.parentNode.textContent.trim() + "<br>";

        if (filterTitle in inputDict) {
          inputDict[filterTitle].push(radio.parentNode.textContent.trim());
        } else {
          inputDict[filterTitle] = [radio.parentNode.textContent.trim()];
        }
      }
    }

    // Check if the radio button is within a spectraGenerationRequirementCategory
    var spectraCategory = radio.closest(
      ".spectraGenerationRequirementCategory"
    );
    if (spectraCategory) {
      var filterTitleElement = spectraCategory.querySelector(".filterTitle");
      if (filterTitleElement) {
        var filterTitle = filterTitleElement.textContent;

        inputData +=
          filterTitle + " : " + radio.parentNode.textContent.trim() + "<br>";

        if (filterTitle in inputDict) {
          inputDict[filterTitle].push(radio.parentNode.textContent.trim());
        } else {
          inputDict[filterTitle] = [radio.parentNode.textContent.trim()];
        }
      }
    }
  });

  // Gather data from visible dropdown menus
  var selectElements = document.querySelectorAll("select");
  selectElements.forEach(function (select) {
    var filterTitle = select
      .closest(".filterContainer")
      .querySelector(".filterTitle").textContent;
    var selectedOption = select.options[select.selectedIndex].text;
    if (
      selectedOption.trim() !== "Select a Hemisphere" &&
      selectedOption.trim() !== "Select a Range"
    ) {
      inputData += filterTitle + " : " + selectedOption + "<br>";

      // Check if filter title exists in inputDict
      if (!inputDict[filterTitle]) {
        // Create a new dictionary for the filter title
        inputDict[filterTitle] = {};
      }

      if (
        selectedOption == "Northern Hemisphere" ||
        selectedOption == "Southern Hemisphere" ||
        selectedOption == "Either"
      ) {
        inputDict[filterTitle]["Hemisphere"] = selectedOption;
      } else {
        // Assign the new value to the placeholder in the filter title dictionary
        inputDict[filterTitle]["Range"] = selectedOption;
      }
    }
  });

  return [inputDict, inputData];
}

// Exports DataSets as a CSV file format
function exportCSV() {
  if (Object.keys(resultData).length === 0) {
    alert("Error Downloading CSV. Invalid Datasets");
  }

  yAxisValues = resultData.result.yAxis;

  // Prepare CSV content for x-values
  let csvContent = "X-Values: energy (eV)\n";
  csvContent += `number: ${inputDict["Mission"].length}\n`;
  var mission = inputDict["Mission"][0];
  var xValues =
    mission === "Early Mission"
      ? earlyMission_xValues
      : mission === "Late Mission"
      ? lateMission_xValues
      : bothMissions_xValues;
  csvContent += "energy, " + xValues.join(",") + "\n\n";

  // Add each y-values array to the CSV content
  csvContent += `Y-Values: dEFlux\n`;
  csvContent += `number: ${Object.getOwnPropertyNames(yAxisValues).length}\n`;
  for (const key in yAxisValues) {
    if (yAxisValues.hasOwnProperty(key)) {
      // Update key for sigma symbols if needed
      var updatedKey = key;
      if (key == "+1σ") {
        updatedKey = "+1 sigma";
      } else if (key == "-1σ") {
        updatedKey = "-1 sigma";
      }

      csvContent += `${updatedKey}, ` + yAxisValues[key].join(",") + "\n";
    }
  }
  csvContent += "\n";

  // Add selection criteria to the CSV content
  csvContent += "Selection Criteria\n";
  csvContent += `number: ${Object.getOwnPropertyNames(inputDict).length}\n`;
  for (let selectionCriteria in inputDict) {
    csvContent += selectionCriteria + ",";

    var selection = inputDict[selectionCriteria];

    // check if value is a dictionary
    if (typeof selection === "object") {
      if (selection.hasOwnProperty("Hemisphere")) {
        csvContent += selection["Hemisphere"] + ", ";
      }

      if (selection.hasOwnProperty("Range")) {
        if (selection["Range"] == "Between") {
          csvContent +=
            " Between, " +
            selection["minRange"] +
            " , " +
            selection["maxRange"];
        } else if (selection["Range"] == "Lesser Than") {
          csvContent += " Lesser Than, " + selection["lesserThanValue"];
        } else if (selection["Range"] == "Greater Than") {
          csvContent += " Greater Than, " + selection["greaterThanValue"];
        } else {
          csvContent += " Invalid Range";
        }
      }

      // If selection criteria is mechanism, it should only have one element since its a radio button
      if (selectionCriteria == "MECHANISMS" && selection.length == 1) {
        csvContent += selection[0];
      }
    }

    // if value is not a dictionary, it is an array
    if (
      selectionCriteria === "Statistics" ||
      selectionCriteria === "Spectra" ||
      selectionCriteria === "Normalization" ||
      selectionCriteria === "Mission"
    ) {
      // CSV cannot read sigma symbol
      var finalStatisticsArr = [];
      for (const ele of inputDict[selectionCriteria]) {
        if (ele == "+1σ") {
          finalStatisticsArr.push("+1 sigma");
        } else if (ele == "-1σ") {
          finalStatisticsArr.push("-1 sigma");
        } else {
          finalStatisticsArr.push(ele);
        }
      }

      csvContent += finalStatisticsArr.join(", ");
    }
    csvContent += "\n";
  }

  // Create a Blob with the CSV content
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

  // Generate download link for the CSV file
  const link = document.createElement("a");
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);

    // Get current date and time
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, "0");
    const day = String(currentDate.getDate()).padStart(2, "0");
    const hours = String(currentDate.getHours()).padStart(2, "0");
    const minutes = String(currentDate.getMinutes()).padStart(2, "0");
    const dateString = `${year}${month}${day}_${hours}${minutes}`;
    link.setAttribute("download", `datasets_${dateString}.csv`);

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// Exports graph as a JPEG format
function exportJPEG() {
  var canvas = document.getElementById("myChart");

  // Convert the chart to a base64-encoded JPEG image
  var imageData = canvas.toDataURL("image/jpeg");
  var link = document.createElement("a");

  // Set the href attribute to the base64-encoded image data
  link.href = imageData;

  // Get current date and time
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = String(currentDate.getMonth() + 1).padStart(2, "0");
  const day = String(currentDate.getDate()).padStart(2, "0");
  const hours = String(currentDate.getHours()).padStart(2, "0");
  const minutes = String(currentDate.getMinutes()).padStart(2, "0");
  const dateString = `${year}${month}${day}_${hours}${minutes}`;

  // Set the download attribute to specify the filename
  link.download = `spectra_graph_${year}${month}${day}_${hours}${minutes}.jpg`;

  // Programmatically trigger the download
  link.click();
}

// Wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Add this line to get the reference to the close button
  var modal = document.getElementById("spectraPanel");
  var span = document.querySelector(".close");

  // When the user clicks on x, close the modal
  span.onclick = function () {
    modal.style.display = "none";
    clearFilters();
  };

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
      clearFilters();
    }
  };
});

// Function to open the modal
function openModal() {
  var modal = document.getElementById("spectraPanel");
  modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
  var modal = document.getElementById("spectraPanel");
  modal.style.display = "none";
}

// Function to clear filters in modalContainer and global variabls inputData and inputDict
function clearFilters() {
  inputData = "";
  inputDict = {};

  const container = document.getElementById("selectionCriteriaContainter");
  if (container) {
    container.innerHTML = "";
  } else {
    console.error("Container not found");
  }
}

// Function to animate loading screen
function animateLoadingPanel(elementId) {
  const loadingText = document.getElementById(elementId);
  let dotCount = 0;

  // Clear any existing interval
  if (loadingText.intervalId) {
    clearInterval(loadingText.intervalId);
  }

  loadingText.intervalId = setInterval(() => {
    dotCount = (dotCount + 1) % 4; // Cycle through 0 to 3
    loadingText.innerText = `Generating Graph${".".repeat(dotCount)}`;
  }, 500);
}
