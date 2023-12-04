function updateTotalPrice() {
  const nettoPrisElement = document.getElementById("netto");
  const cartItems = document.querySelectorAll(".cart-item");
  let total = 0;

  cartItems.forEach((item) => {
    const itemPrice = parseFloat(
      item.querySelector(".cart-price").textContent.replace(" kr.", "")
    );
    total += itemPrice;
  });

  nettoPrisElement.textContent = total.toFixed(2) + " kr.";

  // Store the total value in localStorage
  sessionStorage.setItem("nettoAmount", total.toFixed(2) + " kr.");

  // Update the total in parentheses
  updateTotalInParentheses();
}
