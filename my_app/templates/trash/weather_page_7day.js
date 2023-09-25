
// Create the main container div
const mainContainer = document.createElement('div');
mainContainer.id = 'mainContainer';
const forecast_element = document.getElementById('forecast');
forecast_element.body.appendChild(mainContainer);

// Loop to create 7 child divs
for (let i = 1; i <= 7; i++) {
  const childDiv = document.createElement('div');
  childDiv.className = 'childDiv';
  mainContainer.appendChild(childDiv);

  // Create an image element
  const image = document.createElement('img');
  image.src = `image${i}.jpg`; // Assuming you have images named image1.jpg, image2.jpg, etc.
  image.alt = `Image ${i}`;
  childDiv.appendChild(image);

  // Create a table element
  const table = document.createElement('table');
  const tr = document.createElement('tr');
  const td = document.createElement('td');
  td.textContent = `Table ${i}`;
  tr.appendChild(td);
  table.appendChild(tr);
  childDiv.appendChild(table);
}
