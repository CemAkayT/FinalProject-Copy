function removeCartItem(cartContainer, cartItem) {
  cartContainer.removeChild(cartItem);
}

// Function to update the total in parentheses
function updateTotalInParentheses() {
  const nettoPrisElement = document.getElementById("netto");
  const nettoPrice = parseFloat(nettoPrisElement.innerText.replace(" kr.", ""));
  totalInParentheses.textContent = `(${nettoPrice.toFixed(2)} kr.)`;
}

// Example: Handle the click event for the "+" button to add a product
const plusButtons = document.querySelectorAll(".larger-plus");

plusButtons.forEach((button) => {
  button.addEventListener("click", function () {
    // Get product information from the clicked element
    const quantity = 1; // count is 1 first time a product is added
    const titleElement = this.closest(".row").querySelector(".titel");
    const title = titleElement.textContent;
    const priceElement = this.closest(".row").querySelector(".pris");
    const price = priceElement.textContent;
    // Add the product to the cart
    addProductToCart(quantity, title, price);
  });
});