document.addEventListener("DOMContentLoaded", function () {
  const loadDataButton = document.getElementById("load-data-btn");
  loadDataButton.addEventListener("click", function () {
    fetch("http://127.0.0.1:5000/getGridInfo")
      .then((response) => response.json())
      .then((data) => {
        console.log("Received data:", data); // Log data for debugging
        clearGrid();
        if (data.success && Array.isArray(data.grid)) {
          createGrid(data.grid);
        } else {
          console.error("Received data is not in the expected format:", data);
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});

function createGrid(gridData) {
  const gridContainer = document.getElementById("grid-container");
  gridData.forEach((item) => {
    if (item.position[0] === 0 || item.position[1] === 0) return; // Skip the 0 indexes as per your requirement
    const gridItem = document.createElement("div");
    gridItem.classList.add("grid-item");
    gridItem.innerText = `Name: ${item.name}\nPosition: [${item.position}]\nWeight: ${item.weight}`;
    gridContainer.appendChild(gridItem);
  });
}

function clearGrid() {
  const gridContainer = document.getElementById("grid-container");
  gridContainer.innerHTML = "";
}
