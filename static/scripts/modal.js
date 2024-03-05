
// Add this line to get the reference to the close button
var modal = document.getElementById('spectraPanel');
var span = document.querySelector('.close');


// When the user clicks on x, close the modal
span.onclick = function() {
    modal.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


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

