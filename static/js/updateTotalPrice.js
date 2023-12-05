function updateTotalPrice() {
  const nettoPrisElement = document.getElementById("netto");
  const cartItems = document.querySelectorAll(".cart-item");
  let total = 0;

  let orders = [];

  cartItems.forEach((item) => {
    let order = {};
    const itemPrice = parseFloat(
      item.querySelector(".cart-price").textContent.replace(" kr.", "")
    );

    order.qnty = item.querySelector(".cart-quanity").textContent;
    order.title = item.querySelector(".cart-title").textContent;

    total += itemPrice;
    order.price = itemPrice;
    orders.push(order);
  });

  let orderJSON = JSON.stringify(orders);
  console.log("Orders", orders);

  sessionStorage.setItem("orderJSON", orderJSON)

  nettoPrisElement.textContent = total.toFixed(2) + " kr.";

  // Store the total value in localStorage
  sessionStorage.setItem("nettoAmount", total.toFixed(2) + " kr.");

  // Update the total in parentheses
  updateTotalInParentheses();
}
