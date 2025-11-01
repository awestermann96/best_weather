function toggleCheckboxes(containerId) {
  let container = document.getElementById(containerId);

  // Get the current computed display value of the container
  let currentDisplay = getComputedStyle(container).display;

  // Toggle visibility based on the current display value
  if (currentDisplay === "none") {
    container.style.display = "block";  // Show the container
  } else {
    container.style.display = "none";  // Hide the container
  }
}

window.addEventListener('mouseup', function(event) {
  var checkboxesContainers = document.querySelectorAll('.checkboxes');
  var buttons = document.querySelectorAll('.selectBox');

  // Iterate over all checkboxes containers
  checkboxesContainers.forEach(function(container, index) {
    var button = buttons[index]; // Get the corresponding button based on index
    
    // If the click was outside both the container and the button
    if (!container.contains(event.target) && !button.contains(event.target)) {
      container.style.display = 'none';  // Hide the container
    }
  });
});

