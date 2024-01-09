function addProductToCart(quantity, title, price) {
  const cartContainer = document.getElementById("cart");
  console.log("Vi tager fat i div med id 'cart'");
  const cartItemCountElement = document.getElementById("cartItemCount");
  console.log("vi tager fat i det lille tal ved siden af kurven");

  const cartItem = document.createElement("div");
  console.log("vi opretter div");
  cartItem.classList.add("cart-item");
  console.log("et nyt cart-item div er oprettet");

  // Store the initial quantity and price
  let currentQuantity = quantity;
  let currentPrice = parseFloat(price.replace(" kr.", ""));

  cartItem.innerHTML = `
                <div class="d-flex justify-content-between my-4">
                <div class="cart-quanity">${currentQuantity}</div>
                <div class="cart-title">${title}</div>
                <div class="cart-price mr-2">${currentPrice.toLocaleString(
                  "da-DK",
                  { minimumFractionDigits: 2, maximumFractionDigits: 2 }
                )} kr.</div>
                </div> 
                
                <div
                class="container d-flex justify-content-around"
                style="width: 225px"
              >
                <button type="button" class="btn btn-rounded btn-circle" id="decrementQuantity">
                  <i class="fa-solid fa-minus"></i>
                </button>
                <span class="mt-2">${currentQuantity}</span>
                <button type="button" class="btn btn-rounded btn-circle" id="incrementQuantity">
                  <i class="fa-solid fa-plus"></i>
                </button>
              </div> 
              `;

  // Get references to the buttons and quantity element inside the cartItem
  const incrementButton = cartItem.querySelector("#incrementQuantity");
  const decrementButton = cartItem.querySelector("#decrementQuantity");
  const quantityElement = cartItem.querySelector(".mt-2");

  const cartQuantityElement = cartItem.querySelector(".cart-quanity");

  // Add click event listeners to the buttons for this specific cart item
  incrementButton.addEventListener("click", () => {
    currentQuantity++;
    cartQuantityElement.textContent = currentQuantity;
    quantityElement.textContent = currentQuantity;
    updateCartItemPrice();
    updateCartItemCount(true); // Increment the count in the cart
    console.log("Vi øger antal af samme produkt");
  });

  decrementButton.addEventListener("click", () => {
    if (currentQuantity > 0) {
      currentQuantity--;
      quantityElement.textContent = currentQuantity;
      cartQuantityElement.textContent = currentQuantity;
      updateCartItemPrice();
      updateCartItemCount(false); // Decrement the count in the cart
      console.log("Vi reducerer antal af samme produkt i kurven");

      if (currentQuantity === 0) {
        cartContainer.removeChild(cartItem); // Remove the item from the cart if count reaches 0
        console.log("Vi fjerner produktet helt fra kurven");
      }
    }
  });

  // Function to update the displayed quantity for this specific cart item
  function updateCartItemPrice() {
    const cartPriceElement = cartItem.querySelector(".cart-price");
    currentPrice = currentQuantity * parseFloat(price.replace(" kr.", ""));
    cartPriceElement.textContent =
      currentPrice.toFixed(2).replace(".", ",") + " kr.";
    updateTotalPrice();
  }

  cartContainer.appendChild(cartItem);

  const separator = document.createElement("hr");
  cartItem.appendChild(separator);
  console.log("Vi tilføjer seperator <hr>");

  // Update the total price
  updateCartItemCount(true);
  updateTotalPrice();

  // Funktionen står for at holde styr på antal ved siden af kurv svg
  function updateCartItemCount(increment) {
    const currentCount = parseInt(cartItemCountElement.textContent);
    if (increment) {
      cartItemCountElement.textContent = currentCount + 1;
      console.log("det lille tal ved siden af kurven er øget med en");
    } else {
      if (currentCount > 0) {
        cartItemCountElement.textContent = currentCount - 1;
        console.log("det lille tal ved siden af kurven reduceres med en");
      }
    }
    sessionStorage.setItem("quantity", cartItemCountElement.textContent);
    console.log(sessionStorage.getItem("quantity"));
  }
}
