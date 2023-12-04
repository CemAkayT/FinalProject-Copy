function addProductToCart(quantity, title, price) {
  const cartContainer = document.getElementById("cart");
  const cartItemCountElement = document.getElementById("cartItemCount");

  const cartItem = document.createElement("div");
  cartItem.classList.add("cart-item");

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
    quantityElement.textContent = currentQuantity;
    updateCartItemPrice();
    updateCartItemCount(true); // Increment the count
    cartQuantityElement.textContent = currentQuantity;

  });

  decrementButton.addEventListener("click", () => {
    if (currentQuantity > 0) {
      currentQuantity--;
      quantityElement.textContent = currentQuantity;
      updateCartItemPrice();
      updateCartItemCount(false); // Decrement the count
      cartQuantityElement.textContent = currentQuantity;

      if (currentQuantity === 0) {
        cartContainer.removeChild(cartItem); // Remove the item from the cart if count reaches 0
        removeOrderFromArray(currentQuantity, title, price);
      }
    }
    console.log("Vi trækker et produkt fra array", orders);
  });

  // Function to update the displayed quantity for this specific cart item
  function updateCartItemPrice() {
    const cartPriceElement = cartItem.querySelector(".cart-price");
    currentPrice = currentQuantity * parseFloat(price.replace(" kr.", ""));
    cartPriceElement.textContent = currentPrice.toFixed(2) + " kr.";
    //herefter virker 1000 separatoren ikke
    updateTotalPrice();
  }

  cartContainer.appendChild(cartItem);

  const separator = document.createElement("hr");
  cartItem.appendChild(separator);

  // Update the total price
  updateCartItemCount(true);
  updateTotalPrice();

  // Increment the cart item count
  function updateCartItemCount(increment) {
    const currentCount = parseInt(cartItemCountElement.textContent);
    if (increment) {
      cartItemCountElement.textContent = currentCount + 1;
    } else {
      if (currentCount > 0) {
        cartItemCountElement.textContent = currentCount - 1;
      }
    }
    sessionStorage.setItem("quantity", cartItemCountElement.textContent);
  }

  console.log("Vi har tilføjet et nyt produkt til array:", orders);
}
// Her slutter addProductToCart()



