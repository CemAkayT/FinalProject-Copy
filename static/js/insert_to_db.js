var orders = [];

// Function to add order data to the array
function addOrder(quantity, title, price) {
  orders.push({ quantity: quantity, title: title, price: price });
}

// Call addOrder function whenever a div is generated
// Example usage:
addOrder(currentQuantity, title, currentPrice);

// When checkout is complete, send the orders to the server
function checkout() {
  // Send orders to the server using AJAX or Fetch API
  fetch("/checkout", {
    method: "POST",
    body: JSON.stringify(orders),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      // Handle the response from the server
      if (response.ok) {
        // Orders were successfully inserted
      } else {
        // Handle the error
      }
    })
    .catch((error) => {
      // Handle network or other errors
    });
}
