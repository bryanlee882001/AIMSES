
// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add this line to get the reference to the close button
    var modal = document.getElementById('spectraPanel');
    var span = document.querySelector('.close');

    // When the user clicks on x, close the modal
    span.onclick = function() {
        modal.style.display = "none";
        inputData = '';
        inputDict = {};

        const container = document.getElementById("selectionCriteriaContainter");
        if (container) {
            container.innerHTML = '';
        } else {
            console.error('Container not found');
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            inputData = '';
            inputDict = {};

            const container = document.getElementById("selectionCriteriaContainter");
            if (container) {
                container.innerHTML = '';
            } else {
                console.error('Container not found');
            }
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


